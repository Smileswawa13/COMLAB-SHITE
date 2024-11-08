from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# 🌱 Global crops dictionary to store crop data
crops = {}

# 📅 Function to validate the date input
def get_valid_date():
    while True:
        date_input = input("📅 Enter the date the crop was planted in this format (YYYY-MM-DD): ")
        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            return valid_date
        except ValueError:
            print("🚫 Invalid date format. Please enter a valid date in the format YYYY-MM-DD.")

# 💵 Function to validate supplier cost input
def get_valid_supplier_cost():
    while True:
        try:
            supplier_cost = float(input("💵 Enter the supplier cost per kilogram in PHP: "))
            if supplier_cost < 0:
                print("🚫 Cost cannot be negative. Please enter a valid amount.")
            else:
                return supplier_cost
        except ValueError:
            print("🚫 Invalid input. Please enter a valid number for the supplier cost.")

# 🌾 Function for the main crop management menu
def crop_menu(farmer_name):
    # 🔍 Get the farmer's subfolder path by calling make_farmer_folder
    farmer_subfolder = make_farmer_folder(farmer_name)

    if not farmer_subfolder:
        print("🚫 Farmer folder not created, exiting crop management.")
        return

    # 🗂️ Load crops from the file
    load_crops(farmer_subfolder)

    while True:
        print(f"🌾~~Crop Management - Farmer {farmer_name}~~🌾")
        options = {
            "🌱 Add Crops": add_crops,
            "✏️ Edit Crops": edit_crops,
            "📜 View Crops": view_crops,
            "❌ Delete Crops": delete_crops,
            "🔙 Quit Crop Management": None
        }

        for index, (action, key) in enumerate(options.items(), 1):
            print(f"{index}. {action}")
        print(f"🔄 Which do you want to do, farmer {farmer_name}?")

        try:
            action = int(input("Enter here using the corresponding number: "))

            if 1 <= action <= 4:
                selected_action = list(options.keys())[action - 1]
                selected_function = options[selected_action]
                print(f"▶️ Executing...'{selected_action}'.")

                if callable(selected_function):
                    # 🔑 Check if the crop function has an argument
                    if selected_function == view_crops:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)

            elif action == 5:
                print("🚪 Going Back to Main Menu")
                break

            else:
                print("🚫 Your input is not in the corresponding choices. Please enter a valid number between 1 and 5.")
        except ValueError:
            print("🚫 Please enter a valid number.")

# 📂 Function to load crops from a file
def load_crops(farmer_subfolder):
    crops_file_path = os.path.join(farmer_subfolder, 'crops.txt')

    if os.path.exists(crops_file_path):
        with open(crops_file_path, 'r') as file:
            for line in file:
                crop_data = line.strip().split(",")
                try:
                    crop_id = int(crop_data[0])
                    crops[crop_id] = {
                        'Date planted:': datetime.strptime(crop_data[1], "%Y-%m-%d"),
                        'Name of Crop:': crop_data[2],
                        'Variety:': crop_data[3],
                        'Field:': crop_data[4],
                        'Area:': int(crop_data[5]),
                        'Quantity': int(crop_data[6]),
                        'Notes': crop_data[7],
                        'Supplier Cost (PHP)': float(crop_data[8])  # New field for supplier cost
                    }
                except ValueError as e:
                    print(f"🚫 Error loading crop data: {e}. Skipping line.")
        print("✅ Crops loaded successfully.")
    else:
        print("⚠️ No crops file found. Starting with an empty list.")

# 💾 Function to save crops into the file
def save_crops(farmer_subfolder):
    crops_file_path = os.path.join(farmer_subfolder, 'crops.txt')

    with open(crops_file_path, 'w') as file:
        for crop_id, crop_data in crops.items():
            formatted_date = crop_data['Date planted:'].strftime("%Y-%m-%d")
            file.write(f"{crop_id},{formatted_date},{crop_data['Name of Crop:']},"
                       f"{crop_data['Variety:']},{crop_data['Field:']},{crop_data['Area:']},"
                       f"{crop_data['Quantity']},{crop_data['Notes']},{crop_data['Supplier Cost (PHP)']}\n")
    print("✅ Crops saved successfully.")

# 🌱 Function to add crops
def add_crops(farmer_subfolder, farmer_name):
    print("🌾~~ Adding new crop ~~")
    try:
        crop_id = int(input("🔢 Please enter the crop id: "))
    except ValueError:
        print("🚫 Invalid crop ID. It should be a numeric value.")
        return

    if crop_id in crops:
        print(f"🚫 Crop with ID '{crop_id}' already exists!")
        return

    crop_date = get_valid_date()  # 📅 This returns a datetime object
    crop_name = get_non_empty_input("🌱 Please enter the crop name: ").strip()
    crop_variety = get_non_empty_input("🌾 Please enter the crop variety: ").strip()
    crop_field = get_non_empty_input("📍 Please enter in which field the crop was planted: ").strip()

    while True:
        try:
            crop_area = int(input("📏 Please enter the area planted in hectares: ").strip())
            crop_quantity = int(input("🌾 Please enter the amount of seeds planted in kilograms: ").strip())
            break
        except ValueError:
            print("🚫 Invalid amount input. Please enter numeric values for area and quantity.")

    crop_notes = input("[Optional] 📝 Please enter any additional notes about the crop: ").strip()

    # 💵 Get the supplier cost for the crop
    supplier_cost = get_valid_supplier_cost()

    crops[crop_id] = {
        'Date planted:': crop_date,
        'Name of Crop:': crop_name,
        'Variety:': crop_variety,
        'Field:': crop_field,
        'Area:': crop_area,
        'Quantity': crop_quantity,
        'Notes': crop_notes,
        'Supplier Cost (PHP)': supplier_cost
    }

    save_crops(farmer_subfolder)
    print("✅ Your crop has been added!")

