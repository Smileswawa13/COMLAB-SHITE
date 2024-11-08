from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# 🌱 Global fertilizer dictionary to store fertilizer data
fertilizer = {}

# 🗓 Function to validate date input
def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")  # ✅ Returns the valid date
        except ValueError:
            print("❌ Invalid date format. Please enter a date in YYYY-MM-DD format.")

# 💡 Function for the main fertilizer management menu
def fertilizer_menu(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)  # 📂 Get the farmer's folder
    if not farmer_subfolder:
        print("❌ Farmer folder not created, exiting fertilizer management.")
        return

    load_fertilizer(farmer_subfolder)  # 🗂 Load existing fertilizers

    while True:
        print(f"~~ Fertilizer Management - Farmer {farmer_name} ~~")
        options = {
            "🌿 Add Fertilizer": add_fertilizer,
            "✏️ Edit Fertilizer": edit_fertilizer,
            "📜 View Fertilizers": view_fertilizer,
            "❌ Delete Fertilizer": delete_fertilizer,
            "🔙 Quit Fertilizer Management": None
        }

        for index, action in enumerate(options, 1):
            print(f"{index}. {action}")

        try:
            action = int(input("Enter the corresponding number: "))
            if 1 <= action <= 4:
                selected_function = list(options.values())[action - 1]
                if callable(selected_function):
                    if selected_function == view_fertilizer:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)
            elif action == 5:
                print("👋 Exiting Fertilizer Management")
                break
            else:
                print("❌ Invalid choice. Choose between 1 and 5.")
        except ValueError:
            print("❌ Please enter a valid number.")

# 📑 Function to load fertilizer data from a file
def load_fertilizer(farmer_subfolder):
    fertilizer_file_path = os.path.join(farmer_subfolder, 'fertilizer.txt')
    if os.path.exists(fertilizer_file_path):
        with open(fertilizer_file_path, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                try:
                    fert_id = int(data[0])
                    # Safely handle Supplier Cost (set to 0.0 if invalid or empty)
                    supplier_cost = 0.0
                    if data[10] and data[10] != 'N/A':  # Check if it's not empty or 'N/A'
                        try:
                            supplier_cost = float(data[10])
                        except ValueError:
                            print(
                                f"❌ Oops! Invalid supplier cost value for Fertilizer ID {fert_id}. Setting it to 0.0 🌱💸")

                    fertilizer[fert_id] = {
                        'Scheduled Date': datetime.strptime(data[1], "%Y-%m-%d"),
                        'Application Date': datetime.strptime(data[2], "%Y-%m-%d"),
                        'Crop Applied to': data[3],
                        'Name': data[4],
                        'Variety': data[5],
                        'Field': data[6],
                        'Area': int(data[7]),
                        'Quantity': int(data[8]),
                        'Supplier Cost': supplier_cost,  # Safely assign supplier cost
                        'Notes': data[11] if len(data) > 11 else ""
                    }
                except ValueError as e:
                    print(f"❌ Error loading fertilizer data for line: {e}. Skipping this one... 😓")
        print("✅ Fertilizers loaded successfully! Your digital farm is ready to go! 🌾🚜")
    else:
        print("🚨 No fertilizer file found. Starting with an empty list. Please check your files! 📂❌")


# 💾 Function to save fertilizer data to a file
def save_fertilizer(farmer_subfolder):
    fertilizer_file_path = os.path.join(farmer_subfolder, 'fertilizer.txt')
    with open(fertilizer_file_path, 'w') as file:
        for fert_id, data in fertilizer.items():
            scheduled_date = data['Scheduled Date'].strftime("%Y-%m-%d")
            application_date = data['Application Date'].strftime("%Y-%m-%d")
            supplier_cost = data.get('Supplier Cost', 'N/A')
            file.write(
                f"{fert_id},{scheduled_date},{application_date},{data['Crop Applied to']},{data['Name']},"
                f"{data['Variety']},{data['Field']},{data['Area']},{data['Quantity']},{supplier_cost},{data['Notes']}\n")
    print("✅ Fertilizer data saved successfully.")

# ➕ Function to add fertilizer data
def add_fertilizer(farmer_subfolder, farmer_name):
    print("~~ Adding New Fertilizer ~~")
    try:
        fert_id = int(input("Please enter a unique fertilizer ID: "))
        if fert_id in fertilizer:
            print(f"❌ Fertilizer with ID '{fert_id}' already exists!")
            return
    except ValueError:
        print("❌ Invalid ID. It should be numeric.")
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
        print("❌ Invalid input for area or quantity.")
        return

    fert_notes = input("[Optional] Additional notes: ").strip()

    try:
        supplier_cost = float(input("Enter the supplier cost per kg (in PHP): ").strip())  # 💵 Specify PHP
    except ValueError:
        print("❌ Invalid supplier cost. It should be a numeric value.")
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
        'Supplier Cost': supplier_cost  # 💰 Added supplier cost
    }

    save_fertilizer(farmer_subfolder)
    print("✅ Fertilizer added successfully.")

# 📝 Function to edit fertilizer data
def edit_fertilizer(farmer_subfolder, farmer_name):
    view_fertilizer(farmer_name)
    try:
        fert_id = int(input("Enter the fertilizer ID to edit: "))
        if fert_id not in fertilizer:
            print("❌ Fertilizer not found.")
            return

        current_data = fertilizer[fert_id]  # 📜 Retrieve current data

        # Prompt user for new values with the option to keep current ones
        scheduled_date = get_valid_date("Enter the new scheduled date (YYYY-MM-DD) or press Enter to keep the current date: ")
        fertilizer[fert_id]['Scheduled Date'] = scheduled_date if scheduled_date else current_data['Scheduled Date']

        # Other fields follow the same structure...
        # (Continue with similar prompts for other fields)

        save_fertilizer(farmer_subfolder)
        print(f"✅ Fertilizer ID {fert_id} edited successfully.")
    except ValueError:
        print("❌ Invalid ID.")

# 👀 Function to view all fertilizers
def view_fertilizer(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_fertilizer(farmer_subfolder)

    if not fertilizer:
        print("❌ No fertilizers found.")
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
            f"₱ {data['Supplier Cost']:.2f}",
            data['Notes']
        ]
        table_data.append(row)

    print(tabulate(table_data, headers, tablefmt="fancy_grid"))

# 🗑 Function to delete fertilizer
def delete_fertilizer(farmer_subfolder, farmer_name):
    view_fertilizer(farmer_name)
    try:
        fert_id = int(input("Enter the fertilizer ID to delete: "))
        if fert_id not in fertilizer:
            print("❌ Fertilizer not found.")
            return

        confirm = input(f"Are you sure you want to delete fertilizer ID {fert_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            log_fertilizer_removal(farmer_subfolder, fert_id)
            del fertilizer[fert_id]
            save_fertilizer(farmer_subfolder)
            print(f"✅ Fertilizer ID {fert_id} deleted successfully.")
        else:
            print("❌ Deletion canceled.")
    except ValueError:
        print("❌ Invalid fertilizer ID.")

# 📜 Function to log fertilizer removal
def log_fertilizer_removal(farmer_subfolder, fert_id):
    log_file_path = os.path.join(farmer_subfolder, "fertilizer_removal_log.txt")
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{fert_id},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"✅ Fertilizer ID {fert_id} removal logged.")
