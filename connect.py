import pymysql
import pandas as pd


def get_data(table_name, password='6456456456456456-*-*/hfd -*-/*-gd*//>?[gdfg', host='127.0.0.1', user='root'):
    conn = pymysql.connect(host=host, user=user,
                           passwd=password, db='mysql')
    cur = conn.cursor()
    cur.execute('USE goodreads')
    data = pd.read_sql(f'SELECT * FROM {table_name}', conn)
    return data





