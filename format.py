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
import os
import json

from tmdbv3api import TMDb, Search

from settings import *
from regions import regions


tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY
tmdb.language = "en"


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

def contains_only_letters(data):
	matches = re.findall(r"[^a-zA-Z]+", data)
	return not bool(matches)

def find_show_title_from_tv_show(data):
	show_title = re.sub(r"(\s-\sSeason\s\d)(?!.*\s-\sSeason\s\d).*", "", data)
	return show_title

def find_episode_title_from_tv_show(data):
	episode_title = re.sub(r".*(\sEpisode\s\d+\s)(?!.*\sEpisode\s\d+\s)", "", data)
	return episode_title

def find_season_number_from_tv_show(data):
	season_number = \
		re.findall(
			r"(\d+)$",
			re.findall(
				# r"(.+)(?=\s-\sSeason\s\d)",
				r"(\s-\sSeason\s\d)(?!.*\s-\sSeason\s\d)",
				data
			)[-1]
		)[0]
	if len(season_number) < 2:
		season_number = "0"+ season_number
	return season_number

def find_episode_number_from_tv_show(data):
	# print(data)
	episode_number = \
		re.findall(
			r"(\d+)$",
			re.findall(
				r"(\sEpisode\s\d+)(?!.*\sEpisode\s\d+)",
				data
			)[-1]
		)[0]
	if len(episode_number) < 2:
		episode_number = "0"+ episode_number
	return episode_number


class Format:
	def __init__(self, result):
		# print(url)
		# print(result)
		self.result = json.loads(result)  # Convert str to dict
		self.url = self.result["url"]
		self.data = self.result["data"]
		self.title = self.result["title"]
		self.release_year = self.data["release_year"]
		# self.imdb_score = self.data["imdb_score"]
		# self.duration = self.data["duration"]
		self.release_country = self.data["release_country"]
		# self.genre = self.data["genre"]
		# self.description_preview = self.data["description_preview"]
		# self.key = self.data["key"]
		# self.quality_tag = self.data["quality_tag"]
		# self.user_rating = self.data["user_rating"]
		if "/watch-film/" in self.url and "/watch-tv-show/" not in self.url:
			self.type = "MOVIE"
		elif "/watch-tv-show/" in self.url and "/watch-film/" not in self.url:
			is_episode = self.url.endswith("-online-for-free.html")  # True/False
			self.type = "TV SHOW", is_episode
		else:
			self.type = "MISC"

	def format_file_name(self, bad_characters="<>:\"/\\|?*"):
		# File system safe title formatting removes reserved and non-ascii characters
		search = Search()
		region = regions[self.release_country]
		safe_title = re.sub(f"[{bad_characters}]", "", self.title).encode("ascii", "ignore").decode()
		# print(self.title, safe_title)
		match self.type:
			case "MOVIE":
				query = {
					"query": safe_title,
					"primary_release_year": self.release_year,
					"region": region,
				}

				tmdb_results = search.movies(query)
				tmdb_id = str(tmdb_results[0]["id"])# if tmdb_results else False

				safe_title = (
					safe_title if re.match(
						r"^.*?\([^\d]*(\d+)[^\d]*\).*$", safe_title
					) else f"{safe_title} ({self.release_year})"
				)

				safe_title = safe_title +" {tmdb-"+ tmdb_id +"}"
				file_path = os.path.join(ROOT_LIBRARY_LOCATION, f"MOVIES/{safe_title}/{safe_title}.mp4")
			case "TV SHOW", is_episode:
				show_title = find_show_title_from_tv_show(safe_title)
				query = {
					"query": show_title,
					"first_air_date_year": self.release_year,
				}
				# print(query)
				tmdb_results = search.tv_shows(query)
				tmdb_id = str(tmdb_results[0]["id"]) if tmdb_results else False
				if not tmdb_id: print(f"ERROR: No TMDb results for query: {query}")

				show_title = (
					show_title if re.match(
						r"^.*?\([^\d]*(\d+)[^\d]*\).*$", show_title
					) else f"{show_title} ({self.release_year})"
				)
				season_number = find_season_number_from_tv_show(safe_title)
				file_path = os.path.join(
					ROOT_LIBRARY_LOCATION,
					f"TV Shows/{show_title +' {tmdb-'+ tmdb_id +'}' if tmdb_id else ''}/Season {season_number}"
				)
				if is_episode:
					episode_number = find_episode_number_from_tv_show(safe_title)
					episode_title = find_episode_title_from_tv_show(safe_title)
					file_path = os.path.join(
						file_path,
						f"{show_title} - s{season_number}e{episode_number} - {episode_title}.mp4"
					)
			case _:
				pass  # Error?

		count = len(tmdb_results)
		print(f"\tFound {count} {'result' if count == 1 else 'results'} for TMDb lookup.")
		return file_path

	def run(self):
		print(f"DEBUG: {self.format_file_name()}")


