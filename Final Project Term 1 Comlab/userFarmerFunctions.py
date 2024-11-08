import os


def make_farmer_folder(farmer_name):
	try:
		# Ensure that the farmer's name is already set (no need to ask again)
		if not farmer_name:
			print("Error: Farmer name is not set.")
			return None  # Exit if no name is set

		# Get the current directory for the entire program
		current_directory = os.path.dirname(os.path.abspath(__file__))

		# Define the main directory for all farmers
		farmers_directory = os.path.join(current_directory, "Farmers")
		os.makedirs(farmers_directory, exist_ok=True)  # Create "Farmers" folder if it doesn't exist

		# Path for the specific farmer's subdirectory
		farmer_subfolder_path = os.path.join(farmers_directory, farmer_name)

		# Check if the farmer's directory already exists
		if not os.path.exists(farmer_subfolder_path):
			# Create a new directory for the farmer
			os.makedirs(farmer_subfolder_path)
			print(f"Created folder for farmer: {farmer_name}")
		else:
			print(f"Folder already exists for farmer: {farmer_name}")

		return farmer_subfolder_path

	except PermissionError:
		print("Permission denied: Unable to create directories or files. Please check your permissions.")
		return None

	except FileNotFoundError:
		print("File path not found. Please check the directory structure.")
		return None

	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		return None
