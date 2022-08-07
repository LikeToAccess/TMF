# -*- coding: utf-8 -*-
# filename          : format.py
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
import json


# {
#   "title": "Star Wars: Episode IX - The Rise of Skywalker",
#   "poster_url": "https://static.gomovies-online.cam/dist/img/C97to1aFchTRotSn63m3yc6k-oA7ou6anY3ruU8Lf2WevlTvJjQks5i_z5fTnadgcYV7z9aVPQcKUVsAxMzkDleaTjfFbze08mdub0ZTXuq3y0XxXiUGmfEQFgfeMfN-.jpg",
#   "url": "https://gomovies-online.cam/watch-film/star-wars-episode-ix-the-rise-of-skywalker/dz7sghqt",
#   "data": {
#     "title": "Star Wars: Episode IX - The Rise of Skywalker",
#     "release_year": "2019",
#     "imdb_score": "IMDb: 6.5",
#     "duration": "141 min",
#     "release_country": "United States",
#     "genre": "Action, Adventure, Fantasy",
#     "description_preview": "An action movie that presents another story of the epic films series, Star Wars. This film continues with the events of The Last Jedi (2017). The...",
#     "key": "0",
#     "quality_tag": "HD",
#     "user_rating": "3.138890"
#   }
# }

# def filter_bad_characters(data, ):
# 	return re.sub(bad_characters, "", data).encode("ascii", "ignore").decode()

class Format:
	def __init__(self, result):
		# print(url)
		# print(result)
		self.result = json.loads(result)  # Convert str to dict
		self.url = self.result["url"]
		self.data = self.result["data"]
		self.title = self.result["title"]
		self.release_year = self.data["release_year"]
		# self.imdb_score = data["imdb_score"]
		# self.duration = data["duration"]
		# self.release_country = data["release_country"]
		# self.genre = data["genre"]
		# self.description_preview = data["description_preview"]
		# self.key = data["key"]
		# self.quality_tag = data["quality_tag"]
		# self.user_rating = data["user_rating"]
		if "/watch-film/" in self.url and "/watch-tv-show/" not in self.url:
			self.type = "MOVIE"
		elif "/watch-tv-show/" in self.url and "/watch-film/" not in self.url:
			self.type = "TV SHOW"
		else:
			self.type = "MISC."

	def format_file_name(self, bad_characters="<>:\"/\\|?*"):
		# File system safe title formatting removes reserved and non-ascii characters
		safe_title = re.sub(f"[{bad_characters}]", "", self.title).encode("ascii", "ignore").decode()
		if self.type == "MOVIE":
			safe_title = (
				safe_title if re.match(
					r"^.*?\([^\d]*(\d+)[^\d]*\).*$", safe_title
				) else f"{safe_title} ({self.release_year})"
			)
			safe_title = f"../MOVIES/{safe_title}/{safe_title}.mp4"
		elif self.type == "TV SHOW":
			pass  # TV Show
		else:
			pass  # Error?

		# print(safe_title)
		return safe_title

	def run(self):
		print(self.format_file_name())


def main():
	file_name = Format("https://stream-1-1-ip4.loadshare.org/slice/2/VideoID-gjQ7xn1d/phmP3r/HZ7zrT/Bv5yvD/DjeAzU/2160?name=star-wars-episode-ix-the-rise-of-skywalker_2160&token=ip=75.168.217.234~st=1656919823~exp=1656934223~acl=/*~hmac=43b494990743941044eb168c7b8ed47e3e93875007cac2a8509a30824678b1c8", '{"title":"Star Wars: Episode IX - The Rise of Skywalker","poster_url":"https://static.gomovies-online.cam/dist/img/C97to1aFchTRotSn63m3yc6k-oA7ou6anY3ruU8Lf2WevlTvJjQks5i_z5fTnadgcYV7z9aVPQcKUVsAxMzkDleaTjfFbze08mdub0ZTXuq3y0XxXiUGmfEQFgfeMfN-.jpg","url":"https://gomovies-online.cam/watch-film/star-wars-episode-ix-the-rise-of-skywalker/dz7sghqt","data":{"title":"Star Wars: Episode IX - The Rise of Skywalker","release_year":"2019","imdb_score":"IMDb: 6.5","duration":"141 min","release_country":"United States","genre":"Action, Adventure, Fantasy","description_preview":"An action movie that presents another story of the epic films series, Star Wars. This film continues with the events of The Last Jedi (2017). The...","key":"0","quality_tag":"HD","user_rating":"3.138890"}}')
	file_name.run()


if __name__ == "__main__":
	main()