def main():
	file_name = Format('{"title":"Star Wars: Episode IX - The Rise of Skywalker","poster_url":"https://static.gomovies-online.cam/dist/img/C97to1aFchTRotSn63m3yc6k-oA7ou6anY3ruU8Lf2WevlTvJjQks5i_z5fTnadgcYV7z9aVPQcKUVsAxMzkDleaTjfFbze08mdub0ZTXuq3y0XxXiUGmfEQFgfeMfN-.jpg","url":"https://gomovies-online.cam/watch-film/star-wars-episode-ix-the-rise-of-skywalker/dz7sghqt","data":{"title":"Star Wars: Episode IX - The Rise of Skywalker","release_year":"2019","imdb_score":"IMDb: 6.5","duration":"141 min","release_country":"United States","genre":"Action, Adventure, Fantasy","description_preview":"An action movie that presents another story of the epic films series, Star Wars. This film continues with the events of The Last Jedi (2017). The...","key":"0","quality_tag":"HD","user_rating":"3.138890"}}')
	# file_name = Format('{"title":"The Lord of the Rings: The Rings of Power - Season 1","poster_url":"https://static.gomovies-online.cam/dist/img/_6CcL186P_Wy8TqINYCpv1vQlGZwG8GXTBxUUaWrejiI-K0wsXfLv1anrsfCNZa1E2PlY5giii9QK0441PQ_TZoOBqLiP7OR28gd2UUtKqBXSfHdwrRMYFPAkdQIIuww.jpg","url":"https://gomovies-online.cam/watch-tv-show/the-lord-of-the-rings-the-rings-of-power-season-1/Dok6Ozoc","data":{"title":"The Lord of the Rings: The Rings of Power - Season 1","release_year":"2022","imdb_score":"IMDb: 6.9","duration":"90 min","release_country":"United States","genre":"Drama, Action, Adventure","description_preview":"Epic drama set thousands of years before the events of J.R.R. Tolkien\'s \'The Hobbit\' and \'The Lord of the Rings\' follows an ensemble cast of...","key":"0","quality_tag":"HD","user_rating":"4.000000"}}')
	# file_name = Format('{"title":"John Adams - Season 1","poster_url":"https://static.gomovies-online.cam/dist/img/ZxbUx78gfmcmfZJK6HUKzq6Uc1um2ts3wz9XlD3a-yUgMoK1AaNmYqRAXBeuPJjXk_nZhodkYTIN9Wv_USV7ypr2MWUUsZKw0XaGOoJak-02pMsapG3mGeBQuKxpZnPQ.jpg","url":"https://gomovies-online.cam/watch-tv-show/john-adams-season-1/amA2Zf8B","data":{"title":"John Adams - Season 1","release_year":"2008","imdb_score":"IMDb: 8.5","duration":"71 min","release_country":"United States","genre":"Drama, Biography, History","description_preview":"The life of one of the USA\'s Founding Fathers, its second President, and his role in the nation\'s first 50...","key":"0","quality_tag":"HD","user_rating":"0.000000"}}')
	# file_name = Format('{"title":"House of the Dragon - Season 1 Episode 04: King of the Narrow Sea","poster_url":"https://static.gomovies-online.cam/dist/img/JwcIcm8LmF3N-dxSG-TYdejY60yMncaAQNO_jiedtvGAb5Fox1e_gcAWDJWuCAEYBTQz9hXPyn1ki90-FyAHXRCDimczv6xpDbrT9RO6qEliqnLjBm9-pwQvd4-xwH07.jpg","url":"https://gomovies-online.cam/watch-tv-show/house-of-the-dragon-season-1/1tiQ2oUp/tWUDFo8X/cIECTfeF-online-for-free.html","data":{"title":"House of the Dragon - Season 1 Episode 04: King of the Narrow Sea","release_year":"2022","imdb_score":"8.8","duration":"90 min","release_country":"United States","genre":"Adventure","description_preview":"The story of the House Targaryen set 200 years before the events of Game of Thrones...","quality_tag":"HD","user_rating":"4.71428","key":"0"}}')
	file_name.run()


if __name__ == "__main__":
	main()
