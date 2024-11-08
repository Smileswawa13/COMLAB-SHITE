from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# Global dictionary to store sales records
sales = {}

# Function to validate date input
def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("🔴 Invalid date format. Please enter a date in YYYY-MM-DD format.")

# Function for the main sales menu
def sales_menu(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    if not farmer_subfolder:
        print("⚠️ Farmer folder not created, exiting sales management.")
        return

    load_sales(farmer_subfolder)

    while True:
        print(f"~~\033[92m💰 Sales Management - Farmer {farmer_name}  💰\033[0m~~")
        options = {
            "🌱 Add Sale": add_sale,
            "✏️ Edit Sale": edit_sale,
            "📊 View Sales": view_sales,
            "🗑️ Delete Sale": delete_sale,
            "🔙 Quit Management": None
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
                    if selected_function == view_sales:
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

# Function to load sales data from a file
def load_sales(farmer_subfolder):
    sales_file_path = os.path.join(farmer_subfolder, 'sales.txt')
    if os.path.exists(sales_file_path):
        with open(sales_file_path, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                try:
                    sale_id = int(data[0])
                    sales[sale_id] = {
                        'Sale Date': datetime.strptime(data[1], "%Y-%m-%d"),
                        'Crop Type': data[2],
                        'Quantity Sold': int(data[3]),
                        'Price per kg': float(data[4]),
                        'Total Sale': float(data[5]),
                        'Market Buyer': data[6],
                        'Notes': data[7] if len(data) > 7 else ""
                    }
                except ValueError as e:
                    print(f"⚠️ Error loading sale data: {e}. Skipping line.")
        print("✅ Sales loaded successfully.")
    else:
        print("📂 No sales file found. Starting with an empty list.")

# Function to save sales data to a file
def save_sales(farmer_subfolder):
    sales_file_path = os.path.join(farmer_subfolder, 'sales.txt')
    with open(sales_file_path, 'w') as file:
        for sale_id, data in sales.items():
            date = data['Sale Date'].strftime("%Y-%m-%d")
            file.write(f"{sale_id},{date},{data['Crop Type']},{data['Quantity Sold']},{data['Price per kg']},{data['Total Sale']},{data['Market Buyer']},{data['Notes']}\n")
    print("💾 Sales data saved successfully.")

# Function to add sale data
def add_sale(farmer_subfolder, farmer_name):
    print("~~ 🌱 Adding New Sale 🌱 ~~")
    try:
        sale_id = int(input("🔸 Please enter a unique sale ID: "))
        if sale_id in sales:
            print(f"❗ Sale with ID '{sale_id}' already exists!")
            return
    except ValueError:
        print("🔴 Invalid ID. It should be numeric.")
        return

    date = get_valid_date("📅 Enter the date of the sale (YYYY-MM-DD): ")
    crop_type = input("🌾 Enter the type of crop sold: ").strip()
    try:
        quantity_sold = int(input("📦 Enter the quantity sold (in kg): ").strip())
        sale_price = float(input("💵 Enter the price per kg: ").strip())
    except ValueError:
        print("🔴 Invalid input for quantity or price.")
        return

    sale_total = quantity_sold * sale_price
    sale_buyer = input("🛒 Enter the market buyer: ").strip()
    sale_notes = input("📝 [Optional] Additional notes: ").strip()

    sales[sale_id] = {
        'Sale Date': date,
        'Crop Type': crop_type,
        'Quantity Sold': quantity_sold,
        'Price per kg': sale_price,
        'Total Sale': sale_total,
        'Market Buyer': sale_buyer,
        'Notes': sale_notes
    }

    save_sales(farmer_subfolder)
    print("✅ Sale added successfully.")

# Function to edit sale data
def edit_sale(farmer_subfolder, farmer_name):
    view_sales(farmer_name)
    try:
        sale_id = int(input("🔸 Enter the sale ID to edit: "))
        if sale_id not in sales:
            print("⚠️ Sale not found.")
            return

        current_data = sales[sale_id]

        date = get_valid_date("📅 Enter the new date (YYYY-MM-DD) or press Enter to keep the current date: ")
        sales[sale_id]['Sale Date'] = date if date else current_data['Sale Date']

        crop_type = input(f"🌾 Enter the new crop type [{current_data['Crop Type']}]: ").strip()
        sales[sale_id]['Crop Type'] = crop_type if crop_type else current_data['Crop Type']

        quantity_sold = input(f"📦 Enter the new quantity sold [{current_data['Quantity Sold']}]: ").strip()
        if quantity_sold:
            try:
                sales[sale_id]['Quantity Sold'] = int(quantity_sold)
                sales[sale_id]['Total Sale'] = sales[sale_id]['Quantity Sold'] * sales[sale_id]['Price per kg']
            except ValueError:
                print("🔴 Invalid input for quantity. Keeping current value.")
        else:
            sales[sale_id]['Quantity Sold'] = current_data['Quantity Sold']

        sale_price = input(f"💵 Enter the new price per kg [{current_data['Price per kg']}]: ").strip()
        if sale_price:
            try:
                sales[sale_id]['Price per kg'] = float(sale_price)
                sales[sale_id]['Total Sale'] = sales[sale_id]['Quantity Sold'] * sales[sale_id]['Price per kg']
            except ValueError:
                print("🔴 Invalid input for price. Keeping current value.")
        else:
            sales[sale_id]['Price per kg'] = current_data['Price per kg']

        market_buyer = input(f"🛒 Enter the new market buyer [{current_data['Market Buyer']}]: ").strip()
        sales[sale_id]['Market Buyer'] = market_buyer if market_buyer else current_data['Market Buyer']

        notes = input(f"📝 [Optional] Additional notes [{current_data['Notes'] or 'No notes'}]: ").strip()
        sales[sale_id]['Notes'] = notes if notes else current_data['Notes']

        save_sales(farmer_subfolder)
        print(f"✅ Sale ID {sale_id} edited successfully.")
    except ValueError:
        print("🔴 Invalid ID.")

# Function to view all sales
def view_sales(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_sales(farmer_subfolder)

    if not sales:
        print("🚫 No sales found.")
        return

    headers = ["ID", "Date", "Crop Type", "Quantity Sold (kg)", "Price per kg", "Total Sale", "Market Buyer", "Notes"]
    table_data = []

    for sale_id, data in sales.items():
        row = [
            sale_id,
            data['Sale Date'].strftime("%Y-%m-%d"),
            data['Crop Type'],
            data['Quantity Sold'],
            f"₱{data['Price per kg']:.2f}",  # Display price in PHP
            f"₱{data['Total Sale']:.2f}",   # Display total sale in PHP
            data['Market Buyer'],
            data['Notes'] or "No notes"
        ]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to delete a sale with confirmation
def delete_sale(farmer_subfolder, farmer_name):
    view_sales(farmer_name)  # View the sales list
    try:
        sale_id = int(input("🔸 Enter the sale ID to delete: "))
        if sale_id in sales:
            crop_type = sales[sale_id]['Crop Type']

            confirmation = input(f"⚠️ Are you sure you want to delete sale ID {sale_id} for crop type '{crop_type}'? Type 'yes' to confirm: ").strip().lower()
            if confirmation == "yes":
                log_sale_removal(farmer_subfolder, sale_id, crop_type, farmer_name)
                del sales[sale_id]
                save_sales(farmer_subfolder)
                print(f"🗑️ Sale ID {sale_id} deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("⚠️ Sale not found.")
    except ValueError:
        print("🔴 Invalid ID. Please enter a valid sale ID.")
    except Exception as e:
        print(f"🔴 Error deleting sale: {e}")

# Function to log sale removal
def log_sale_removal(farmer_subfolder, sale_id, crop_type, farmer_name):
    log_file_path = os.path.join(farmer_subfolder, 'sale_removal_log.txt')
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Sale ID: {sale_id}, Crop Type: {crop_type}, Removed by: {farmer_name}\n"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)
    print("📄 Removal logged successfully.")

# Helper function to ensure non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("🔴 Input cannot be empty. Please try again.")
