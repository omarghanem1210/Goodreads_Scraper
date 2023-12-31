import json
import time
from urllib.error import HTTPError

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
import re


def log_in():
    email = ''
    password = ''
    driver = webdriver.Chrome()
    driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid'
               '.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F'
               '%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F'
               '%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads'
               '.com%2Fap-handler%2Fsign-in&siteState=9d60eb2d7ef31314ecc2c6d068065c5e')
    input_email = driver.find_element(By.ID, 'ap_email')
    input_password = driver.find_element(By.ID, 'ap_password')
    sign_in = driver.find_element(By.ID, 'signInSubmit')

    input_email.send_keys(email)
    time.sleep(5)
    input_password.send_keys(password)
    time.sleep(2)
    sign_in.click()
    return driver


def scrape(driver, start_url, table_name, shelves=None, as_dataframe=False):
    with open('location.txt', 'r') as file:
        i = int(file.readline())
        shelf = int(file.readline())
    if as_dataframe:
        books_data = pd.DataFrame(
            columns=['Title', 'Genre', 'Author_Name', 'Summary', 'Page_Count', 'Average_Rating', 'Num_Ratings',
                     'Num_Reviews', 'url', 'isbn'])

    while True:
        if shelves != None:
            current_page = f'{start_url}/{shelves[shelf]}?page={i}'
        else:
            current_page = f'{start_url}?page={i}'
        driver.get(current_page)

        html = driver.page_source.encode('utf-8').strip()
        bs = BeautifulSoup(html, 'lxml')

        book_links = bs.find_all('a', {'class': 'bookTitle', 'itemprop': 'url'})
        if len(book_links) == 0:
            break
        for link in book_links:
            href = 'https://www.goodreads.com/' + link.attrs['href']
            print(href)
            driver.get(href)
            try:
                book_html = driver.page_source
            except HTTPError as e:
                book_html = driver.page_source
            bs = BeautifulSoup(book_html, 'lxml')
            try:
                summary = str(bs.find('span', {'class': 'Formatted'}).contents)
                summary = re.sub('<[^>]*>', '', summary)[1:-1]
            except:
                time.sleep(5)
                driver.get(href)
                time.sleep(2)
                book_html = driver.page_source
                bs = BeautifulSoup(book_html, 'lxml')
                summary = str(bs.find('span', {'class': 'Formatted'}).contents)
                summary = re.sub('<[^>]*>', '', summary)

            information = str(bs.find('script', {'type': 'application/ld+json'}).contents).replace('[', '').replace(']',
                                                                                                                    '')[
                          1:-1]

            try:
                information = json.loads(information)

            except json.decoder.JSONDecodeError as e:
                print('Could not parse json')
                continue
            try:
                language = information['inLanguage']
            except KeyError:
                language = None
            if language != 'English' and language is not None:
                print('Book not in english')
                continue

            title = information['name']
            try:
                page_count = information['numberOfPages']
            except KeyError as e:
                page_count = None
            try:
                author_name = information['author']['name']
            except KeyError:
                author_name = None
            try:
                average_rating = information['aggregateRating']['ratingValue']
            except KeyError:
                average_rating = None
            try:
                num_ratings = information['aggregateRating']['ratingCount']
            except KeyError:
                num_ratings = None
            try:
                num_reviews = information['aggregateRating']['reviewCount']
            except KeyError:
                num_reviews = None
            try:
                genre = str(bs.find('span', {'class': 'BookPageMetadataSection__genreButton'}).find('a').attrs['href'])[
                        33:]
            except AttributeError as e:
                genre = None
            print(json.dumps(information))
            try:
                isbn = information['isbn']
            except KeyError:
                isbn = None
            if not as_dataframe:
                store(title, genre, author_name, summary, page_count, average_rating, num_ratings,
                  num_reviews, href, isbn, table_name)
            else:
                books_data = books_data.append(
                    {'Title': title, 'Genre': genre, 'Author_name': author_name, 'Summary': summary,
                     'Page_Count': page_count, 'Average_Rating': average_rating,
                     'Num_Ratings': num_ratings
                        , 'Num_Reviews': num_reviews, 'url': href, 'isbn': isbn})

        i += 1
        with open('location.txt', 'w') as file:
            file.write(f'{i}\n')
            file.write(str(shelf))
    shelf += 1
    with open('location.txt', 'w') as file:
        file.write(f'{i}\n')
        file.write(str(shelf))
    if as_dataframe:
        return books_data


def store(title, genre, author_name, summary, page_count, average_rating, num_ratings,
          num_reviews, url, isbn, table_name):
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           passwd='6456456456456456-*-*/hfd -*-/*-gd*//>?[gdfg', db='mysql')
    cur = conn.cursor()
    cur.execute('USE goodreads')
    cur.execute(f'INSERT INTO {table_name} (Title, Genre, Author_Name, Summary, Page_Count, Average_Rating, '
                f'Num_Ratings, '
                'Num_Reviews, url, isbn) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (title, genre, author_name, summary, page_count, average_rating, num_ratings
                 , num_reviews, url, isbn))
    conn.commit()
    cur.close()
    conn.close()