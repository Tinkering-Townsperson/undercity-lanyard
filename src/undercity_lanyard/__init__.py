__version__ = "1.3.0"

import os
from pathlib import Path
import sys
import shutil
import subprocess
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont

from undercity_lanyard.bmp_to_array import image_to_c_array


StrOrBytesPath = Union[str, bytes, os.PathLike]


def get_resource(path: StrOrBytesPath):
	"""Return the absolute path of the resource specified by the given path.

	Args:
		path (Path or str): The path of the resource.

	Returns:
		Path: The absolute path of the resource.
	"""

	try:
		if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
			base_path = Path(sys._MEIPASS)
		elif getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS2'):
			base_path = Path(sys.__MEIPASS2)
		else:
			raise AttributeError("Attributes sys.__MEIPASS and sys.__MEIPASS2 do not exist.")
	except AttributeError:
		base_path = Path(__file__).resolve().parent.parent.parent

	base_path = Path(base_path).resolve()
	return (base_path / path).resolve()


def cleanup():  # noqa
	try:
		for f in os.listdir("./build"):
			os.remove(os.path.join("./build", f))
	except FileNotFoundError:
		pass

	try:
		os.remove("img.png")
	except FileNotFoundError:
		pass

	try:
		os.remove("img_resized.png")
	except FileNotFoundError:
		pass

	try:
		os.remove("newbadge.bmp")
	except FileNotFoundError:
		pass

	try:
		os.remove("f.h")
	except FileNotFoundError:
		pass


def init():
	if os.name != 'nt':
		subprocess.run("brew install arduino-cli", shell=True)

	subprocess.run("arduino-cli config add board_manager.additional_urls https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json", shell=True) # noqa

	subprocess.run("arduino-cli core install rp2040:rp2040", shell=True)
	subprocess.run("arduino-cli lib install \"Adafruit NeoPixel\"", shell=True)

	print("Welcome to undercity hopefully fixed lanyard upload script (x2)")


def create_badge(name: str, slack_handle: str, extra: Optional[str] = None, img_path: Optional[os.PathLike] = None):  # noqa
	img: Optional[Image.Image] = None
	handle_offset: int = 0

	if img_path:
		try:
			img = Image.open(img_path)
			img = img.convert("RGBA")  # Ensure alpha channel
			# Composite over white background to replace transparency with white
			white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
			img = Image.alpha_composite(white_bg, img)
			# Resize while maintaining aspect ratio, max size 60x60
			max_size = (32, 32)
			img.thumbnail(max_size, Image.LANCZOS)
			img.save("img_resized.png")
			handle_offset = 32
		except Exception as e:
			print(f"Error processing image: {e}")
			exit(1)
	else:
		img = None
		print("No image provided.")

	try:
		font = ImageFont.truetype("./font.ttf", 25)

		temp_img = Image.new('RGB', (1000, 100), color='white')
		draw = ImageDraw.Draw(temp_img)

		bbox = draw.textbbox((0, 0), name, font=font)
		name_width = bbox[2] - bbox[0]

		# print(f"Name width: {name_width} pixels")

	except Exception as e:
		print(f"Error calculating text width: {e}")
		exit(1)

	extra_text_x = name_width + 40

	try:
		badge = Image.open("badge.bmp")
		draw = ImageDraw.Draw(badge)

		main_font = ImageFont.truetype("./font.ttf", 25)
		bank_font = ImageFont.truetype("./bankfont.ttf", 15)

		draw.text((20, 10), name, font=main_font, fill="black")

		draw.text((12 + handle_offset, 40), f"@{slack_handle}", font=main_font, fill="black")

		draw.text((extra_text_x, 20), extra, font=bank_font, fill="black")

		badge.save("newbadge.bmp")
		print("Badge created successfully!")
	except Exception as e:
		print(f"Error creating badge: {e}")
		exit(1)

	if img:
		try:
			img = Image.open("img_resized.png")
			badge.paste(img, (8, 36))
			badge.save("newbadge.bmp")
			print("Badge with image created successfully!")
		except Exception as e:
			print(f"Error adding image to badge: {e}")
			exit(1)

	image_to_c_array("newbadge.bmp", "f.h", "gImage_img")


def flash_badge(
	wait_callback: callable = (lambda *a, **k: (
			input("Press Enter to AFTER you pressed the boot button on the board.") + "y")[0] == 'y'),
	cancel_callback: callable = (lambda *a, **k: print("Badge flashing cancelled.")),
	complete_callback: callable = (lambda *a, **k: print("Badge flashed successfully!")),
):
	image_to_c_array("newbadge.bmp", "f.h", "gImage_img")
	subprocess.run("arduino-cli compile --fqbn rp2040:rp2040:generic_rp2350 --output-dir ./build", shell=True)

	if not wait_callback():
		cancel_callback()
		return

	shutil.copy(
		f"build/{os.path.basename(os.path.abspath('.'))}.ino.uf2",
		"D:/" if os.name == 'nt' else "/Volumes/RP2350/"
		)

	complete_callback()
