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
import os
import json
# import threading

from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from waitress import serve
from flask import Flask

from download import Download
from settings import *
from scraper import Scraper
from format import Format, contains_only_letters


app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}})
scraper = Scraper()
threads = []
# download = Download()


class Queue_Downloads:
	def __init__(self, query, data):
		self.query = query
		self.data = data
		self.queue = []

	def setup(self):
		# TODO: Make TV Shows work
		self.queue, status = scraper.get_video_url_from_page_link(
			self.query
		)

		return status

	def run(self):
		for url in self.queue:
			download = Download(url, Format(self.data).format_file_name())
			download.run()
			# if the media is a TV Show than the data is useless
			if download.verify(): return {"message": "Created", "data": self.data}, 201
			return {"message": "Gone (failure to verify)"}, 410

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

		qd = Queue_Downloads(args["query"], args["data"])
		status = qd.setup()

		if status == 404:
			return {"message": "Page not found"}, 404
		if status == 225:
			image_data = base64.b64encode(open("captcha.png", "rb").read()).decode("utf-8")
			image_data = f"data:image/png;base64,{image_data}"
			return {"message": "CAPTCHA", "data": image_data}, 225

		return qd.run()

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
		if not os.path.exists("captcha.png"):
			return {"message": "File not found"}, 404
		image_data = base64.b64encode(open("captcha.png", "rb").read()).decode("utf-8")
		image_data = f"data:image/png;base64,{image_data}"
		return {"message": "CAPTCHA", "data": image_data}, 225

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("key", required=True, type=str, location="args")
		parser.add_argument("result", required=False, type=str, location="json")
		args = parser.parse_args()
		if not args:
			return {"message": "Bad request"}, 400

		key = args["key"]
		if not contains_only_letters(key):
			return {"message": "Bad request (CAPTCHA contains only uppercase letters)"}, 400

		# if args["result"]:
		# 	result = json.loads(args["result"].replace("'" ,'"'))
		# 	print(json.dumps(result, indent=4))

		captcha_is_resolved = scraper.resolve_captcha(key)
		print(f"CAPTCHA is solved? ({captcha_is_resolved})")
		if not captcha_is_resolved:
			return {"message": "Bad request (CAPTCHA is incorrect)"}, 400
		return {"message": "OK (CAPTCHA resolved)"}, 200


def main():
	api.add_resource(Search, "/search")
	api.add_resource(Test, "/test")
	api.add_resource(Catagory, "/catagory")
	api.add_resource(Captcha, "/captcha")
	serve(app, host=HOST, port=PORT)
	# For debugging only!
	# app.run(host=HOST, port=PORT, debug=True)


if __name__ == "__main__":
	main()
