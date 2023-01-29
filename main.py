from dash import Dash, dcc, html, Input, Output, dash_table
import pymysql
import pandas as pd

app = Dash(__name__)


conn = pymysql.connect(host='127.0.0.1', user='root',
                       passwd='6456456456456456-*-*/hfd -*-/*-gd*//>?[gdfg', db='mysql')
cur = conn.cursor()
cur.execute('USE goodreads')
cur.execute('SHOW TABLES;')

table_names = cur.fetchall()[0]
options = []
values = []

for name in table_names:
    data = pd.read_sql(f'SELECT * FROM {name}', conn)
    col_names = data.columns
    values = [data.loc[i].to_dict() for i in range(len(data))]

    options.append({
        "label": name,
        "value": values
    })

cur.close()
conn.close()


car_sharing_data = pd.read_json('https://raw.githubusercontent.com/plotly/datasets/master/carshare_data.json')
iris_data = pd.read_json('https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json')

iris_data = [iris_data.loc[i].to_dict() for i in range(len(iris_data))]
print(values)

app.layout = html.Div(
    [
        dcc.Dropdown(
            options=[
                {
                    "label": "Car-sharing data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/carshare_data.json",
                },
                {
                    "label": "Iris data",
                    "value": "https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
                },
            ],
            value="https://raw.githubusercontent.com/plotly/datasets/master/iris_data.json",
            id="data-select",
        ),
        html.Br(),
        dash_table.DataTable(id="my-table-promises", page_size=10),
    ]
)

app.clientside_callback(
    """
    async function(value) {
    const response = await fetch(value);
    const data = await response.json();
    return data;
    }
    """,
    Output("my-table-promises", "data"),
    Input("data-select", "value"),
)

if __name__ == "__main__":
    app.run_server(debug=True)
