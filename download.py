import os
import wget
import time
import requests
from requests.exceptions import *
from file import *


url = "https://stream-1-1-ip4.loadshare.org/slice/1/VideoID-J0jblDNB/ZgHnoD/Rf9KYb/JJwZ9U/yw6vyb/1080?name=booksmart_1080&token=ip=12.191.26.4~st=1659584599~exp=1659598999~acl=/*~hmac=14c16c1e608e6275c1201c3ffc6e67410bfdc4565a90250c42844dcb4394fb2a"
destination = "TEST/movie.mp4"


def download_with_wget(url, destination, bar=None):
	wget.download(url, destination, bar=bar)

def verify_path(destination):
	if not os.path.exists(os.path.dirname(destination)):
		os.makedirs(os.path.dirname(destination))
		return False
	return True

def verify_file(destination):
	return os.path.exists(destination)

def create_request(url):
	print("Creating request...")
	connection_timout = 10
	read_timeout = 60
	headers = {
		"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
	}

	try:
		request = requests.get(
			url,
			headers=headers,
			stream=True,
			timeout=(connection_timout, read_timeout)
		)
	except ConnectionError:  # URL is offline or Server is IP banned
		request = None

	return request

class Download:
	def __init__(self, url, destination):
		self.url = url
		self.destination = destination
		self.chunk_size = 8*1024*1024  # 8.00 MB
		self.minimum_file_size = 10*1024*1024  # 10.00 MB
		self.request = create_request(url)
		self.target_size = None

		print(f"\tRequest status code: {self.request.status_code}.")

	def run(self):
		self.target_size = int(self.request.headers.get("content-length", 0))
		url_download_timestamp = time.time()
		path_already_exists = verify_path(self.destination)
		file_already_exists = verify_file(self.destination)
		print("\tWARNING: File already exists!\n" if file_already_exists else "", end="")
		print(f"\tDownloading {round(self.target_size/1024/1024,2)} MB...")
		with open(self.destination +".crdownload", "wb") as file:
			for count, chunk in enumerate(self.request.iter_content(chunk_size=self.chunk_size)):
				file.write(chunk)
				# progress.file_size(
				# 	self.filename,
				# 	count,
				# 	url_download_timestamp,
				# 	target_size=self.target_size
				# )
				# time.sleep(0.01)
		# 		percentage_complete = count * self.chunk_size / target_size * 100
		# 		if round(percentage_complete, 1) % 2.5 == 0:
		# 			print(f"{round(percentage_complete)}%")
		# print(f"100%")
		rename_file(self.destination +".crdownload", self.destination)
		print(f"\tCompleted download in {round(time.time()-url_download_timestamp,2)}s.")


	def verify(self):
		print("Verifying current download...")
		file_size = os.path.getsize(self.destination)

		if file_size != self.target_size:  # File must match the target file size
			print("\tERROR: File size does not match!")
			rename_file(self.destination, self.destination +".crdownload")
			return False
		if file_size <= self.minimum_file_size:  # File must be larger than 10.00 MB
			print(f"\tERROR: File size is too small! (< {self.minimum_file_size} Bytes)")
			rename_file(self.destination, self.destination +".crdownload")
			return False

		print("\tFile size match OK.\n\tVerification passed.")
		return True


def main():
	download = Download(url, destination)
	download.run()
	download.verify()


if __name__ == "__main__":
	main()
