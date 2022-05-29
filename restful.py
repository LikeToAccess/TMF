# -*- coding: utf-8 -*-
# filename          : restful.py
# description       : API to grab movie links
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 05-24-2022
# version           : v1.0
# usage             : python restful.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
from contextlib import closing
from flask import Flask
from flask_restful import Resource, Api, reqparse
from waitress import serve


app = Flask(__name__)
api = Api(app)


class Users(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("email", required=False, type=str, location="args")
		parser.add_argument("name", required=False, type=str, location="args")
		args = parser.parse_args()
		if args:
			return {"message": "Movie link"}, 200

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("name", required=True, type=str, location="args")
		parser.add_argument("email", required=True, type=str, location="args")
		parser.add_argument("profile_picture", required=False, type=str, location="args")
		args = parser.parse_args()

		print("Succesful 200 in POST request: New user created")
		return {"message": "New user created"}, 200

class Sample(Resource):
	def get(self):
		return {"message": "Not implemented"}, 501

	def post(self):
		return {"message": "Not implemented"}, 501


def main():
	# plexserver.ga:8080/sample
	api.add_resource(Users, "/users")
	api.add_resource(Sample, "/sample")
	serve(app, host="0.0.0.0", port=8080)
	# app.run()


if __name__ == "__main__":
	main()
