from flask import Flask, redirect
import pandas as pd
import pygsheets

app = Flask(__name__)
gc = pygsheets.authorize()

table_url = "https://docs.google.com/spreadsheets/d/1yulX7BjPw_PC1Wc1BUEICvRKdWnPKpwV83dRRGsZXyM/edit#gid=0"


def grabber(url):
    sh = gc.open_by_url(url)
    main_sheet = sh.sheet1
    return main_sheet


@app.route('/report')
def report():
    wks = grabber(table_url)

    data = wks.get_as_df()

    table_len = len(data)

    # data.iloc[0, data.columns.get_loc('cumsum')] = 100

    data.at[0, 'cumsum'] = data['spend'][0]

    # filling cumsum
    for i in range(1, table_len, 1):
        data.at[i, 'cumsum'] = data['cumsum'][i - 1] + data['spend'][i]
        if i <= 3:
            data.at[i - 1, 'last3d'] = data.at[i - 1, 'cumsum']
        if i <= 7:
            data.at[i - 1, 'last7d'] = data.at[i - 1, 'cumsum']

    # filling last3d
    for i in range(3, table_len, 1):
        data.at[i, 'last3d'] = data['spend'][i - 1]
        for n in range(2, 4, 1):
            data.at[i, 'last3d'] += data['spend'][i - n]

    # filling last7d
    for i in range(7, table_len, 1):
        data.at[i, 'last7d'] = data['spend'][i - 1]
        for n in range(2, 8, 1):
            data.at[i, 'last7d'] += data['spend'][i - n]

    data_html = pd.DataFrame.to_html(data)

    return data_html


@app.route('/')
def index():
    return redirect('report')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
