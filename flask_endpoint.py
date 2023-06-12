import os

import pandas as pd
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from collector import DataEntry, Base

app = Flask(__name__)
engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@app.route('/', methods=['GET'])
def get_data():
    file_path = 'data.xlsx'

    if os.path.isfile(file_path):
        data = pd.read_excel('data.xlsx')
        records = data.to_dict(orient='records')
        return jsonify(records)

    else:
        try:
            session = DBSession()
            data_entries = session.query(DataEntry).all()
            data = [[entry.date, entry.data] for entry in data_entries]
            session.close()
            return jsonify(data)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app.run()
