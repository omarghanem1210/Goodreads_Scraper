from scraper import scrape, log_in

table_name = 'espionage_books'
start_url = 'https://www.goodreads.com/list/show/2096.Espionage'

scrape(log_in(), start_url, table_name)
