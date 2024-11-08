from datetime import datetime
from tabulate import tabulate
import os
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
        print(f"\n🌱~~ Pesticide & Medicine Management - Farmer {farmer_name} ~~🌱")
        options = {
            "🌿 Add Pesticide/Medicine": add_pesticide_medicine,
            "✏️ Edit Pesticide/Medicine": edit_pesticide_medicine,
            "👀 View Pesticides/Medicines": view_pesticide_medicine,
            "🗑️ Delete Pesticide/Medicine": delete_pesticide_medicine,
            "🚪 Quit Pesticide/Medicine Management": None
        }

        for index, action in enumerate(options, 1):
            print(f"{index}. {action}")

        try:
            action = int(input("📋 Enter here using the corresponding number: "))
            if 1 <= action <= 4:
                selected_function = list(options.values())[action - 1]
                if callable(selected_function):
                    if selected_function == view_pesticide_medicine:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)
            elif action == 5:
                print("🔙 Exiting Pesticide & Medicine Management")
                break
            else:
                print("❌ Invalid choice. Choose between 1 and 5.")
        except ValueError:
            print("❌ Please enter a valid number.")

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

        name = input(f"💊 Pesticide/medicine name [{current_data['Name']}]: ").strip()
        pesticideMedicine[pestmed_id]['Name'] = name if name else current_data['Name']

        variety = input(f"🌿 Variety/type [{current_data['Variety']}]: ").strip()
        pesticideMedicine[pestmed_id]['Variety'] = variety if variety else current_data['Variety']

        field = input(f"📍 Field/location [{current_data['Field']}]: ").strip()
        pesticideMedicine[pestmed_id]['Field'] = field if field else current_data['Field']

        try:
            area = input(f"📏 Area in hectares [{current_data['Area']}]: ").strip()
            pesticideMedicine[pestmed_id]['Area'] = int(area) if area else current_data['Area']
        except ValueError:
            print("❌ Invalid input for area. Keeping current value.")

        try:
            quantity = input(f"⚖️ Quantity in kg [{current_data['Quantity']}]: ").strip()
            pesticideMedicine[pestmed_id]['Quantity'] = int(quantity) if quantity else current_data['Quantity']
        except ValueError:
            print("❌ Invalid input for quantity. Keeping current value.")

        try:
            supplier_cost_php = input(f"💰 Supplier cost in PHP [{current_data['Supplier Cost']}]: ").strip()
            pesticideMedicine[pestmed_id]['Supplier Cost'] = float(supplier_cost_php) if supplier_cost_php else current_data['Supplier Cost']
        except ValueError:
            print("❌ Invalid input for supplier cost. Keeping current value.")

        notes = input(f"📝 Additional notes [{current_data['Notes']}]: ").strip()
        pesticideMedicine[pestmed_id]['Notes'] = notes if notes else current_data['Notes']

        save_pesticide_medicine(farmer_subfolder)
        print("✅ Pesticide/Medicine updated successfully.")

    except ValueError:
        print("❌ Invalid pesticide/medicine ID.")

# Display function with formatted currency and a table layout
def view_pesticide_medicine(farmer_name):
    if pesticideMedicine:
        headers = ["ID", "Scheduled Date", "Application Date", "Disease/Pests", "Crop", "Name", "Variety", "Field", "Area (Ha)", "Quantity (kg)", "Supplier Cost (PHP)", "Notes"]
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
                f"₱{data['Supplier Cost']:.2f}",
                data["Notes"]
            ]
            for pestmed_id, data in pesticideMedicine.items()
        ]
        print(tabulate(table_data, headers, tablefmt="grid"))
    else:
        print("🔍 No pesticide/medicine records found.")

# Delete function with confirmation and logging
def delete_pesticide_medicine(farmer_subfolder, farmer_name):
    view_pesticide_medicine(farmer_name)
    try:
        pestmed_id = int(input("🗑️ Enter the ID of the pesticide/medicine to delete: "))
        if pestmed_id in pesticideMedicine:
            log_pesticide_medicine_removal(farmer_subfolder, pestmed_id, pesticideMedicine[pestmed_id])
            del pesticideMedicine[pestmed_id]
            save_pesticide_medicine(farmer_subfolder)
            print("✅ Pesticide/Medicine deleted successfully.")
        else:
            print("🚫 Pesticide/Medicine ID not found.")
    except ValueError:
        print("❌ Invalid pesticide/medicine ID.")

# Helper function to log deletions
def log_pesticide_medicine_removal(farmer_subfolder, pestmed_id, data):
    log_file_path = os.path.join(farmer_subfolder, "pesticide_medicine_removal_log.txt")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"🗑️ {datetime.now()} - Deleted Pesticide/Medicine ID: {pestmed_id}\nDetails: {data}\n\n")
    print("📝 Deletion logged successfully.")

# Helper function to prompt non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("⚠️ This field cannot be empty.")

