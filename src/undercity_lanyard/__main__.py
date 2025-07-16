from . import __version__
import sys


if __name__ == "__main__":
	print(f"Undercity Lanyard Flasher v{__version__}")

	try:
		if len(sys.argv) > 1 and sys.argv[1] == "--gui":
			from .gui import main
		else:
			from .console import main
	except ImportError as e:
		print(f"Error: {e}")
		sys.exit(1)
	else:
		main()
