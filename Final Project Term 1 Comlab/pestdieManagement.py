from datetime import datetime
from tabulate import tabulate
import os

from profitManagement import pesticide_medicine
from userFarmerFunctions import make_farmer_folder

# Global dictionary to store pesticide and medicine data
pesticideMedicine = {}

# Function to validate date input
def get_valid_date(prompt):
    while True:
        date_input = input(f"📅 {prompt}").strip()
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("❌ Invalid date format. Please enter a date in YYYY-MM-DD format.")

# Main menu function with emoji labels
def pesticide_medicine_menu(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    if not farmer_subfolder:
        print("🚫 Farmer folder not created, exiting pesticide/medicine management.")
        return

    load_pesticide_medicine(farmer_subfolder)

    while True:
        print(f"\033[92m🌱~~ Pesticide & Medicine Management - Farmer {farmer_name} ~~🌱\033[0m")
        options = {
            "🌿 Add Pesticide/Medicine": add_pesticide_medicine,
            "✏️ Edit Pesticide/Medicine": edit_pesticide_medicine,
            "👀 View Pesticides/Medicines": view_pesticide_medicine,
            "🗑️ Delete Pesticide/Medicine": delete_pesticide_medicine,
            "🚪 Quit Pesticide/Medicine Management": None
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
                    if selected_function == view_pesticide_medicine:
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

# Load function with a message for clarity
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
                        'Supplier Cost': float(data[10]),
                        'Notes': data[11] if len(data) > 11 else ""
                    }
                except ValueError as e:
                    print(f"⚠️ Error loading pesticide/medicine data: {e}. Skipping line.")
        print("✅ Pesticides/Medicines loaded successfully.")
    else:
        print("📂 No pesticide/medicine file found. Starting with an empty list.")

# Save function with emoji notification
def save_pesticide_medicine(farmer_subfolder):
    file_path = os.path.join(farmer_subfolder, 'pesticide_medicine.txt')
    with open(file_path, 'w') as file:
        for pestmed_id, data in pesticideMedicine.items():
            scheduled_date = data['Scheduled Date'].strftime("%Y-%m-%d")
            application_date = data['Application Date'].strftime("%Y-%m-%d")
            file.write(
                f"{pestmed_id},{scheduled_date},{application_date},{data['Disease/Pests']},{data['Crop Applied to']},"
                f"{data['Name']},{data['Variety']},{data['Field']},{data['Area']},{data['Quantity']},{data['Supplier Cost']},{data['Notes']}\n")
    print("💾 Pesticide/Medicine data saved successfully.")

# Add pesticide/medicine function with prompts and emojis
def add_pesticide_medicine(farmer_subfolder, farmer_name):
    print("🌱~~ Adding New Pesticide/Medicine ~~🌱")
    try:
        pestmed_id = int(input("🔢 Please enter a unique pesticide/medicine ID: "))
        if pestmed_id in pesticideMedicine:
            print(f"⚠️ Pesticide/Medicine with ID '{pestmed_id}' already exists!")
            return
    except ValueError:
        print("❌ Invalid ID. It should be numeric.")
        return

    scheduled_date = get_valid_date("Enter the scheduled date for pesticide/medicine use (YYYY-MM-DD): ")
    application_date = get_valid_date("Enter the actual application date (YYYY-MM-DD): ")
    disease_pests = get_non_empty_input("🦠 Enter the disease or pests targeted by this pesticide/medicine: ")
    crop_name = get_non_empty_input("🌾 Enter the crop this pesticide/medicine is applied to: ")
    name = get_non_empty_input("💊 Enter the pesticide/medicine name: ")
    variety = get_non_empty_input("🌿 Enter the pesticide/medicine variety/type: ")
    field = get_non_empty_input("📍 Enter the field or location: ")

    try:
        area = int(get_non_empty_input("📏 Enter the area covered in hectares: "))
        quantity = int(get_non_empty_input("⚖️ Enter the quantity used in kg: "))
    except ValueError:
        print("❌ Invalid input for area or quantity.")
        return

    try:
        supplier_cost_php = float(get_non_empty_input("💰 Enter the supplier cost for the pesticide/medicine (in PHP): "))
    except ValueError:
        print("❌ Invalid input for supplier cost. Please enter a valid number.")
        return

    notes = input("📝 [Optional] Additional notes: ").strip()

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
        'Supplier Cost': supplier_cost_php,
        'Notes': notes
    }

    save_pesticide_medicine(farmer_subfolder)
    print("✅ Pesticide/Medicine added successfully.")

