from undercity_lanyard import __version__
import sys


if __name__ == "__main__":
	print(f"Undercity Lanyard Flasher v{__version__}")

	try:
		if len(sys.argv) > 1 and sys.argv[1] == "--gui":
			from undercity_lanyard.gui import main
		elif getattr(sys, 'frozen', False) and (hasattr(sys, '_MEIPASS') or hasattr(sys, '_MEIPASS2')):
			from undercity_lanyard.gui import main
		else:
			from undercity_lanyard.console import main
	except ImportError as e:
		print(f"Error: {e}")
		sys.exit(1)
	else:
		main()
