import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_data():
    data = pd.read_excel('data.xlsx')
    records = data.to_dict(orient='records')
    return jsonify(records)


if __name__ == '__main__':
    app.run()