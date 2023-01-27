import re
from urllib.error import HTTPError
from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json

email = 'omarghanem1210@gmail.com'
password = 'sekiro18*'

driver = webdriver.Chrome()
driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid'
           '.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F'
           '%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F'
           '%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads'
           '.com%2Fap-handler%2Fsign-in&siteState=9d60eb2d7ef31314ecc2c6d068065c5e')
ID = 'id'
NAME = 'name'
XPATH = 'xpath'
LINK_TEXT = 'link text'
PARTIAL_LINK_TEXT = 'partial link text'
TAG_NAME = 'tag name'
CLASS_NAME = 'class name'
CSS_SELECTOR = 'css selector'

input_email = driver.find_element(By.ID, 'ap_email')
input_password = driver.find_element(By.ID, 'ap_password')
sign_in = driver.find_element(By.ID, 'signInSubmit')

input_email.send_keys(email)
input_password.send_keys(password)
sign_in.click()

start_url = 'https://www.goodreads.com/shelf/show/'

shelves = ['published-2020', 'published-2021', 'published-2022', 'published-2023']

shelf = shelves[0]
i = 1
current_page = f'{start_url}/{shelf}?page={1}'

driver.get(current_page)
html = driver.page_source
bs = BeautifulSoup(html, 'lxml')

book_links = bs.find_all('a', {'class': 'bookTitle'})
for link in book_links:
    href = 'https://www.goodreads.com/' + link.attrs['href']
    driver.get(href)
    try:
        book_html = driver.page_source
    except HTTPError as e:
        book_html = driver.page_source
    bs = BeautifulSoup(book_html, 'lxml')
    summary = bs.find('meta', property='og:description').attrs['content']
    information = str(bs.find('script', {'type': 'application/ld+json'}).contents).replace('[', '').replace(']', '')[
                  1:-1]
    information = json.loads(information)
    title = information['name']
    page_count = information['numberOfPages']
    author_name = information['author']['name']
    average_rating = information['aggregateRating']['ratingValue']
    num_ratings = information['aggregateRating']['ratingCount']
    num_reviews = information['aggregateRating']['reviewCount']
    genre = str(bs.find('span', {'class': 'BookPageMetadataSection__genreButton'}).find('a').attrs['href'])[33:]
    print(f'{summary}   {page_count}  {author_name}  {average_rating}   {num_ratings}   {num_reviews}  {genre}')

    try:
        page_count = int(bs.find('meta', property='books:page_count').attrs['content'])
    except:
        page_count = None
    author_name = str(bs.find('span', {'itemprop': 'name'}).contents).replace('[', '').replace(']', '')
    genre = str(bs.find('a', {'actionLinkLite bookPageGenreLink'}).contents).replace('[', '').replace(']', '')
    average_rating = float(str(bs.find('span', {'itemprop': 'ratingValue'}).contents). \
                           replace('[', '').replace(']', '').replace('\\n', '').replace(' ', '')[1:-2])
    num_ratings = int(bs.find('meta', {'itemprop': 'ratingCount'}).attrs['content'])
    top_review = str(bs.find('span', {'id': re.compile('^freeTextContainer')}).contents).replace('[',
                                                                                                 '').replace(
        ']', '')
    top_review = re.sub('<[^>]*>', '', top_review)
    num_reviews = int(bs.find('meta', {'itemprop': 'reviewCount'}).attrs['content'])
    print(f'{average_rating}, {num_ratings}')
"""
while True:
    html = urlopen(current_page)
    bs = BeautifulSoup(html, 'html.parser')
    book_links = bs.find_all('a', {'class': 'bookTitle'})

    if book_links is None:
        break
    for link in book_links:
        href = 'https://www.goodreads.com/' + link.attrs['href']
        print(href)
        book_html = requests.get(href).text
        bs = BeautifulSoup(book_html, 'html.parser')
        title = bs.find('meta', property='og:title')
        summary = bs.find('meta', property='og:description')
        page_count = bs.find('meta', property='books:page_count')
        name = bs.find('span', {'itemprop': 'name'}).text

        print(title.attrs['content'])
"""
