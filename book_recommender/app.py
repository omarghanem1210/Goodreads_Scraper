from scraper import scrape, log_in

driver = log_in()
book_data = scrape(driver, 'https://www.goodreads.com/review/list/135265628-omar-ghanem%20&ref=nav_mybooks&shelf=read')