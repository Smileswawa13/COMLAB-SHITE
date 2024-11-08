from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# Global dictionary to store harvest data
harvests = {}

# Function to validate the date input
def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return valid_date
        except ValueError:
            print("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.")

# Function for the main harvest management menu
def harvest_menu(farmer_name):
    # Get the farmer's subfolder path
    farmer_subfolder = make_farmer_folder(farmer_name)

    if not farmer_subfolder:
        print("Farmer folder not created, exiting harvest management.")
        return

    # Load harvest data from the file
    load_harvests(farmer_subfolder)

    while True:
        print(f"~~ Harvest Management - Farmer {farmer_name} ~~")
        options = {
            "Add Harvest": add_harvest,
            "Edit Harvest": edit_harvest,
            "View Harvests": view_harvests,
            "Delete Harvest": delete_harvest,
            "Quit Harvest Management": None
        }

        for index, (action, key) in enumerate(options.items(), 1):
            print(f"{index}. {action}")
        print(f"What would you like to do, farmer {farmer_name}?")

        try:
            action = int(input("Enter here using the corresponding number: "))

            if 1 <= action <= 4:
                selected_action = list(options.keys())[action - 1]
                selected_function = options[selected_action]
                print(f"Executing...'{selected_action}'.")

                if callable(selected_function):
                    if selected_function == view_harvests:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)

            elif action == 5:
                print("Going Back to Main Menu")
                break

            else:
                print("Please enter a valid number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

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
                    print(f"Error loading harvest data: {e}. Skipping line.")
        print("Harvests loaded successfully.")
    else:
        print("No harvest file found. Starting with an empty list.")

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
    print("Harvests saved successfully.")

# Function to add harvest data
def add_harvest(farmer_subfolder, farmer_name):
    print("~~ Adding New Harvest ~~")
    try:
        harvest_id = int(input("Please enter the harvest ID: "))
    except ValueError:
        print("Invalid harvest ID. It should be a numeric value.")
        return

    if harvest_id in harvests:
        print(f"Harvest with ID '{harvest_id}' already exists!")
        return

    # Input harvest details
    harvest_date = get_valid_date("Enter the harvest date (YYYY-MM-DD): ")
    planted_date = get_valid_date("Enter the date the crop was planted (YYYY-MM-DD): ")
    crop_name = get_non_empty_input("Enter the crop name: ").strip()
    crop_variety = get_non_empty_input("Enter the crop variety: ").strip()
    crop_field = get_non_empty_input("Enter the field or location: ").strip()

    while True:
        try:
            harvest_quantity = int(input("Enter the harvest quantity in kilograms: ").strip())
            break
        except ValueError:
            print("Invalid quantity. Please enter a numeric value.")

    # New input for price per kg (currency in PHP)
    while True:
        try:
            price_per_kg = float(input("Enter the price per kilogram in PHP: ").strip())
            break
        except ValueError:
            print("Invalid price. Please enter a numeric value.")

    quality_assessment = input("Enter a quality assessment for the harvest: ").strip()
    harvest_notes = input("Enter any additional notes about the harvest (optional): ").strip()

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
    print(f"Harvest ID {harvest_id} has been added!")

# Function to view all harvests
def view_harvests(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_harvests(farmer_subfolder)

    print("~~ All Harvests Stored in the Logbook ~~")

    if not harvests:
        print("No harvests found.")
        return

    headers = ["Harvest ID", "Date Harvested", "Date Planted", "Crop Name", "Variety", "Field", "Harvest Quantity (kg)", "Price Per Kg (PHP)", "Quality", "Notes"]
    table_data = []

    for harvest_id, details in harvests.items():
        formatted_date_harvested = details['Date Harvested:'].strftime("%Y-%m-%d")
        formatted_date_planted = details['Date Planted:'].strftime("%Y-%m-%d")

        # Format the price per kg to include PHP symbol
        price_per_kg = f"₱ {details['Price Per Kg (PHP)']:.2f}"

        row = [
            harvest_id,
            formatted_date_harvested,
            formatted_date_planted,
            details['Name of Crop:'],
            details['Variety:'],
            details['Field:'],
            details['Harvest Quantity'],
            price_per_kg,  # Display the price with PHP
            details['Quality Assessment:'],
            details['Notes'] or "No notes"
        ]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to edit existing harvest data
def edit_harvest(farmer_subfolder, farmer_name):
    view_harvests(farmer_name)
    try:
        harvest_id = int(input("Enter the harvest ID to edit: "))
        if harvest_id not in harvests:
            print("Harvest not found.")
            return

        # Retrieve current data for each field
        current_data = harvests[harvest_id]

        # Prompt for each field, keeping the existing value if the user skips
        crop_name = input(f"Enter the new crop name [{current_data['Name of Crop:']}]: ").strip()
        harvests[harvest_id]['Name of Crop:'] = crop_name if crop_name else current_data['Name of Crop:']

        crop_variety = input(f"Enter the new crop variety [{current_data['Variety:']}]: ").strip()
        harvests[harvest_id]['Variety:'] = crop_variety if crop_variety else current_data['Variety:']

        field = input(f"Enter the new field or location [{current_data['Field:']}]: ").strip()
        harvests[harvest_id]['Field:'] = field if field else current_data['Field:']

        # Numeric field for harvest quantity with option to keep current value
        quantity = input(f"Enter the new harvest quantity (kg) [{current_data['Harvest Quantity']}]: ").strip()
        if quantity:
            try:
                harvests[harvest_id]['Harvest Quantity'] = int(quantity)
            except ValueError:
                print("Invalid input for quantity. Keeping current value.")
        else:
            harvests[harvest_id]['Harvest Quantity'] = current_data['Harvest Quantity']

        # New input for price per kg (currency in PHP)
        price_per_kg = input(f"Enter the new price per kilogram in PHP [{current_data['Price Per Kg (PHP)']}]: ").strip()
        if price_per_kg:
            try:
                harvests[harvest_id]['Price Per Kg (PHP)'] = float(price_per_kg)
            except ValueError:
                print("Invalid input for price. Keeping current value.")
        else:
            harvests[harvest_id]['Price Per Kg (PHP)'] = current_data['Price Per Kg (PHP)']

        # Additional text fields
        quality = input(f"Enter the new quality assessment [{current_data['Quality Assessment:']}]: ").strip()
        harvests[harvest_id]['Quality Assessment:'] = quality if quality else current_data['Quality Assessment:']

        # Optional notes field
        notes = input(f"[Optional] Additional notes [{current_data['Notes'] or 'No notes'}]: ").strip()
        harvests[harvest_id]['Notes'] = notes if notes else current_data['Notes']

        # Save updated harvest data
        save_harvests(farmer_subfolder)
        print(f"Harvest ID {harvest_id} updated successfully.")

    except ValueError:
        print("Invalid input. Please enter a valid harvest ID.")

# Function to delete a harvest with confirmation
def delete_harvest(farmer_subfolder, farmer_name):
    view_harvests(farmer_name)  # Display the list of harvests first
    try:
        harvest_id = int(input("Enter the harvest ID to delete: "))
        if harvest_id in harvests:
            # Get the correct harvest name for logging purposes
            harvest_name = harvests[harvest_id]['Name of Crop:']

            # Prompt for confirmation
            confirmation = input(
                f"Are you sure you want to delete harvest ID {harvest_id} ('{harvest_name}')? Type 'yes' to confirm: ").strip().lower()
            if confirmation == "yes":
                # Log the harvest removal before deleting
                log_harvest_removal(farmer_subfolder, harvest_id, harvest_name, farmer_name)

                # Delete the harvest
                del harvests[harvest_id]
                save_harvests(farmer_subfolder)  # Save the updated harvest list
                print(f"Harvest with ID {harvest_id} and name '{harvest_name}' has been deleted.")
            else:
                print("Deletion canceled.")
        else:
            print("Harvest not found.")
    except ValueError:
        print("Invalid input. Please enter a valid harvest ID.")
    except Exception as e:
        print(f"Error deleting harvest: {e}")

# Function to log harvest removal action
def log_harvest_removal(farmer_subfolder, harvest_id, harvest_name, farmer_name):
    log_file_path = os.path.join(farmer_subfolder, 'harvest_removal_log.txt')

    # Prepare the log entry with the current date and time
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Harvest ID: {harvest_id}, Crop Name: {harvest_name}, Removed by: {farmer_name}\n"

    # Append the log entry to the log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)
    print("Harvest removal logged successfully.")


# Helper function to get non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip():
            return user_input
        print("This field cannot be empty. Please provide a value.")
