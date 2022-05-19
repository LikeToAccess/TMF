# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Respond to GET requests from websites with MP4 links
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 04-25-2022
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import os
import ast
import time
import platform
import jmespath
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from file import *
from settings import *
from find_captcha import Find_Captcha


OS = platform.system()


class Scraper(Find_Captcha):
	def __init__(self):
		init_timestamp = time.time()
		options = Options()
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument("autoplay-policy=no-user-gesture-required")
		options.add_argument("log-level=3")
		options.add_argument(f"user-data-dir={user_data_dir}")
		if HEADLESS:
			options.add_argument("--headless")
			options.add_argument("--disable-gpu")
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		super().__init__(self.driver)
		print(f"Completed init in {round(time.time()-init_timestamp,2)}s.")

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def refresh(self):
		self.driver.refresh()

	def find_video_source(self):
		pass
		#//*[@id="_skqeqEJBSrS"]/div[2]/video

	def current_page_is_404(self):
		try:
			if self.find_element_by_xpath("//*[@id='_sKnoHaKJFse']/div[1]/h1/p[1]").text == "404":
				return True
		except NoSuchElementException:
			pass

		try:
			if self.find_element_by_xpath('//*[@id="oppsBlock"]/span') \
			.get_attribute("innerHTML").strip() == "Oh!":
				return True
		except NoSuchElementException:
			pass

		return False

	def resume_video(self):
		self.driver.execute_script(
			"for(v of document.querySelectorAll('video')){v.setAttribute('muted','');v.play()}"
		)

	def pause_video(self):
		self.driver.execute_script(
			"videos = document.querySelectorAll('video'); for(video of videos) {video.pause()}"
		)

	def get_first_page_link_from_search(self, search_results):
		return search_results[0]["url"] if not isinstance(search_results, int) else search_results

	def find_subtitles_source(self):
		sequence = "/html/body/main/div/div/section/div[5]/div/script[2]"
		element = self.wait_until_element_by_xpath(sequence)
		subtitle_data = ast.literal_eval(
			element.get_attribute("innerHTML").rsplit("window.subtitles = ", 1)[1]
		)
		keys = ["src", "lang"]
		values = [jmespath.search(f"[*].{key}", subtitle_data) for key in keys]
		values = list(zip(values[1],values[0]))

		subtitles = []
		for value in values:
			if value[0] == "en":
				subtitles.append({"lang":value[0], "src":value[1]})

		return subtitles

	def search_by_title(self, search_term, top_result_only=False):
		print("Waiting for search results...")
		search_timestamp = time.time()
		self.open_link(f"https://gomovies-online.cam/search/{search_term}")

		if self.current_page_is_404():
			print("\tERROR: Page error 404!")
			return 404

		try:
			results_data = []
			results = self.find_elements_by_xpath("//*[@class='item_hd']") + \
					  self.find_elements_by_xpath("//*[@class='item_sd']") + \
					  self.find_elements_by_xpath("//*[@class='item_cam']") + \
					  self.find_elements_by_xpath("//*[@class='item_series']") \
					  if top_result_only < 1 else [
					  	  self.find_element_by_xpaths(
					  	  	  "//*[@class='item_hd']",
					  	  	  "//*[@class='item_sd']",
					  	  	  "//*[@class='item_cam']",
					  	  	  "//*[@class='item_series']",
					  	  )]
		except NoSuchElementException:
			return 404

		for result in results:
			# Title
			title = result.text
			# Poster
			poster_url = result.find_element(by=By.XPATH, value="div/div/img").get_attribute("src")
			# URL
			url = result.get_attribute("href")
			# Other Data
			_data_element = result.find_element(by=By.XPATH, value="..")

			search_data = {
				"title":               _data_element.get_attribute("data-filmname"),
				"release_year":        _data_element.get_attribute("data-year"),
				"imdb_score":          _data_element.get_attribute("data-imdb"),
				"duration":            _data_element.get_attribute("data-duration"),
				"release_country":     _data_element.get_attribute("data-country"),
				"genre":               _data_element.get_attribute("data-genre"),
				"description_preview": _data_element.get_attribute("data-descript"),  # Limit is 151 characters
				"star_prefix":         _data_element.get_attribute("data-star_prefix"),
				"key":                 _data_element.get_attribute("data-key"),
				"quality_tag":         _data_element.get_attribute("data-quality"),
				"user_rating":         _data_element.get_attribute("data-rating"),
			}

			search_data["description_preview"], search_data["quality_tag"] = (
				search_data["description_preview"].strip(". ").rsplit(" ", 1)[0].strip(".") + "...",
				search_data["quality_tag"].replace("itemAbsolute_", "").upper()
			)

			results_data.append(
				{
					"title":           title,
					"poster_url":      poster_url,
					"url":             url,
					"search_data":     search_data,
				}
			)

			if title != search_data["title"]:
				print("\tWARNING: Titles do not match!")
				print(f"\t\tGot:      '{search_data['title']}'")
				print(f"\t\tExpected: '{title}'")

		print(f"Completed search in {round(time.time()-search_timestamp,2)}s,", end=" ")
		print(f"found {len(results_data)} {'result' if len(results_data) == 1 else 'results'}.")

		return results_data

	def get_video_url_from_page_link(self, page_link, timeout=30):
		if page_link == 404:
			return 404
		print("Waiting for page to load...")
		get_video_url_timestamp = time.time()
		self.open_link(page_link)
		current_page_url = self.current_url()

		if self.current_page_is_404():
			print("\tERROR: Page error 404!")
			return 404

		movie = bool(
			self.find_element_by_xpath(
				"/html/body/main/div/div/section/section/ul/li[2]/div/a"
			).text == "MOVIES"
		)

		if movie:
			print("\tMedia is detected as 'MOVIE'.")

			print("\tWaiting for video to load... (up to 60 seconds)")
			page_extension = "-online-for-free.html"
			current_page_url += page_extension if not current_page_url.endswith(page_extension) else ""
			self.open_link(current_page_url)
			print("\tChecking for captchas...")
			self.resolve_captchas()

			original_video_url = self.wait_until_element(
				By.TAG_NAME, "video", timeout=60
			).get_attribute("src")
			print("\tVideo loaded.")

			print("\tSleeping...")
			time.sleep(0.5)
			# TODO: Instead of sleeping, this time could be used to get meta data about the movie

			try:
				print("\tWaiting for video resolution list...")
				best_quality = self.wait_until_element_by_xpath(
					"//*[@class='changeClassLabel jw-reset jw-settings-content-item']",
					timeout
				).get_attribute("innerHTML").split("p (")[0]
				print("\tVideo resolution list found.")
			except TimeoutException:
				# TODO: Fallback to old way of verifying resolutions if the above way fails.
				print("\tWARNING: Could not find a resoltion higher than 360p!")
				best_quality = "360"

			self.pause_video()
			print("\tVideo paused.")
		else:
			print("\tMedia is detected as 'TV SHOW'.")
			print("\tWaiting for season page to load...")
			self.open_link(current_page_url)

		print("\tWaiting for subtitles...")
		subtitles = self.find_subtitles_source()
		if subtitles:
			print(f"\tFound {len(subtitles)} English {'subtitle' if len(subtitles) == 1 else 'subtitles'}.")
		else:
			print("\tNo English subtitles available.")

		modified_video_url = original_video_url \
			.replace("/360?name=", f"/{best_quality}?name=") \
			.replace("_360&token=ip=", f"_{best_quality}&token=ip=")

		print(f"\tVideo link converted to {best_quality}p.")
		print(f"Completed all scraping in {round(time.time()-get_video_url_timestamp,2)}s.")

		return modified_video_url, page_link

	def run(self):
		while True:
			url = self.get_video_url_from_page_link(
				self.get_first_page_link_from_search(
					self.search_by_title(
						input("\nEnter movie title:\n> "),
						top_result_only=True
					)
				)
			)

			if url == 404:
				print("ERROR: Page error 404!")
				continue

			print(url[0])

		wait_for_input()


def wait_for_input():
	print()
	if OS == "Windows":  # Only works on Windows
		os.system("pause")
	else:                # Works for MacOS and Linux
		print("Press any key to continue...", end="", flush=True)
		os.system("read -n1 -r")

def main():
	scraper = Scraper()
	scraper.run()
	# scraper.close()


if __name__ == "__main__":
	main()
