from flask import Flask, render_template, redirect
import pandas as pd
import pygsheets

app = Flask(__name__)

gc = pygsheets.authorize()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1A3xQOY8P0juEfEf_xMXkMs-zXPu3R6FPdCylmM7nSJI/edit#gid=0')
wks = sh.sheet1

df = wks.get_as_df()


@app.route('/report')
def about():
    data = pd.DataFrame.to_html(df)
    return data


@app.route('/')
def index():
    return redirect('report')


if __name__ == "__main__":
    app.run(debug=True, port=3000)

