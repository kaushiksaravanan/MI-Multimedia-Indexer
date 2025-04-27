from flask import Flask, render_template
import pandas as pd

def make_clickable(val):
    return f'<a href="{val}">{val}</a>'

app = Flask(__name__)

@app.route("/")
def table():
    data_dic = {
        'id': [100, 101, 102],
        'color': ['red', 'blue', 'red'],
        'url':['https://www.softhints.com', 'https://datascientyst.com','https://google.com']
        }
    # dictionary
    columns = ['id', 'color','url']
    columnNames=columns
    index = ['a', 'b', 'c']
    df = pd.DataFrame(data_dic, columns=columns, index=index)
    # df.style.format(make_clickable)
    # df['url'] = df.apply(lambda x: make_clickable(x['url']), axis=1)
    table = df.to_html(index=True,render_links=True, escape=False)
    temp = df.to_dict('records')
    return render_template("record.html",records=temp, colnames=columnNames)

if __name__ == "__main__":
    app.run(debug=True)