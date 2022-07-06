# -*- coding: utf-8 -*-
# filename          : find_captcha.py
# description       : Class containing methods for finding elements
# author            : Ian Ault
# email             : liketoaccess@protonmail.com
# date              : 05-19-2022
# version           : v1.0
# usage             : python main.py
# notes             : This file should not be run directly
# license           : MIT
# py version        : 3.10.2
#==============================================================================
import os
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from wait_until_element import Wait_Until_Element
from find_element import Find_Element


class Find_Captcha(Find_Element, Wait_Until_Element):
	def check_captcha(self):
		# "Myles" - Myles
		# "Liam" - Liam
		try:
			captcha_image = self.wait_until_element(
				By.XPATH,
				"//*[@id=\"checkcapchamodelyii-captcha-image\"]",
				timeout=1.5
			)
			captcha_input = self.driver.find_element(By.XPATH, "//*[@id=\"checkcapchamodelyii-captcha\"]")
			captcha_submit = self.driver.find_element(By.XPATH, "//*[@id=\"player-captcha\"]/div[3]/div/div")
		except TimeoutException:
			return False

		return captcha_image, captcha_input, captcha_submit

	def get_captcha_image(self):
		captcha = self.check_captcha()
		if captcha:
			print("\tWARNING: Found captcha!")
			captcha_image, *_ = captcha
			captcha_image.screenshot("captcha.png")
			return 225
		return 200

	def resolve_captcha(self):
		captcha = self.check_captcha()
		while captcha:
			captcha_image, captcha_input, captcha_submit = captcha
			print("\tWARNING: Found captcha!")
			try:
				captcha_image.screenshot("captcha.png")
				captcha_input.send_keys(input("\t\tSolve Captcha:\n\t\t> "))
				captcha_submit.click()
			except WebDriverException:
				os.remove("captcha.png")
				break

			self.wait_until_element(
				By.TAG_NAME, "video", timeout=3
			).get_attribute("src")
			captcha = self.check_captcha()
