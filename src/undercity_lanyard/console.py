from . import __version__, cleanup, init, create_badge, flash_badge  # noqa
import requests
import os
import shutil


def main():
	cleanup()
	init()

	name = input("Enter the name of the badge: ")
	if not name:
		print("Name is required.")
		exit(1)
	print(f"Hola: {name}")
	slack_handle = input("Enter the Slack handle: ")
	if not slack_handle:
		print("Slack handle is required.")
		exit(1)

	print(f"Hey: {slack_handle}! Nice to meet you!")

	extra = input("Enter any text you want to add: ")

	if not extra:
		print("No additional text provided.")

	img_mode = input("Image mode? (file/url/NONE): ").strip().lower() + " "
	if img_mode[0] == "f":
		img = input("Enter the path to the image file: ")
		if not os.path.exists(img):
			print("Image file does not exist.")
			img = None
		else:
			shutil.copy(img, "img.png")
	elif img_mode[0] == "u":
		img = input("Enter the url to the image: ")
		response = requests.get(img)
		if response.status_code == 200:
			with open("img.png", "wb") as f:
				f.write(response.content)
		else:
			print("Failed to download image.")
			img = None
	else:
		img = None

	create_badge(name, slack_handle, extra, img)
	flash_badge()

	cleanup()