# Edit function with user feedback for each field
def edit_pesticide_medicine(farmer_subfolder, farmer_name):
    print("🌱~~ Editing Pesticide/Medicine ~~🌱")
    view_pesticide_medicine(farmer_name)
    try:
        pestmed_id = int(input("✏️ Enter the pesticide/medicine ID to edit: "))
        if pestmed_id not in pesticideMedicine:
            print("🚫 Pesticide/Medicine not found.")
            return

        current_data = pesticideMedicine[pestmed_id]
        scheduled_date = get_valid_date("Enter the new scheduled date (YYYY-MM-DD) or press Enter to keep the current date: ")
        pesticideMedicine[pestmed_id]['Scheduled Date'] = scheduled_date if scheduled_date else current_data['Scheduled Date']

        application_date = get_valid_date("Enter the new application date (YYYY-MM-DD) or press Enter to keep the current date: ")
        pesticideMedicine[pestmed_id]['Application Date'] = application_date if application_date else current_data['Application Date']

        disease_pests = input(f"🦠 Disease or pests targeted [{current_data['Disease/Pests']}]: ").strip()
        pesticideMedicine[pestmed_id]['Disease/Pests'] = disease_pests if disease_pests else current_data['Disease/Pests']

        crop_name = input(f"🌾 Crop applied to [{current_data['Crop Applied to']}]: ").strip()
        pesticideMedicine[pestmed_id]['Crop Applied to'] = crop_name if crop_name else current_data['Crop Applied to']

        name = input(f"💊 Pesticide/Medicine name [{current_data['Name']}]: ").strip()
        pesticideMedicine[pestmed_id]['Name'] = name if name else current_data['Name']

        variety = input(f"🌿 Variety/type [{current_data['Variety']}]: ").strip()
        pesticideMedicine[pestmed_id]['Variety'] = variety if variety else current_data['Variety']

        field = input(f"📍 Field/location [{current_data['Field']}]: ").strip()
        pesticideMedicine[pestmed_id]['Field'] = field if field else current_data['Field']

        try:
            area = int(input(f"📏 Area covered (current: {current_data['Area']}): "))
            pesticideMedicine[pestmed_id]['Area'] = area
        except ValueError:
            print("❌ Invalid area. Keeping current value.")
            pesticideMedicine[pestmed_id]['Area'] = current_data['Area']

        try:
            quantity = int(input(f"⚖️ Quantity used (current: {current_data['Quantity']}): "))
            pesticideMedicine[pestmed_id]['Quantity'] = quantity
        except ValueError:
            print("❌ Invalid quantity. Keeping current value.")
            pesticideMedicine[pestmed_id]['Quantity'] = current_data['Quantity']

        try:
            supplier_cost = float(input(f"💰 Supplier cost (current: {current_data['Supplier Cost']}): "))
            pesticideMedicine[pestmed_id]['Supplier Cost'] = supplier_cost
        except ValueError:
            print("❌ Invalid cost. Keeping current value.")
            pesticideMedicine[pestmed_id]['Supplier Cost'] = current_data['Supplier Cost']

        notes = input(f"📝 Additional notes (current: {current_data['Notes']}): ").strip()
        pesticideMedicine[pestmed_id]['Notes'] = notes if notes else current_data['Notes']

        save_pesticide_medicine(farmer_subfolder)
        print("✅ Pesticide/Medicine edited successfully.")

    except ValueError:
        print("❌ Invalid ID entered.")

# View function to list all pesticide/medicine
def view_pesticide_medicine(farmer_name):
    print("🌿 Pesticides/Medicines List:")
    if not pesticideMedicine:
        print("🚫 No pesticides/medicines available.")
        return
    headers = ["ID", "Scheduled Date", "Application Date", "Disease/Pests", "Crop", "Name", "Variety", "Field", "Area", "Quantity", "Cost", "Notes"]
    table_data = [
        [
            pestmed_id,
            data["Scheduled Date"].strftime("%Y-%m-%d"),
            data["Application Date"].strftime("%Y-%m-%d"),
            data["Disease/Pests"],
            data["Crop Applied to"],
            data["Name"],
            data["Variety"],
            data["Field"],
            data["Area"],
            data["Quantity"],
            data["Supplier Cost"],
            data["Notes"]
        ]
        for pestmed_id, data in pesticideMedicine.items()
    ]
    print(tabulate(table_data, headers, tablefmt="fancy_grid"))

# 🗑️ Function to delete a pesticide/medicine
def delete_pesticide_medicine(farmer_subfolder, farmer_name):
    print("\033[92m🛑~~ Deleting Pesticide/Medicine ~~\033[0m")

    # Display the list of all pesticide/medicine records for the farmer
    view_pesticide_medicine(farmer_name)

    try:
        pestmed_id = int(input("\033[93m🔢 Enter the pesticide/medicine ID to delete: \033[0m"))
    except ValueError:
        print("\033[91m🚫 Invalid ID. Please enter a numeric value.\033[0m")
        return

    if pestmed_id not in pesticideMedicine:
        print(f"\033[91m🚫 No pesticide/medicine found with ID '{pestmed_id}'. Please check the ID and try again.\033[0m")
        return

    # Get the name of the pesticide/medicine to log the removal
    pestmed_name = pesticideMedicine[pestmed_id]['Name']

    # Confirm deletion
    confirmation = input(f"\033[94mAre you sure you want to delete pesticide/medicine with ID '{pestmed_id}'? (y/n): \033[0m").strip().lower()
    if confirmation == 'y':
        # Log the removal before deleting
        pesticide_medicine_removal_log(farmer_subfolder, pestmed_id, pestmed_name, farmer_name)

        # Delete the pesticide/medicine from the list
        del pesticideMedicine[pestmed_id]
        save_pesticide_medicine(farmer_subfolder)

        print(f"\033[92m✅ Pesticide/Medicine with ID '{pestmed_id}' has been deleted.\033[0m")
    else:
        print("\033[93m❌ Deletion cancelled.\033[0m")

# 📝 Function to log pesticide/medicine removal
def pesticide_medicine_removal_log(farmer_subfolder, pestmed_id, pestmed_name, farmer_name):
    # Define the path for the log file
    removal_log_file = os.path.join(farmer_subfolder, 'pesticide_medicine_removal_log.txt')

    # Append the removal log with the farmer's details
    with open(removal_log_file, 'a') as file: file.write(f"{farmer_name},Farmer,{datetime.now()},{pestmed_id},{pestmed_name}\n")
       

    # Notify that the removal has been logged successfully
    print("\033[92m✅ Removal logged successfully.\033[0m")


# Helper function to prompt non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("⚠️ This field cannot be empty.")

