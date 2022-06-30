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
class Download:
	def __init__(self):
		pass

	def format_filename(self):
		filename = (f"{filmname} ({year})" if filmname[-1] != ")" else filmname)


def main():
	download = Download()


if __name__ == "__main__":
	main()
