from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# Global dictionary to store harvest data
harvests = {}

# Function to validate the date input
def get_valid_date(prompt):
    while True:
        date_input = input(f"\033[92m🌾 {prompt} 🌿\033[0m")  # Green for farming theme
        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return valid_date
        except ValueError:
            print("\033[91m❌ Invalid date format. Please enter a valid date in the format YYYY-MM-DD. ❌\033[0m")  # Red for error

# Function for the main harvest management menu
def harvest_menu(farmer_name):
    # Get the farmer's subfolder path
    farmer_subfolder = make_farmer_folder(farmer_name)

    if not farmer_subfolder:
        print("\033[91m❌ Farmer folder not created, exiting harvest management. ❌\033[0m")  # Red for error
        return

    # Load harvest data from the file
    load_harvests(farmer_subfolder)

    while True:
        print(f"\033[92m🌱~~ Harvest Management - Farmer {farmer_name} ~~🌱\033[0m")  # Green for main menu
        options = {
            "Add Harvest 🌾": add_harvest,
            "Edit Harvest ✏️": edit_harvest,
            "View Harvests 📋": view_harvests,
            "Delete Harvest 🗑️": delete_harvest,
            "Quit Harvest Management 🚪": None
        }

        for index, (action, key) in enumerate(options.items(), 1):
            print(f"\033[93m{index}. {action}\033[0m")  # Yellow for action choices
        print(f"\033[92m🌻 What would you like to do, farmer {farmer_name}? 🌻\033[0m")

        try:
            action = int(input("\033[94m🌾 Enter here using the corresponding number: 🌾\033[0m"))  # Blue for input prompt

            if 1 <= action <= 4:
                selected_action = list(options.keys())[action - 1]
                selected_function = options[selected_action]
                print(f"\033[93m🌱 Executing...'{selected_action}' 🌾\033[0m.")  # Yellow for execution message

                if callable(selected_function):
                    if selected_function == view_harvests:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)

            elif action == 5:
                print("\033[92m🚪 Going Back to Main Menu 🚪\033[0m")  # Green for going back message
                break

            else:
                print("\033[91m❌ Please enter a valid number between 1 and 5. ❌\033[0m")  # Red for invalid input
        except ValueError:
            print("\033[91m❌ Please enter a valid number. ❌\033[0m")  # Red for invalid input

# Function to load harvest data from a file
def load_harvests(farmer_subfolder):
    harvest_file_path = os.path.join(farmer_subfolder, 'harvests.txt')

    if os.path.exists(harvest_file_path):
        with open(harvest_file_path, 'r') as file:
            for line in file:
                harvest_data = line.strip().split(",")
                try:
                    harvest_id = int(harvest_data[0])
                    harvests[harvest_id] = {
                        'Date Harvested:': datetime.strptime(harvest_data[1], "%Y-%m-%d"),
                        'Date Planted:': datetime.strptime(harvest_data[2], "%Y-%m-%d"),
                        'Name of Crop:': harvest_data[3],
                        'Variety:': harvest_data[4],
                        'Field:': harvest_data[5],
                        'Harvest Quantity': int(harvest_data[6]),
                        'Price Per Kg (PHP)': float(harvest_data[7]),  # Load price per kg
                        'Quality Assessment:': harvest_data[8],
                        'Notes': harvest_data[9]
                    }
                except ValueError as e:
                    print(f"\033[91m❌ Error loading harvest data: {e}. Skipping line. ❌\033[0m")
        print("\033[92m🌾 Harvests loaded successfully. 🌾\033[0m")
    else:
        print("\033[91m❌ No harvest file found. Starting with an empty list. ❌\033[0m")

