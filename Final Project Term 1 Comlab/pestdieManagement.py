from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# Global dictionary to store pesticide and medicine data
pesticideMedicine = {}

# Function to validate date input
def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")

# Function for the main pesticide and medicine management menu
def pesticide_medicine_menu(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    if not farmer_subfolder:
        print("Farmer folder not created, exiting pesticide/medicine management.")
        return

    load_pesticide_medicine(farmer_subfolder)

    while True:
        print(f"~~Pesticide & Medicine Management - Farmer {farmer_name}~~")
        options = {
            "Add Pesticide/Medicine": add_pesticide_medicine,
            "Edit Pesticide/Medicine": edit_pesticide_medicine,
            "View Pesticides/Medicines": view_pesticide_medicine,
            "Delete Pesticide/Medicine": delete_pesticide_medicine,
            "Quit Pesticide/Medicine Management": None
        }

        for index, action in enumerate(options, 1):
            print(f"{index}. {action}")

        try:
            action = int(input("Enter here using the corresponding number: "))
            if 1 <= action <= 4:
                selected_function = list(options.values())[action - 1]
                if callable(selected_function):
                    if selected_function == view_pesticide_medicine:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)
            elif action == 5:
                print("Exiting Pesticide & Medicine Management")
                break
            else:
                print("Invalid choice. Choose between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

# Function to load pesticide and medicine data from a file
def load_pesticide_medicine(farmer_subfolder):
    file_path = os.path.join(farmer_subfolder, 'pesticide_medicine.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                try:
                    pestmed_id = int(data[0])
                    pesticideMedicine[pestmed_id] = {
                        'Scheduled Date': datetime.strptime(data[1], "%Y-%m-%d"),
                        'Application Date': datetime.strptime(data[2], "%Y-%m-%d"),
                        'Disease/Pests': data[3],
                        'Crop Applied to': data[4],
                        'Name': data[5],
                        'Variety': data[6],
                        'Field': data[7],
                        'Area': int(data[8]),
                        'Quantity': int(data[9]),
                        'Supplier Cost': float(data[10]),  # Add Supplier Cost
                        'Notes': data[11] if len(data) > 11 else ""
                    }
                except ValueError as e:
                    print(f"Error loading pesticide/medicine data: {e}. Skipping line.")
        print("Pesticides/Medicines loaded successfully.")
    else:
        print("No pesticide/medicine file found. Starting with an empty list.")

# Function to save pesticide and medicine data to a file
def save_pesticide_medicine(farmer_subfolder):
    file_path = os.path.join(farmer_subfolder, 'pesticide_medicine.txt')
    with open(file_path, 'w') as file:
        for pestmed_id, data in pesticideMedicine.items():
            scheduled_date = data['Scheduled Date'].strftime("%Y-%m-%d")
            application_date = data['Application Date'].strftime("%Y-%m-%d")
            file.write(
                f"{pestmed_id},{scheduled_date},{application_date},{data['Disease/Pests']},{data['Crop Applied to']},"
                f"{data['Name']},{data['Variety']},{data['Field']},{data['Area']},{data['Quantity']},{data['Supplier Cost']},{data['Notes']}\n")
    print("Pesticide/Medicine data saved successfully.")

# Function to add pesticide and medicine data
def add_pesticide_medicine(farmer_subfolder, farmer_name):
    print("~~ Adding New Pesticide/Medicine ~~")
    try:
        pestmed_id = int(input("Please enter a unique pesticide/medicine ID: "))
        if pestmed_id in pesticideMedicine:
            print(f"Pesticide/Medicine with ID '{pestmed_id}' already exists!")
            return
    except ValueError:
        print("Invalid ID. It should be numeric.")
        return

    scheduled_date = get_valid_date("Enter the scheduled date for pesticide/medicine use (YYYY-MM-DD): ")
    application_date = get_valid_date("Enter the actual application date (YYYY-MM-DD): ")
    disease_pests = input("Enter the disease or pests targeted by this pesticide/medicine: ").strip()
    crop_name = input("Enter the crop this pesticide/medicine is applied to: ").strip()
    name = input("Enter the pesticide/medicine name: ").strip()
    variety = input("Enter the pesticide/medicine variety/type: ").strip()
    field = input("Enter the field or location: ").strip()
    try:
        area = int(input("Enter the area covered in hectares: ").strip())
        quantity = int(input("Enter the quantity used in kg: ").strip())
    except ValueError:
        print("Invalid input for area or quantity.")
        return

    # Ask for supplier cost in PHP
    try:
        supplier_cost_php = float(input("Enter the supplier cost for the pesticide/medicine (in PHP): ").strip())
    except ValueError:
        print("Invalid input for supplier cost. Please enter a valid number.")
        return

    notes = input("[Optional] Additional notes: ").strip()

    pesticideMedicine[pestmed_id] = {
        'Scheduled Date': scheduled_date,
        'Application Date': application_date,
        'Disease/Pests': disease_pests,
        'Crop Applied to': crop_name,
        'Name': name,
        'Variety': variety,
        'Field': field,
        'Area': area,
        'Quantity': quantity,
        'Supplier Cost': supplier_cost_php,  # Store supplier cost in PHP
        'Notes': notes
    }

    save_pesticide_medicine(farmer_subfolder)
    print("Pesticide/Medicine added successfully.")

# Function to edit pesticide and medicine data
def edit_pesticide_medicine(farmer_subfolder, farmer_name):
    view_pesticide_medicine(farmer_name)
    try:
        pestmed_id = int(input("Enter the pesticide/medicine ID to edit: "))
        if pestmed_id not in pesticideMedicine:
            print("Pesticide/Medicine not found.")
            return

        # Retrieve the current data for each field
        current_data = pesticideMedicine[pestmed_id]

        # Prompt for each field, keeping the existing value if the user skips
        scheduled_date = get_valid_date(
            "Enter the new scheduled date (YYYY-MM-DD) or press Enter to keep the current date: ")
        pesticideMedicine[pestmed_id]['Scheduled Date'] = scheduled_date if scheduled_date else current_data[
            'Scheduled Date']

        application_date = get_valid_date(
            "Enter the new application date (YYYY-MM-DD) or press Enter to keep the current date: ")
        pesticideMedicine[pestmed_id]['Application Date'] = application_date if application_date else current_data[
            'Application Date']

        # Text fields with option to keep current value
        disease_pests = input(f"Enter the disease or pests targeted [{current_data['Disease/Pests']}]: ").strip()
        pesticideMedicine[pestmed_id]['Disease/Pests'] = disease_pests if disease_pests else current_data[
            'Disease/Pests']

        crop_name = input(
            f"Enter the crop this pesticide/medicine is applied to [{current_data['Crop Applied to']}]: ").strip()
        pesticideMedicine[pestmed_id]['Crop Applied to'] = crop_name if crop_name else current_data['Crop Applied to']

        name = input(f"Enter the pesticide/medicine name [{current_data['Name']}]: ").strip()
        pesticideMedicine[pestmed_id]['Name'] = name if name else current_data['Name']

        variety = input(f"Enter the pesticide/medicine variety/type [{current_data['Variety']}]: ").strip()
        pesticideMedicine[pestmed_id]['Variety'] = variety if variety else current_data['Variety']

        field = input(f"Enter the field or location [{current_data['Field']}]: ").strip()
        pesticideMedicine[pestmed_id]['Field'] = field if field else current_data['Field']

        # Numeric fields with option to keep current value
        area = input(f"Enter the area in hectares [{current_data['Area']}]: ").strip()
        if area:
            try:
                pesticideMedicine[pestmed_id]['Area'] = int(area)
            except ValueError:
                print("Invalid input for area. Keeping current value.")
        else:
            pesticideMedicine[pestmed_id]['Area'] = current_data['Area']

        quantity = input(f"Enter the quantity in kg [{current_data['Quantity']}]: ").strip()
        if quantity:
            try:
                pesticideMedicine[pestmed_id]['Quantity'] = int(quantity)
            except ValueError:
                print("Invalid input for quantity. Keeping current value.")
        else:
            pesticideMedicine[pestmed_id]['Quantity'] = current_data['Quantity']

        # Ask for supplier cost in PHP (new field)
        try:
            supplier_cost = input(f"Enter the new supplier cost in PHP (current cost: {current_data['Supplier Cost']}) or press Enter to keep current value: ").strip()
            if supplier_cost:
                pesticideMedicine[pestmed_id]['Supplier Cost'] = float(supplier_cost)
        except ValueError:
            print("Invalid input for supplier cost. Keeping current value.")

        # Optional notes field
        notes = input(f"[Optional] Additional notes [{current_data['Notes'] or 'No notes'}]: ").strip()
        pesticideMedicine[pestmed_id]['Notes'] = notes if notes else current_data['Notes']

        save_pesticide_medicine(farmer_subfolder)
        print(f"Pesticide/Medicine ID {pestmed_id} edited successfully.")
    except ValueError:
        print("Invalid ID.")

# Function to view all pesticides and medicines
def view_pesticide_medicine(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_pesticide_medicine(farmer_subfolder)

    if not pesticideMedicine:
        print("No pesticides or medicines found.")
        return

    # Add Supplier Cost to the headers and table
    headers = ["ID", "Scheduled Date", "Application Date", "Disease/Pests", "Crop Applied to", "Name",
               "Variety", "Field", "Area (ha)", "Quantity (kg)", "Supplier Cost (PHP)", "Notes"]
    table_data = []

    for pestmed_id, data in pesticideMedicine.items():
        row = [
            pestmed_id,
            data['Scheduled Date'].strftime("%Y-%m-%d"),
            data['Application Date'].strftime("%Y-%m-%d"),
            data['Disease/Pests'],
            data['Crop Applied to'],
            data['Name'],
            data['Variety'],
            data['Field'],
            data['Area'],
            data['Quantity'],
            f"₱{data['Supplier Cost']:.2f}",  # Format supplier cost as PHP
            data['Notes'] or "No notes"
        ]
        table_data.append(row)

    # Display the table with the new header and supplier cost in PHP format
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to delete a pesticide or medicine with confirmation
def delete_pesticide_medicine(farmer_subfolder, farmer_name):
    view_pesticide_medicine(farmer_name)  # Display the list of pesticide/medicine
    try:
        pestmed_id = int(input("Enter the pesticide/medicine ID to delete: "))
        if pestmed_id in pesticideMedicine:
            name = pesticideMedicine[pestmed_id]['Name']

            # Prompt for confirmation
            confirmation = input(
                f"Are you sure you want to delete pesticide/medicine ID {pestmed_id} ({name})? Type 'yes' to confirm: ").strip().lower()
            if confirmation == "yes":
                # Log the pesticide/medicine removal before deleting
                log_pesticide_medicine_removal(farmer_subfolder, pestmed_id, name, farmer_name)

                # Delete the pesticide/medicine
                del pesticideMedicine[pestmed_id]
                save_pesticide_medicine(farmer_subfolder)  # Save the updated pesticide/medicine list
                print(f"Pesticide/Medicine ID {pestmed_id} deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("Pesticide/Medicine not found.")
    except ValueError:
        print("Invalid ID. Please enter a valid pesticide/medicine ID.")
    except Exception as e:
        print(f"Error deleting pesticide/medicine: {e}")


# Function to log pesticide and medicine removal
def log_pesticide_medicine_removal(farmer_subfolder, pestmed_id, name, farmer_name):
    log_file_path = os.path.join(farmer_subfolder, 'pesticide_medicine_removal_log.txt')

    # Prepare the log entry with the current date and time
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ID: {pestmed_id}, Name: {name}, Removed by: {farmer_name}\n"

    # Append the log entry to the log file
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
