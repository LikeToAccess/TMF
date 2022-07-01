# -*- coding: utf-8 -*-
# filename          : download.py
# description       : Handle formatting filenames and downloading media
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 06-25-2022
# version           : v1.0
# usage             : python main.py
# notes             : This file should not be run directly
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import re


class Download:
	def __init__(self, url, data):
		print(url)
		print(data)
		self.url = url
		self.data = data
		self.title = data["title"]
		self.release_year = data["release_year"]
		# self.imdb_score = data["imdb_score"]
		# self.duration = data["duration"]
		# self.release_country = data["release_country"]
		# self.genre = data["genre"]
		# self.description_preview = data["description_preview"]
		# self.key = data["key"]
		# self.quality_tag = data["quality_tag"]
		# self.user_rating = data["user_rating"]

	def format_filename(self):
		title = (
			self.title if re.match(
				r"^.*?\([^\d]*(\d+)[^\d]*\).*$", self.title
			) else f"{self.title} ({self.release_year})"
		)

		print(title)
		return title

	def run(self):
		pass


def main():
	download = Download("foo", "bar")
	download.run()


if __name__ == "__main__":
	main()