# Function to save harvest data into the file
def save_harvests(farmer_subfolder):
    harvest_file_path = os.path.join(farmer_subfolder, 'harvests.txt')

    with open(harvest_file_path, 'w') as file:
        for harvest_id, harvest_data in harvests.items():
            formatted_date_harvested = harvest_data['Date Harvested:'].strftime("%Y-%m-%d")
            formatted_date_planted = harvest_data['Date Planted:'].strftime("%Y-%m-%d")
            file.write(f"{harvest_id},{formatted_date_harvested},{formatted_date_planted},{harvest_data['Name of Crop:']},"
                       f"{harvest_data['Variety:']},{harvest_data['Field:']},{harvest_data['Harvest Quantity']},"
                       f"{harvest_data['Price Per Kg (PHP)']},"
                       f"{harvest_data['Quality Assessment:']},{harvest_data['Notes']}\n")
    print("\033[92m🌾 Harvests saved successfully. 🌾\033[0m")

# Function to add harvest data
def add_harvest(farmer_subfolder, farmer_name):
    print("\033[92m🌱~~ Adding New Harvest ~~🌱\033[0m")
    try:
        harvest_id = int(input("\033[94m🌾 Please enter the harvest ID: 🌾\033[0m"))
    except ValueError:
        print("\033[91m❌ Invalid harvest ID. It should be a numeric value. ❌\033[0m")
        return

    if harvest_id in harvests:
        print(f"\033[91m❌ Harvest with ID '{harvest_id}' already exists! ❌\033[0m")
        return

    # Input harvest details
    harvest_date = get_valid_date("\033[94m🌾 Enter the harvest date (YYYY-MM-DD): 🌾\033[0m")
    planted_date = get_valid_date("\033[94m🌾 Enter the date the crop was planted (YYYY-MM-DD): 🌾\033[0m")
    crop_name = get_non_empty_input("\033[92m🌾 Enter the crop name: 🌿\033[0m").strip()
    crop_variety = get_non_empty_input("\033[92m🌾 Enter the crop variety: 🌿\033[0m").strip()
    crop_field = get_non_empty_input("\033[92m🌾 Enter the field or location: 🌿\033[0m").strip()

    while True:
        try:
            harvest_quantity = int(input("\033[94m🌾 Enter the harvest quantity in kilograms: 🌾\033[0m").strip())
            break
        except ValueError:
            print("\033[91m❌ Invalid quantity. Please enter a numeric value. ❌\033[0m")

    # New input for price per kg (currency in PHP)
    while True:
        try:
            price_per_kg = float(input("\033[94m🌾 Enter the price per kilogram in PHP: 🌾\033[0m").strip())
            break
        except ValueError:
            print("\033[91m❌ Invalid price. Please enter a numeric value. ❌\033[0m")

    quality_assessment = input("\033[92m🌿 Enter a quality assessment for the harvest: 🌿\033[0m").strip()
    harvest_notes = input("\033[92m🌾 Enter any additional notes about the harvest (optional): 🌾\033[0m").strip()

    harvests[harvest_id] = {
        'Date Harvested:': harvest_date,
        'Date Planted:': planted_date,
        'Name of Crop:': crop_name,
        'Variety:': crop_variety,
        'Field:': crop_field,
        'Harvest Quantity': harvest_quantity,
        'Price Per Kg (PHP)': price_per_kg,  # New field
        'Quality Assessment:': quality_assessment,
        'Notes': harvest_notes
    }

    save_harvests(farmer_subfolder)
    print(f"\033[92m🌿 Harvest ID {harvest_id} has been added! 🌾\033[0m")

