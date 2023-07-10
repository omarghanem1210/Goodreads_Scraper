from dash import Dash, dcc, html, Input, Output, dash_table
import pymysql
import pandas as pd

app = Dash(__name__)

conn = pymysql.connect(host='127.0.0.1', user='root',
                       passwd='', db='mysql')
cur = conn.cursor()
cur.execute('USE goodreads')
cur.execute('SHOW TABLES;')

table_names = cur.fetchall()[0]
options = []
table_data = []
i = 0

for name in table_names:
    data = pd.read_sql(f'SELECT * FROM {name}', conn)
    col_names = data.columns
    table_data.append([data.loc[i].to_dict() for i in range(len(data))])

    options.append({
        "label": name,
        "value": i
    })
    i += 1

cur.close()
conn.close()
"""
car_sharing_data = pd.read_json('https://raw.githubusercontent.com/plotly/datasets/master/carshare_data.json')
iris_data = pd.read_json('https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json')

iris_data = [iris_data.loc[i].to_dict() for i in range(len(iris_data))]
car_sharing_data = [car_sharing_data.loc[i].to_dict() for i in range(len(car_sharing_data))]
data = [car_sharing_data, iris_data]
"""

app.layout = html.Div(
    [
        dcc.Dropdown(
            options=options,
            value=0,
            id='data-select',
        ),
        html.Br(),
        dash_table.DataTable(id='my-table-promises',
                             editable=True,
                             filter_action="native",
                             sort_action="native",
                             sort_mode='multi',
                             row_selectable='multi',
                             row_deletable=True,
                             selected_rows=[],
                             page_action='native',
                             page_current=0,
                             page_size=10, )
    ]
)


@app.callback(
    Output('my-table-promises', 'data'),
    Input('data-select', 'value'),
)
def update_output_div(input_value):
    return table_data[input_value]


if __name__ == "__main__":
    app.run_server(debug=True)
