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
import base64
# import threading

from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from waitress import serve
from flask import Flask

from download import Download
from settings import *
from scraper import Scraper
from format import Format


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})
scraper = Scraper()
threads = []
# download = Download()


class Search(Resource):
	def get(self):
		# Gets search results from a search term
		parser = reqparse.RequestParser()
		parser.add_argument("query", required=True, type=str, location="args")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		data = scraper.search(
				args["query"]
			)

		if data == 404 or not data:
			return {"message": "Page not found"}, 404
		return {"message": data}, 200

	def post(self):
		# Adds media to the server
		parser = reqparse.RequestParser()
		parser.add_argument("query", required=True,  type=str, location="args")
		parser.add_argument("data", required=False, type=str, location="args")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		# TODO: Make TV Shows work
		queue, status = scraper.get_video_url_from_page_link(
				args["query"]
			)
		data = args["data"]  # if the media is a TV Show than the data is useless

		# print(queue)   # URL (list)
		# print(status)  # 200
		# print(data)    # DATA

		if status == 404:
			return {"message": "Page not found"}, 404
		if status == 225:
			image_data = base64.b64encode(open("captcha.png", "rb").read()).decode("utf-8")
			image_data = f"data:image/png;base64,{image_data}"
			return {"message": "Captcha", "data": image_data}, 225

		# download = Download(status, data)

		for url in queue:
			download = Download(url, Format(data).format_file_name())
			download.run()
			if download.verify(): return {"message": "Created", "data": data}, 201
			return {"message": "Gone (failure to verify)"}, 410

class Test(Resource):
	def get(self):
		return {"message": "Not implemented"}, 501

	def post(self):
		return {"message": "Not implemented"}, 501

class Catagory(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("query", required=True, type=str, location="args")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		query = args["query"]
		return {"message": query}, 200

	def post(self):
		return {"message": "Not implemented"}, 501

class Captcha(Resource):
	def get(self):
		return {"message": "Not implemented"}, 501

	def post(self):
		return {"message": "Not implemented"}, 501


def main():
	api.add_resource(Search, "/search")
	api.add_resource(Test, "/test")
	api.add_resource(Catagory, "/catagory")
	api.add_resource(Captcha, "/captcha")
	serve(app, host=HOST, port=PORT)
	# app.run()


if __name__ == "__main__":
	main()
