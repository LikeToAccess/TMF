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
import time
import json
import platform
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
# from tqdm import tqdm
from settings import *


OS = platform.system()


def remove_file(filename):
	try:
		os.remove(filename)
		return True
	except OSError:
		return False

def read_file(filename, encoding="utf8"):
	if not os.path.exists(filename): return filename
	with open(filename, "r", encoding=encoding) as file:
		data = file.read()

	return data

def write_file(filename, data, encoding="utf8"):
	with open(filename, "w", encoding=encoding) as file:
		file.write(data)

def read_json_file(filename, encoding="utf8"):
	if not os.path.exists(filename): return []
	with open(filename, "r", encoding=encoding) as file:
		data = json.load(file)

	return data

def write_json_file(filename, data, encoding="utf8"):
	with open(filename, "w", encoding=encoding) as file:
		json.dump(data, file, indent=4, sort_keys=True)

	return pretty_print_json(data)

def append_json_file(filename, data, encoding="utf8"):
	existing_data = read_json_file(filename, encoding=encoding)
	existing_data.append(data)
	write_json_file(filename, existing_data, encoding=encoding)

def pretty_print_json(data):
	return json.dumps(data, indent=4, sort_keys=True)


class Scraper:
	def __init__(self):
		self.begin_init_timestamp = time.time()
		options = Options()
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument(f"user-data-dir={user_data_dir}")
		options.add_argument("log-level=3")
		if HEADLESS:
			options.add_argument("--headless")
			options.add_argument("--disable-gpu")
		self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
		# self.driver.minimize()
		print("Init finished")

	def wait_until_element(self, selector, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		element = wait.until(
			EC.presence_of_element_located(
				(
					selector, locator
				)
			)
		)
		return element

	def wait_until_elements(self, selector, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		elements = wait.until(
			EC.presence_of_all_elements_located(
				(
					selector, locator
				)
			)
		)
		return elements

	def find_element(self, selector, sequence):
		return self.driver.find_element(selector, sequence)

	def find_elements(self, selector, sequence):
		return self.driver.find_elements(selector, sequence)

	def wait_until_element_by_xpath(self, sequence, timeout=10):
		return self.wait_until_element(By.XPATH, sequence, timeout=timeout)

	def wait_until_elements_by_xpath(self, sequence, timeout=10):
		return self.wait_until_elements(By.XPATH, sequence, timeout=timeout)

	def find_element_by_xpath(self, sequence):
		return self.find_element(By.XPATH, sequence)

	def find_elements_by_xpath(self, sequence):
		return self.find_elements(By.XPATH, sequence)

	def open_link(self, url):
		self.driver.get(url)

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def refresh(self):
		self.driver.refresh()

	def find_subtitles_source(self):
		sequence = "/html/body/main/div/div/section/div[3]/div/script[2]/text()"
		element = self.find_element_by_xpath(sequence)
		print(element.text)
		# source = element.get_attribute("src")
		#/html/body/main/div/div/section/div[3]/div/script[2]/text()

	def find_video_source(self):
		pass
		#//*[@id="_skqeqEJBSrS"]/div[2]/video

	def current_page_is_404(self):
		try:
			if self.find_element_by_xpath("//*[@id='_sKnoHaKJFse']/div[1]/h1/p[1]").text == "404":
				return True
		except NoSuchElementException:
			pass

		return False

	def resume_video(self):
		self.driver.execute_script(
			"videos = document.querySelectorAll('video'); for(video of videos) {video.play()}"
		)

	def pause_video(self):
		self.driver.execute_script(
			"videos = document.querySelectorAll('video'); for(video of videos) {video.pause()}"
		)

	def search_by_title(self, search_term):
		self.open_link(f"https://gomovies-online.cam/search/{search_term}")

		if self.current_page_is_404():
			print("ERROR: Page error 404!\n")
			return self.search_by_title(search_term)

		results_data = []
		results = self.find_elements_by_xpath("//*[@class='item_hd']") + \
				  self.find_elements_by_xpath("//*[@class='item_sd']") + \
				  self.find_elements_by_xpath("//*[@class='item_cam']") + \
				  self.find_elements_by_xpath("//*[@class='item_series']")
		for result in results:
			# Title
			title = result.text
			# Poster
			poster_url = result.find_element(by=By.XPATH, value="div/div/img").get_attribute("src")
			# URL
			url = result.get_attribute("href")
			# Other Data
			_data_element = result.find_element(by=By.XPATH, value="..")
			additional_data = {
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

			additional_data["description_preview"] = \
				additional_data["description_preview"].strip(". ").rsplit(" ", 1)[0].strip(".") + "..."
			additional_data["quality_tag"] = \
				additional_data["quality_tag"].replace("itemAbsolute_", "").upper()

			results_data.append(
				{
					"title":           title,
					"poster_url":      poster_url,
					"url":             url,
					"additional_data": additional_data,
				}
			)

			if title != additional_data["title"]:
				print("WARNING: Titles do not match!")
				print(f"\tGot:      '{additional_data['title']}'")
				print(f"\tExpected: '{title}'\n")

		return results_data

	def debug(self):
		while True:
			search_term = input("Enter a movie name to search for:\n> ")

			print("Waiting for search results...")
			begin_search_timestamp = time.time()
			results = self.search_by_title(search_term)
			print(f"Completed search in {round(time.time()-begin_search_timestamp,2)}s,", end=" ")
			print(f"found {len(results)} {'result' if len(results) == 1 else 'results'}.\n")
			# print(pretty_print_json(results))

			wait_for_input()

	def download_from_link(self, link, timeout=30):
		self.open_link(link)
		movie = bool(
			self.find_element_by_xpath(
				"/html/body/main/div/div/section/section/ul/li[2]/div/a"
			).text == "MOVIES"
		)
		current_page_url = self.current_url()
		if movie:
			print("Media is detected as 'MOVIE'.")

			print("Waiting for video to load...")
			current_page_url += "-online-for-free.html"
			self.open_link(current_page_url)

			original_video_url = self.wait_until_element(
				By.TAG_NAME, "video", timeout
			).get_attribute("src")
			print("Video element loaded.")
			print("Resuming content...")
			self.wait_until_element_by_xpath(
				"//*[@id='_skqeqEJBSrS']/div[10]/div[4]/div[2]/div[1]",
				timeout,
			).click()

			# best_premium_quality = self.wait_until_element_by_xpath(
			# 	"//*[@class='changeClassLabel jw-reset jw-settings-content-item']",
			# 	timeout,
			# ).text#.split("p (Premium)")[0]
			# self.wait_until_element_by_xpath("//*[@class='sadhjasdjkASDd']")  # waits for video to load
			# time.sleep(3)
			best_premium_quality = self.find_element_by_xpath(
				"//*[@id='_skqeqEJBSrS']/div[10]/div[3]/div[4]/a[1]/button"
			).text#.split("p (Premium)")[0]
			print(best_premium_quality)

			print("Pausing content...")
			self.pause_video()
		print(current_page_url)
		print(original_video_url)
		#https://gomovies-online.cam/watch-tv-show/batman-the-animated-series-season-1/5kIqZ6LH/yFmPceNC
		#https://gomovies-online.cam/watch-tv-show/batman-the-animated-series-season-1/5kIqZ6LH/gDov772B/yFmPceNC-online-for-free.html

		#https://gomovies-online.cam/watch-film/sonic-the-hedgehog-2/S8efDEgq/NjyHbCra
		#https://gomovies-online.cam/watch-film/sonic-the-hedgehog-2/S8efDEgq/NjyHbCra-online-for-free.html

	def run(self):
		print(f"Completed init in {round(time.time()-self.begin_init_timestamp,2)}s.\n")
		print("Waiting for URL...")
		begin_download_timestamp = time.time()
		self.download_from_link(
			"https://gomovies-online.cam/watch-film/death-on-the-nile/TjWH9YzW/aToNTDyI"
		)
		print(f"Completed download in {round(time.time()-begin_download_timestamp,2)}s.\n")

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
