from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
client = app.test_client()
engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):

        result = engine.execute(f"select * from Company_data where name_ = '{str(u_path).upper()}'")
        serialized = []
        for item in result:
            serialized.append({item.Date_: {"id": item.id, "name": item.name_, "open": item.Open_, "High": item.High,
                                          "Low": item.Low, "Close": item.Close_, "Adj Close": item.Adj_Close,
                                          "Volume": item.Volume, }})
        if len(serialized) > 0:
            print(type(jsonify(serialized)))
            return jsonify(serialized)
        if len(serialized) == 0 and len(str(u_path)) == 0:
            return "way of using:  url\\companyname"
        else:
            return "Nothing to show"

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)