# Function to view all harvests
def view_harvests(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_harvests(farmer_subfolder)

    print("\033[92m🌿~~ All Harvests Stored ~~🌿\033[0m")

    if not harvests:
        print("\033[91m❌ No harvest data available! ❌\033[0m")
    else:
        table = []
        for harvest_id, harvest_data in harvests.items():
            table.append([harvest_id, harvest_data['Name of Crop:'], harvest_data['Harvest Quantity'], harvest_data['Price Per Kg (PHP)']])
        print(tabulate(table, headers=["Harvest ID", "Crop Name", "Quantity (Kg)", "Price per Kg"], tablefmt="grid"))

# Function to edit a specific harvest
def edit_harvest(farmer_subfolder, farmer_name):
    view_harvests(farmer_name)
    try:
        harvest_id = int(input("\033[94m🌾 Enter the ID of the harvest you want to edit: 🌾\033[0m"))
    except ValueError:
        print("\033[91m❌ Invalid harvest ID. ❌\033[0m")
        return

    if harvest_id not in harvests:
        print("\033[91m❌ Harvest ID not found. ❌\033[0m")
        return

    print(f"\033[92m🌿 Editing Harvest ID {harvest_id} 🌿\033[0m")
    harvest_data = harvests[harvest_id]

    # Edit the details
    harvest_data['Name of Crop:'] = get_non_empty_input("\033[92m🌾 Enter the crop name: 🌿\033[0m").strip()
    harvest_data['Variety:'] = get_non_empty_input("\033[92m🌾 Enter the crop variety: 🌿\033[0m").strip()
    harvest_data['Field:'] = get_non_empty_input("\033[92m🌾 Enter the field or location: 🌿\033[0m").strip()
    harvest_data['Harvest Quantity'] = int(input("\033[94m🌾 Enter the updated harvest quantity in kilograms: 🌾\033[0m"))
    harvest_data['Price Per Kg (PHP)'] = float(input("\033[94m🌾 Enter the updated price per kilogram in PHP: 🌾\033[0m"))
    harvest_data['Quality Assessment:'] = input("\033[92m🌿 Enter the updated quality assessment: 🌿\033[0m").strip()
    harvest_data['Notes'] = input("\033[92m🌾 Enter any updated notes about the harvest: 🌾\033[0m").strip()

    save_harvests(farmer_subfolder)
    print(f"\033[92m🌿 Harvest ID {harvest_id} has been updated! 🌾\033[0m")

# Function to delete a harvest with confirmation
def delete_harvest(farmer_subfolder, farmer_name):
    view_harvests(farmer_name)  # Display the list of harvests first
    try:
        harvest_id = int(input("\033[94m🌾 Enter the harvest ID to delete: 🌾\033[0m"))
        if harvest_id in harvests:
            # Get the correct harvest name for logging purposes
            harvest_name = harvests[harvest_id]['Name of Crop:']

            # Prompt for confirmation
            confirmation = input(
                f"\033[91m❓ Are you sure you want to delete harvest ID {harvest_id} ('{harvest_name}')? Type 'yes' to confirm: ❓\033[0m").strip().lower()
            if confirmation == "yes":
                # Log the harvest removal before deleting
                log_harvest_removal(farmer_subfolder, harvest_id, harvest_name, farmer_name)

                # Delete the harvest
                del harvests[harvest_id]
                save_harvests(farmer_subfolder)  # Save the updated harvest list
                print(f"\033[91m❌ Harvest with ID {harvest_id} and name '{harvest_name}' has been deleted. ❌\033[0m")
            else:
                print("\033[92m✅ Deletion canceled. ✅\033[0m")
        else:
            print("\033[91m❌ Harvest not found. ❌\033[0m")
    except ValueError:
        print("\033[91m❌ Invalid input. Please enter a valid harvest ID. ❌\033[0m")
    except Exception as e:
        print(f"\033[91m❌ Error deleting harvest: {e} ❌\033[0m")

# Function to log harvest removal action
def log_harvest_removal(farmer_subfolder, harvest_id, harvest_name, farmer_name):
    log_file_path = os.path.join(farmer_subfolder, 'harvest_removal_log.txt')

    # Prepare the log entry with the current date and time
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Harvest ID: {harvest_id}, Crop Name: {harvest_name}, Removed by: {farmer_name}\n"

    # Append the log entry to the log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)
    print("\033[91m❌ Harvest removal logged successfully. ❌\033[0m")


# Function to get non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(f"\033[92m{prompt}\033[0m").strip()
        if user_input:
            return user_input
        else:
            print("\033[91m❌ Input cannot be empty. Please enter something. ❌\033[0m")
