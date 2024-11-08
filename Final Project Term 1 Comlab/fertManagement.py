from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# Global fertilizer dictionary to store fertilizer data
fertilizer = {}

# Function to validate date input
def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")

# Function for the main fertilizer management menu
def fertilizer_menu(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    if not farmer_subfolder:
        print("Farmer folder not created, exiting fertilizer management.")
        return

    load_fertilizer(farmer_subfolder)

    while True:
        print(f"~~Fertilizer Management - Farmer {farmer_name}~~")
        options = {
            "Add Fertilizer": add_fertilizer,
            "Edit Fertilizer": edit_fertilizer,
            "View Fertilizers": view_fertilizer,
            "Delete Fertilizer": delete_fertilizer,
            "Quit Fertilizer Management": None
        }

        for index, action in enumerate(options, 1):
            print(f"{index}. {action}")

        try:
            action = int(input("Enter here using the corresponding number: "))
            if 1 <= action <= 4:
                selected_function = list(options.values())[action - 1]
                if callable(selected_function):
                    if selected_function == view_fertilizer:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)
            elif action == 5:
                print("Exiting Fertilizer Management")
                break
            else:
                print("Invalid choice. Choose between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

# Function to load fertilizer data from a file
def load_fertilizer(farmer_subfolder):
    fertilizer_file_path = os.path.join(farmer_subfolder, 'fertilizer.txt')
    if os.path.exists(fertilizer_file_path):
        with open(fertilizer_file_path, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                try:
                    fert_id = int(data[0])
                    # Ensure to properly handle Supplier Cost (assuming it's always at index 10, or provide a fallback)
                    supplier_cost = float(data[10]) if data[10] != 'N/A' else 0.0

                    fertilizer[fert_id] = {
                        'Scheduled Date': datetime.strptime(data[1], "%Y-%m-%d"),
                        'Application Date': datetime.strptime(data[2], "%Y-%m-%d"),
                        'Crop Applied to': data[3],
                        'Name': data[4],
                        'Variety': data[5],
                        'Field': data[6],
                        'Area': int(data[7]),
                        'Quantity': int(data[8]),
                        'Supplier Cost': supplier_cost,  # Add the Supplier Cost here
                        'Notes': data[11] if len(data) > 11 else ""
                    }
                except ValueError as e:
                    print(f"Error loading fertilizer data: {e}. Skipping line.")
        print("Fertilizers loaded successfully.")
    else:
        print("No fertilizer file found. Starting with an empty list.")


# Function to save fertilizer data to a file
def save_fertilizer(farmer_subfolder):
    fertilizer_file_path = os.path.join(farmer_subfolder, 'fertilizer.txt')
    with open(fertilizer_file_path, 'w') as file:
        for fert_id, data in fertilizer.items():
            scheduled_date = data['Scheduled Date'].strftime("%Y-%m-%d")
            application_date = data['Application Date'].strftime("%Y-%m-%d")
            supplier_cost = data.get('Supplier Cost', 'N/A')  # Ensure to handle the Supplier Cost
            file.write(
                f"{fert_id},{scheduled_date},{application_date},{data['Crop Applied to']},{data['Name']},"
                f"{data['Variety']},{data['Field']},{data['Area']},{data['Quantity']},{supplier_cost},{data['Notes']}\n")
    print("Fertilizer data saved successfully.")


# Function to add fertilizer data
def add_fertilizer(farmer_subfolder, farmer_name):
    print("~~ Adding New Fertilizer ~~")
    try:
        fert_id = int(input("Please enter a unique fertilizer ID: "))
        if fert_id in fertilizer:
            print(f"Fertilizer with ID '{fert_id}' already exists!")
            return
    except ValueError:
        print("Invalid ID. It should be numeric.")
        return

    scheduled_date = get_valid_date("Enter the scheduled date for fertilizer use (YYYY-MM-DD): ")
    application_date = get_valid_date("Enter the actual application date (YYYY-MM-DD): ")
    crop_name = input("Enter the crop this fertilizer is applied to: ").strip()
    fert_name = input("Enter the fertilizer name: ").strip()
    fert_variety = input("Enter the fertilizer variety/type: ").strip()
    fert_field = input("Enter the field or location: ").strip()
    try:
        fert_area = int(input("Enter the area covered in hectares: ").strip())
        fert_quantity = int(input("Enter the quantity used in kg: ").strip())
    except ValueError:
        print("Invalid input for area or quantity.")
        return

    fert_notes = input("[Optional] Additional notes: ").strip()

    # New input for Supplier Cost in PHP
    try:
        supplier_cost = float(input("Enter the supplier cost per kg (in PHP): ").strip())  # Specify PHP
    except ValueError:
        print("Invalid supplier cost. It should be a numeric value.")
        return

    fertilizer[fert_id] = {
        'Scheduled Date': scheduled_date,
        'Application Date': application_date,
        'Crop Applied to': crop_name,
        'Name': fert_name,
        'Variety': fert_variety,
        'Field': fert_field,
        'Area': fert_area,
        'Quantity': fert_quantity,
        'Notes': fert_notes,
        'Supplier Cost': supplier_cost  # New field for supplier cost
    }

    save_fertilizer(farmer_subfolder)
    print("Fertilizer added successfully.")

# Function to edit fertilizer data
def edit_fertilizer(farmer_subfolder, farmer_name):
    view_fertilizer(farmer_name)
    try:
        fert_id = int(input("Enter the fertilizer ID to edit: "))
        if fert_id not in fertilizer:
            print("Fertilizer not found.")
            return

        # Retrieve the current data for each field
        current_data = fertilizer[fert_id]

        # Prompt for each field, keeping the existing value if the user skips
        scheduled_date = get_valid_date(
            "Enter the new scheduled date (YYYY-MM-DD) or press Enter to keep the current date: ")
        fertilizer[fert_id]['Scheduled Date'] = scheduled_date if scheduled_date else current_data['Scheduled Date']

        application_date = get_valid_date(
            "Enter the new application date (YYYY-MM-DD) or press Enter to keep the current date: ")
        fertilizer[fert_id]['Application Date'] = application_date if application_date else current_data[
            'Application Date']

        # Text fields with option to keep current value
        crop_name = input(f"Enter the crop this fertilizer is applied to [{current_data['Crop Applied to']}]: ").strip()
        fertilizer[fert_id]['Crop Applied to'] = crop_name if crop_name else current_data['Crop Applied to']

        name = input(f"Enter the fertilizer name [{current_data['Name']}]: ").strip()
        fertilizer[fert_id]['Name'] = name if name else current_data['Name']

        variety = input(f"Enter the fertilizer variety/type [{current_data['Variety']}]: ").strip()
        fertilizer[fert_id]['Variety'] = variety if variety else current_data['Variety']

        field = input(f"Enter the field or location [{current_data['Field']}]: ").strip()
        fertilizer[fert_id]['Field'] = field if field else current_data['Field']

        # Numeric fields with option to keep current value
        area = input(f"Enter the area in hectares [{current_data['Area']}]: ").strip()
        if area:
            try:
                fertilizer[fert_id]['Area'] = int(area)
            except ValueError:
                print("Invalid input for area. Keeping current value.")
        else:
            fertilizer[fert_id]['Area'] = current_data['Area']

        quantity = input(f"Enter the quantity in kg [{current_data['Quantity']}]: ").strip()
        if quantity:
            try:
                fertilizer[fert_id]['Quantity'] = int(quantity)
            except ValueError:
                print("Invalid input for quantity. Keeping current value.")
        else:
            fertilizer[fert_id]['Quantity'] = current_data['Quantity']

        # Optional notes field
        notes = input(f"[Optional] Additional notes [{current_data['Notes'] or 'No notes'}]: ").strip()
        fertilizer[fert_id]['Notes'] = notes if notes else current_data['Notes']

        # New field for Supplier Cost
        try:
            supplier_cost = input(
                f"Enter the supplier cost per kg [{current_data.get('Supplier Cost', 'No cost')}]: ").strip()
            if supplier_cost:
                fertilizer[fert_id]['Supplier Cost'] = float(supplier_cost)
        except ValueError:
            print("Invalid supplier cost input. Keeping current value.")

        save_fertilizer(farmer_subfolder)
        print(f"Fertilizer ID {fert_id} edited successfully.")
    except ValueError:
        print("Invalid ID.")


# Function to view all fertilizers
def view_fertilizer(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_fertilizer(farmer_subfolder)

    if not fertilizer:
        print("No fertilizers found.")
        return

    headers = ["ID", "Scheduled Date", "Application Date", "Crop Applied to", "Name", "Variety", "Field", "Area (ha)",
               "Quantity (kg)", "Supplier Cost", "Notes"]
    table_data = []

    for fert_id, data in fertilizer.items():
        row = [
            fert_id,
            data['Scheduled Date'].strftime("%Y-%m-%d"),
            data['Application Date'].strftime("%Y-%m-%d"),
            data['Crop Applied to'],
            data['Name'],
            data['Variety'],
            data['Field'],
            data['Area'],
            data['Quantity'],
            f"₱{data['Supplier Cost']:.2f}" if 'Supplier Cost' in data else "N/A",
            data['Notes'] or "No notes"
        ]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to delete a fertilizer with confirmation
def delete_fertilizer(farmer_subfolder, farmer_name):
    view_fertilizer(farmer_name)
    try:
        fert_id = int(input("Enter the fertilizer ID to delete: "))
        if fert_id in fertilizer:
            # Prompt for confirmation
            confirmation = input(f"Are you sure you want to delete fertilizer ID {fert_id}? Type 'yes' to confirm: ").strip().lower()
            if confirmation == "yes":
                fert_name = fertilizer[fert_id]['Name']
                del fertilizer[fert_id]
                save_fertilizer(farmer_subfolder)
                log_fertilizer_removal(farmer_subfolder, fert_id, fert_name, farmer_name)
                print(f"Fertilizer ID {fert_id} deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("Fertilizer not found.")
    except ValueError:
        print("Invalid ID.")

# Function to log fertilizer removal
def log_fertilizer_removal(farmer_subfolder, fert_id, fert_name, farmer_name):
    log_file_path = os.path.join(farmer_subfolder, 'fertilizer_removal_log.txt')
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ID: {fert_id}, Name: {fert_name}, Removed by: {farmer_name}\n"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)
    print("Removal logged successfully.")

def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")
