import pandas as pd
from connect import get_data

books = get_data('books')
print(books['Summary'])