# 🌿 Function to view all crops
def view_crops(farmer_name):
    try:
        farmer_subfolder = make_farmer_folder(farmer_name)
        if farmer_subfolder:
            load_crops(farmer_subfolder)
        else:
            print("🚫 Farmer folder not found. Exiting crop management.")
            return
    except Exception as e:
        print(f"🚫 Error loading crops: {e}")
        return

    print("🌾~~ All Crops ~~")

    if not crops:
        print("🚫 No crops found.")
        return

    headers = ["Crop ID", "Date of Planting", "Name of Crop", "Variety", "Field", "Area Planted (hectares)",
               "Quantity (kg)", "Notes", "Supplier Cost (PHP)"]

    table_data = []

    for crop_id, details in crops.items():
        try:
            formatted_date = details['Date planted:'].strftime("%Y-%m-%d")

            row = [
                crop_id,
                formatted_date,
                details['Name of Crop:'],
                details['Variety:'],
                details['Field:'],
                details['Area:'],
                details['Quantity'],
                details['Notes'] if details['Notes'] else "No notes",
                details['Supplier Cost (PHP)']
            ]
            table_data.append(row)
        except KeyError as e:
            print(f"🚫 Error: Missing key {e} in crop ID {crop_id}. Skipping crop.")
            continue

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# ✏️ Function to edit crop data
def edit_crops(farmer_subfolder, farmer_name):
    view_crops(farmer_name)
    try:
        crop_id = int(input("🔢 Enter the crop ID to edit: "))
        if crop_id not in crops:
            print("🚫 Crop not found.")
            return

        current_data = crops[crop_id]

        crop_name = input(f"✏️ Enter the new crop name [{current_data['Name of Crop:']}]: ").strip()
        crops[crop_id]['Name of Crop:'] = crop_name if crop_name else current_data['Name of Crop:']

        crop_variety = input(f"✏️ Enter the new crop variety [{current_data['Variety:']}]: ").strip()
        crops[crop_id]['Variety:'] = crop_variety if crop_variety else current_data['Variety:']

        field = input(f"✏️ Enter the new field [{current_data['Field:']}]: ").strip()
        crops[crop_id]['Field:'] = field if field else current_data['Field:']

        while True:
            try:
                area = input(f"✏️ Enter the new area planted [{current_data['Area:']} hectares]: ").strip()
                area = int(area) if area else current_data['Area:']
                crops[crop_id]['Area:'] = area
                break
            except ValueError:
                print("🚫 Invalid input for area, it should be numeric.")

        while True:
            try:
                quantity = input(f"✏️ Enter the new quantity planted [{current_data['Quantity']} kg]: ").strip()
                quantity = int(quantity) if quantity else current_data['Quantity']
                crops[crop_id]['Quantity'] = quantity
                break
            except ValueError:
                print("🚫 Invalid input for quantity, it should be numeric.")

        save_crops(farmer_subfolder)
        print("✅ Crop data has been updated successfully.")
    except ValueError:
        print("🚫 Invalid crop ID. Please enter a valid numeric crop ID.")

# ❌ Function to delete a crop
def delete_crops(farmer_subfolder, farmer_name):
    view_crops(farmer_name)
    try:
        crop_id = int(input("🔢 Enter the crop ID to delete: "))
        if crop_id not in crops:
            print("🚫 Crop not found.")
            return

        del crops[crop_id]
        save_crops(farmer_subfolder)
        print("✅ Crop deleted successfully.")
    except ValueError:
        print("🚫 Invalid crop ID. Please enter a valid numeric crop ID.")

# 🗑️ Function to log crop removal
def log_crop_removal(farmer_subfolder, crop_id, crop_name, farmer_name):
    removal_log_file = os.path.join(farmer_subfolder, 'crop_removal_log.txt')

    if not os.path.exists(removal_log_file):
        with open(removal_log_file, 'w') as file:
            file.write("Username,Role,Removed Date,Crop ID,Crop Name\n")

    with open(removal_log_file, 'a') as file:
        file.write(f"{farmer_name},Farmer,{datetime.now()},{crop_id},{crop_name}\n")
    print("✅ Removal logged successfully.")

# 📝 Function to get non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("🚫 Input cannot be empty. Please enter a valid value.")

