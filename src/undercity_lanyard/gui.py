from dataclasses import dataclass
from os import listdir
from os.path import basename, exists
from pathlib import Path
from shutil import copy
from tkinter.messagebox import askokcancel, showinfo

from PIL import Image

from undercity_lanyard import __version__, cleanup, create_badge, flash_badge, init, get_resource

try:
	import customtkinter as ctk
except ImportError:
	exit("CustomTkinter is not installed. Please install it using `pip install .[gui]`")


@dataclass
class AppConfig():
	HEADING_FONT: tuple = ("Consolas", 32, "bold")
	LABEL_FONT: tuple = ("Consolas", 14)
	BUTTON_FONT: tuple = ("Consolas", 16)


class ImagePropertiesPopup(ctk.CTkToplevel):
	def __init__(self, master, image_path: str):
		super().__init__(master)
		self.title("Image Properties")
		self.geometry("300x200")

		self.image = Image.open(image_path)
		self.image_info = f"Size: {self.image.size[0]}x{self.image.size[1]} pixels\nMode: {self.image.mode}"

		self.label = ctk.CTkLabel(self, text=self.image_info, font=AppConfig.LABEL_FONT)
		self.label.pack(pady=20)

		self.close_button = ctk.CTkButton(self, text="Close", command=self.destroy)
		self.close_button.pack(pady=10)


class App(ctk.CTk):
	def __init__(self):
		super().__init__()

		self.image_path = None

		self.title(f"Undercity Lanyard Flasher v{__version__}")
		self.iconbitmap(get_resource(Path("./assets/icon.ico")))

		self.geometry("600x500")
		self.grid_setup()

		self.setup_widgets()

		# self.image_properties = ImagePropertiesPopup(self, "badge.bmp")

	def grid_setup(self):
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.rowconfigure(0, weight=2)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)

	def setup_widgets(self):
		self.title_label = ctk.CTkLabel(
			self,
			text=f"Undercity\nLanyard\nFlasher\nv{__version__}",
			font=AppConfig.HEADING_FONT,
			justify="left",
			anchor="w",
		)
		self.title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

		self.preview_image = ctk.CTkImage(
			light_image=Image.open("./newbadge.bmp" if "newbadge.bmp" in listdir() else "badge.bmp"),
			size=(296, 128)
		)
		self.preview_label = ctk.CTkLabel(
			self,
			image=self.preview_image,
			text=""
		)
		self.preview_label.grid(row=0, column=2, columnspan=2, padx=10, pady=20)

		self.name_label = ctk.CTkLabel(self, text="Name:", justify="left", anchor="w", font=AppConfig.LABEL_FONT)
		self.name_label.grid(row=1, column=0, padx=10, pady=10)
		self.name_entry = ctk.CTkEntry(self, font=AppConfig.LABEL_FONT)
		self.name_entry.grid(row=1, column=1, padx=10, pady=10)

		self.slack_label = ctk.CTkLabel(self, text="Handle:", justify="left", anchor="w", font=AppConfig.LABEL_FONT)
		self.slack_label.grid(row=1, column=2, padx=10, pady=10)
		self.slack_entry = ctk.CTkEntry(self, font=AppConfig.LABEL_FONT)
		self.slack_entry.grid(row=1, column=3, padx=10, pady=10)

		self.extra_label = ctk.CTkLabel(self, text="Extra Text:", justify="left", anchor="w", font=AppConfig.LABEL_FONT)
		self.extra_label.grid(row=2, column=2, padx=10, pady=10)
		self.extra_entry = ctk.CTkEntry(self, font=AppConfig.LABEL_FONT)
		self.extra_entry.grid(row=2, column=3, padx=10, pady=10)

		self.image_label = ctk.CTkLabel(self, text="Image:", justify="left", anchor="w", font=AppConfig.LABEL_FONT)
		self.image_label.grid(row=2, column=0, padx=10, pady=10)
		self.image_select = ctk.CTkButton(
			self,
			text="Select File...",
			font=AppConfig.BUTTON_FONT,
			command=self.select_image_file
		)
		self.image_select.grid(row=2, column=1, padx=10, pady=10)

		self.create_button = ctk.CTkButton(
			self,
			text="Create!",
			font=AppConfig.BUTTON_FONT + ("bold",),
			command=self.invoke_creation
		)
		self.create_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

		self.flash_button = ctk.CTkButton(
			self,
			text="Flash!",
			font=AppConfig.BUTTON_FONT + ("bold",),
			command=self.invoke_flash
		)
		self.flash_button.grid(row=4, column=2, columnspan=2, padx=10, pady=20)

	def select_image_file(self):
		self.image_path = ctk.filedialog.askopenfilename(title="Select an Image", filetypes=[("PNG Image Files", "*.png")])
		if self.image_path:
			print(f"Selected image: {self.image_path}")
		else:
			print("No image selected.")

		self.verify_image()
		self.image_select.configure(text=f"{basename(self.image_path) if self.image_path else 'Select File...'}")

	def verify_image(self):
		if not self.image_path:
			print("No image provided.")
			return

		if exists(self.image_path):
			copy(self.image_path, "img.png")
		else:
			print("Image file does not exist.")
			self.image_path = None

	def invoke_creation(self):
		cleanup()
		init()
		name = self.name_entry.get().strip()
		slack_handle = self.slack_entry.get().strip()
		extra = self.extra_entry.get().strip()
		self.verify_image()

		create_badge(name, slack_handle, extra, self.image_path)

		try:
			self.preview_image = ctk.CTkImage(
				light_image=Image.open("newbadge.bmp"),
				size=(296, 128)
			)
			self.preview_label.configure(image=self.preview_image)
		except FileNotFoundError:
			print("Error: 'newbadge.bmp' not found. Please create the badge first.")
			return

	def invoke_flash(self):
		try:
			flash_badge(
				wait_callback=(lambda *a, **k: askokcancel("Confirm", "Please ensure you have pressed the boot button on the board.")),
				cancel_callback=(lambda *a, **k: showinfo("Cancel", "Badge flashing cancelled.")),
				complete_callback=(lambda *a, **k: showinfo("Success", "Badge flashed successfully!"))
			)
		except Exception as e:
			print(f"Error flashing badge: {e}")
			return


def main():
	ctk.set_appearance_mode("system")
	app = App()
	app.mainloop()
