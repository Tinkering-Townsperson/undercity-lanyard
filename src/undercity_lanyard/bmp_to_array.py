from PIL import Image
import sys


def image_to_c_array(image_path, output_file, variable_name="image_data"):  # noqa
	"""
	Converts a monochrome BMP image to a C-style byte array.

	Args:
		image_path (str): The path to the input BMP image.
		output_file (str): The path to the output C header file.
		variable_name (str): The name for the C array variable.
	"""
	try:
		image = Image.open(image_path).convert('1').rotate(180)
	except IOError:
		print(f"Error: Cannot open image file {image_path}")
		return

	width, height = image.size
	pixels = list(image.getdata())

	with open(output_file, 'w') as f:
		f.write(f"// Generated from {image_path}\n")
		f.write(f"// Width: {width}, Height: {height}\n\n")
		f.write(f"const unsigned char {variable_name}[] = {{\n")

		byte_array = []
		for x in range(width):
			for y in range(0, height, 8):
				byte = 0
				for bit in range(8):
					if y + bit < height:
						pixel = pixels[(y + bit) * width + x]
						if pixel != 0:  # White pixel
							byte |= (1 << (7 - bit))
				byte_array.append(byte)

		for i, byte in enumerate(byte_array):
			if i % 16 == 0:
				f.write("    ")
			f.write(f"0x{byte:02X}, ")
			if i % 16 == 15:
				f.write("\n")

		if len(byte_array) % 16 != 0:
			f.write("\n")

		f.write("};\n")

	print(f"Successfully converted {image_path} to {output_file}")


if __name__ == "__main__":
	if len(sys.argv) != 4:
		print("Usage: python bmp_to_array.py <input.bmp> <output.h> <variable_name>")
		sys.exit(1)

	image_to_c_array(sys.argv[1], sys.argv[2], sys.argv[3])
