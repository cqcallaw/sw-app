""" Main REST API """

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
#from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///demo.db')
app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from users")
        return [{ 'id': i[0], 'name': i[1]} for i in query.cursor.fetchall()]

api.add_resource(Users, '/users')

if __name__ == "__main__":
    app.run()

