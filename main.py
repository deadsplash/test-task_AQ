from flask import Flask, redirect
import pandas as pd
import pygsheets

app = Flask(__name__)
gc = pygsheets.authorize()

# test task 1 url:
# table_url = 'https://docs.google.com/spreadsheets/d/1A3xQOY8P0juEfEf_xMXkMs-zXPu3R6FPdCylmM7nSJI/edit#gid=0'

# test task 2 url
table_url = "https://docs.google.com/spreadsheets/d/1yulX7BjPw_PC1Wc1BUEICvRKdWnPKpwV83dRRGsZXyM/edit#gid=0"


def grabber(url):
    sh = gc.open_by_url(url)
    main_sheet = sh.sheet1
    return main_sheet


@app.route('/report')
def report():

    wks = grabber(table_url)

    df = wks.get_as_df()
    data = pd.DataFrame.to_html(df)
    return data


@app.route('/')
def index():
    return redirect('report')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
