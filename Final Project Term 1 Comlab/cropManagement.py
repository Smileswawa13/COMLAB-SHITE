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
        print("\033[91m🚫 Farmer folder not created, exiting crop management.\033[0m")
        return

    # 🗂️ Load crops from the file
    load_crops(farmer_subfolder)

    while True:
        print(f"\033[92m🌾~~Crop Management - Farmer {farmer_name}~~🌾\033[0m")
        options = {
            "🌱 Add Crops": add_crops,
            "✏️ Edit Crops": edit_crops,
            "📜 View Crops": view_crops,
            "❌ Delete Crops": delete_crops,
            "🔙 Quit Crop Management": None
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
                    if selected_function == view_crops:
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
        print("\033[92m✅ Crops loaded successfully.\033[0m")
    else:
        print("\033[93m⚠️ No crops file found. Starting with an empty list.\033[0m")

# 💾 Function to save crops into the file
def save_crops(farmer_subfolder):
    crops_file_path = os.path.join(farmer_subfolder, 'crops.txt')

    with open(crops_file_path, 'w') as file:
        for crop_id, crop_data in crops.items():
            formatted_date = crop_data['Date planted:'].strftime("%Y-%m-%d")
            file.write(f"{crop_id},{formatted_date},{crop_data['Name of Crop:']},"
                       f"{crop_data['Variety:']},{crop_data['Field:']},{crop_data['Area:']},"
                       f"{crop_data['Quantity']},{crop_data['Notes']},{crop_data['Supplier Cost (PHP)']}\n")
    print("\033[92m✅ Crops saved successfully.\033[0m")

# 🌱 Function to add crops
def add_crops(farmer_subfolder, farmer_name):
    print("\033[92m🌾~~ Adding new crop ~~\033[0m")
    try:
        crop_id = int(input("\033[93m🔢 Please enter the crop id: \033[0m"))
    except ValueError:
        print("\033[91m🚫 Invalid crop ID. It should be a numeric value.\033[0m")
        return

    if crop_id in crops:
        print(f"\033[91m🚫 Crop with ID '{crop_id}' already exists!\033[0m")
        return

    crop_date = get_valid_date()  # 📅 This returns a datetime object
    crop_name = get_non_empty_input("\033[94m🌱 Please enter the crop name: \033[0m").strip()
    crop_variety = get_non_empty_input("\033[94m🌾 Please enter the crop variety: \033[0m").strip()
    crop_field = get_non_empty_input("\033[94m📍 Please enter in which field the crop was planted: \033[0m").strip()

    while True:
        try:
            crop_area = int(input("\033[94m📏 Please enter the area planted in hectares: \033[0m").strip())
            crop_quantity = int(input("\033[94m🌾 Please enter the amount of seeds planted in kilograms: \033[0m").strip())
            break
        except ValueError:
            print("\033[91m🚫 Invalid amount input. Please enter numeric values for area and quantity.\033[0m")

    crop_notes = input("\033[92m[Optional] 📝 Please enter any additional notes about the crop: \033[0m").strip()

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
    print("\033[92m✅ Your crop has been added!\033[0m")

# 🌿 Function to view all crops
def view_crops(farmer_name):
    try:
        farmer_subfolder = make_farmer_folder(farmer_name)
        if farmer_subfolder:
            load_crops(farmer_subfolder)
        else:
            print("\033[91m🚫 Farmer folder not found. Exiting crop management.\033[0m")
            return
    except Exception as e:
        print(f"\033[91m🚫 Error loading crops: {e}\033[0m")
        return

    print("\033[92m🌾~~ All Crops ~~\033[0m")

    if not crops:
        print("\033[91m🚫 No crops found.\033[0m")
        return

    headers = ["Crop ID", "Date of Planting", "Name of Crop", "Variety", "Field", "Area Planted (hectares)", "Quantity (kg)", "Notes", "Supplier Cost (PHP)"]
    table = []

    for crop_id, crop_data in crops.items():
        table.append([crop_id,
                      crop_data['Date planted:'].strftime("%Y-%m-%d"),
                      crop_data['Name of Crop:'],
                      crop_data['Variety:'],
                      crop_data['Field:'],
                      crop_data['Area:'],
                      crop_data['Quantity'],
                      crop_data['Notes'],
                      crop_data['Supplier Cost (PHP)']])

    print(tabulate(table, headers, tablefmt="fancy_grid"))

# ✏️ Function to edit crop details
def edit_crops(farmer_subfolder, farmer_name):
    print("\033[92m🌾~~ Editing crop ~~\033[0m")

    try:
        crop_id = int(input("\033[93m🔢 Enter the crop ID to edit: \033[0m"))
    except ValueError:
        print("\033[91m🚫 Invalid crop ID. Please enter a numeric value.\033[0m")
        return

    if crop_id not in crops:
        print(f"\033[91m🚫 No crop found with ID '{crop_id}'. Please check the ID and try again.\033[0m")
        return

    crop = crops[crop_id]
    print(f"\033[92m🌾 Editing crop with ID: {crop_id} 🌾\033[0m")
    print(f"\033[94mCurrent details for crop '{crop['Name of Crop:']}':\033[0m")
    print(f"\033[94mDate planted: {crop['Date planted:'].strftime('%Y-%m-%d')}\033[0m")
    print(f"\033[94mVariety: {crop['Variety:']}\033[0m")
    print(f"\033[94mField: {crop['Field:']}\033[0m")
    print(f"\033[94mArea planted: {crop['Area:']} hectares\033[0m")
    print(f"\033[94mQuantity planted: {crop['Quantity']} kg\033[0m")
    print(f"\033[94mNotes: {crop['Notes']}\033[0m")
    print(f"\033[94mSupplier cost: PHP {crop['Supplier Cost (PHP)']}\033[0m")

    # 📝 Allow changes to specific fields
    crop_name = get_non_empty_input("\033[94m🌱 New crop name (leave empty to keep current): \033[0m").strip()
    crop_variety = get_non_empty_input("\033[94m🌾 New crop variety (leave empty to keep current): \033[0m").strip()
    crop_field = get_non_empty_input("\033[94m📍 New field (leave empty to keep current): \033[0m").strip()

    while True:
        try:
            crop_area = input("\033[94m📏 New area planted in hectares (leave empty to keep current): \033[0m").strip()
            crop_quantity = input("\033[94m🌾 New quantity planted in kilograms (leave empty to keep current): \033[0m").strip()

            if crop_area:
                crop_area = int(crop_area)
            else:
                crop_area = crop['Area:']

            if crop_quantity:
                crop_quantity = int(crop_quantity)
            else:
                crop_quantity = crop['Quantity']

            break
        except ValueError:
            print("\033[91m🚫 Invalid input for area or quantity. Please enter valid numeric values.\033[0m")

    crop_notes = input("\033[92m[Optional] 📝 New notes (leave empty to keep current): \033[0m").strip()

    # 💵 Update supplier cost if necessary
    supplier_cost = input("\033[92m💵 New supplier cost (leave empty to keep current): \033[0m").strip()
    if supplier_cost:
        try:
            supplier_cost = float(supplier_cost)
        except ValueError:
            print("\033[91m🚫 Invalid supplier cost. Keeping the current value.\033[0m")
            supplier_cost = crop['Supplier Cost (PHP)']
    else:
        supplier_cost = crop['Supplier Cost (PHP)']

    # Apply changes
    if crop_name:
        crop['Name of Crop:'] = crop_name
    if crop_variety:
        crop['Variety:'] = crop_variety
    if crop_field:
        crop['Field:'] = crop_field
    crop['Area:'] = crop_area
    crop['Quantity'] = crop_quantity
    if crop_notes:
        crop['Notes'] = crop_notes
    crop['Supplier Cost (PHP)'] = supplier_cost

    save_crops(farmer_subfolder)
    print("\033[92m✅ Crop details updated successfully!\033[0m")

# ❌ Function to delete a crop
def delete_crops(farmer_subfolder, farmer_name):
    print("\033[92m🌾~~ Deleting a crop ~~\033[0m")

    try:
        crop_id = int(input("\033[93m🔢 Enter the crop ID to delete: \033[0m"))
    except ValueError:
        print("\033[91m🚫 Invalid crop ID. Please enter a numeric value.\033[0m")
        return

    if crop_id not in crops:
        print(f"\033[91m🚫 No crop found with ID '{crop_id}'. Please check the ID and try again.\033[0m")
        return

    # Get the crop name to log the removal
    crop_name = crops[crop_id]['Name of Crop:']

    # Confirm deletion
    confirmation = input(f"\033[94mAre you sure you want to delete crop with ID '{crop_id}'? (y/n): \033[0m").strip().lower()
    if confirmation == 'y':
        # Log the removal before deleting
        crop_removal_log(farmer_subfolder, crop_id, crop_name, farmer_name)

        # Delete the crop from the crops dictionary
        del crops[crop_id]
        save_crops(farmer_subfolder)

        print(f"\033[92m✅ Crop with ID '{crop_id}' has been deleted.\033[0m")
    else:
        print("\033[93m❌ Deletion cancelled.\033[0m")

# 🗑️ Function to log crop removal
def crop_removal_log(farmer_subfolder, crop_id, crop_name, farmer_name):
    # Define the path for the log file
    removal_log_file = os.path.join(farmer_subfolder, 'crop_removal_log.txt')

    # Append the removal log with the farmer's details
    with open(removal_log_file, 'a') as file:
        file.write(f"{farmer_name},Farmer,{datetime.now()},{crop_id},{crop_name}\n")

    # Notify that the removal has been logged successfully
    print("\033[92m✅ Removal logged successfully.\033[0m")

# 📩 Function to handle non-empty inputs (for names, variety, etc.)
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("\033[91m🚫 Input cannot be empty. Please provide a valid input.\033[0m")

