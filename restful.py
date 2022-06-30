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
# from contextlib import closing
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from waitress import serve
from main import Scraper
from settings import *


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})
scraper = Scraper()


class Plex(Resource):
	def get(self):
		# Gets search results from a search term
		parser = reqparse.RequestParser()
		parser.add_argument("search_term", required=True, type=str, location="args")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		data = scraper.search(
				args["search_term"]
			)

		if data == 404 or not data:
			return {"message": "Page not found"}, 404
		return {"message": data}, 200

	def post(self):
		# Adds media to the server
		parser = reqparse.RequestParser()
		parser.add_argument("search_term", required=True, type=str, location="args")
		parser.add_argument("result_data", required=False, type=str, location="args")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		url = scraper.get_video_url_from_page_link(
				args["search_term"]
			)

		if url == 404:
			return {"message": "Page not found"}, 404
		return {"message": url}, 200

class Sample(Resource):
	def get(self):
		return {"message": "Not implemented"}, 501

	def post(self):
		return {"message": "Not implemented"}, 501


def main():
	# plexserver.ga:8080/sample
	api.add_resource(Plex, "/plex")
	api.add_resource(Sample, "/sample")
	serve(app, host=HOST, port=PORT)
	# app.run()


if __name__ == "__main__":
	main()
