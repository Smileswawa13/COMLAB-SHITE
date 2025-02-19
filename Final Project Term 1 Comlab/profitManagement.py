from datetime import datetime, timedelta
from tabulate import tabulate
import os

# Assuming all data structures are loaded similarly as you provided
# Example: Loading crops, expenses, fertilizer, pesticide_medicine, and sales from respective files

crops = {}
expenses = {}
fertilizer = {}
pesticide_medicine = {}
sales = {}


# Function to get the farmer's folder path
def get_farmer_folder(farmer_name):
    # Assuming the folders are named based on the farmer's name
    folder_path = os.path.join('Farmers', farmer_name)
    if os.path.exists(folder_path):
        return folder_path
    else:
        print(f"Folder for farmer {farmer_name} not found.")
        return None


# Load the crops data from the farmer's specific folder
def load_crops(farmer_name):
    farmer_folder = get_farmer_folder(farmer_name)
    if not farmer_folder:
        return

    crops_file = os.path.join(farmer_folder, 'crops.txt')
    if os.path.exists(crops_file):
        with open(crops_file, 'r') as file:
            for line in file:
                crop_data = line.strip().split(",")
                crop_id = int(crop_data[0])
                crops[crop_id] = {
                    'Date planted:': datetime.strptime(crop_data[1], "%Y-%m-%d"),
                    'Name of Crop:': crop_data[2],
                    'Variety:': crop_data[3],
                    'Field:': crop_data[4],
                    'Area:': int(crop_data[5]),
                    'Quantity': int(crop_data[6]),
                    'Notes': crop_data[7],
                    'Supplier Cost (PHP)': float(crop_data[8])
                }
    else:
        print(f"No crops file found for farmer {farmer_name}.")


# Load expenses data from the farmer's folder
def load_expenses(farmer_name):
    farmer_folder = get_farmer_folder(farmer_name)
    if not farmer_folder:
        return

    expenses_file = os.path.join(farmer_folder, 'expenses.txt')
    if os.path.exists(expenses_file):
        with open(expenses_file, 'r') as file:
            for line in file:
                expen_data = line.strip().split(",")
                expen_id = int(expen_data[0])
                expenses[expen_id] = {
                    'Date': datetime.strptime(expen_data[1], "%Y-%m-%d"),
                    'Expense Type': expen_data[2],
                    'Description': expen_data[3],
                    'Amount': float(expen_data[4]),
                    'Notes': expen_data[5]
                }
    else:
        print(f"No expenses file found for farmer {farmer_name}.")


# Load fertilizer data from the farmer's folder
def load_fertilizer(farmer_name):
    farmer_folder = get_farmer_folder(farmer_name)
    if not farmer_folder:
        return

    fertilizer_file = os.path.join(farmer_folder, 'fertilizer.txt')
    if os.path.exists(fertilizer_file):
        with open(fertilizer_file, 'r') as file:
            for line in file:
                fert_data = line.strip().split(",")
                fert_id = int(fert_data[0])
                fertilizer[fert_id] = {
                    'Scheduled Date': datetime.strptime(fert_data[1], "%Y-%m-%d"),
                    'Application Date': datetime.strptime(fert_data[2], "%Y-%m-%d"),
                    'Crop Applied to': fert_data[3],
                    'Name': fert_data[4],
                    'Variety': fert_data[5],
                    'Field': fert_data[6],
                    'Area': int(fert_data[7]),
                    'Quantity': int(fert_data[8]),
                    'Supplier Cost': float(fert_data[9]),
                    'Notes': fert_data[10]
                }
    else:
        print(f"No fertilizer file found for farmer {farmer_name}.")


# Load pesticide/medicine data from the farmer's folder
def load_pesticide_medicine(farmer_name):
    farmer_folder = get_farmer_folder(farmer_name)
    if not farmer_folder:
        return

    pestmed_file = os.path.join(farmer_folder, 'pesticide_medicine.txt')
    if os.path.exists(pestmed_file):
        with open(pestmed_file, 'r') as file:
            for line in file:
                pestmed_data = line.strip().split(",")
                pestmed_id = int(pestmed_data[0])
                pesticide_medicine[pestmed_id] = {
                    'Scheduled Date': datetime.strptime(pestmed_data[1], "%Y-%m-%d"),
                    'Application Date': datetime.strptime(pestmed_data[2], "%Y-%m-%d"),
                    'Disease/Pests': pestmed_data[3],
                    'Crop Applied to': pestmed_data[4],
                    'Name': pestmed_data[5],
                    'Variety': pestmed_data[6],
                    'Field': pestmed_data[7],
                    'Area': int(pestmed_data[8]),
                    'Quantity': int(pestmed_data[9]),
                    'Supplier Cost': float(pestmed_data[10]),
                    'Notes': pestmed_data[11]
                }
    else:
        print(f"No pesticide/medicine file found for farmer {farmer_name}.")


# Load sales data from the farmer's folder
def load_sales(farmer_name):
    farmer_folder = get_farmer_folder(farmer_name)
    if not farmer_folder:
        return

    sales_file = os.path.join(farmer_folder, 'sales.txt')
    if os.path.exists(sales_file):
        with open(sales_file, 'r') as file:
            for line in file:
                sale_data = line.strip().split(",")
                sale_id = int(sale_data[0])
                sales[sale_id] = {
                    'Sale Date': datetime.strptime(sale_data[1], "%Y-%m-%d"),
                    'Crop Type': sale_data[2],
                    'Quantity Sold': int(sale_data[3]),
                    'Price per kg': float(sale_data[4]),
                    'Total Sale': float(sale_data[5]),
                    'Market Buyer': sale_data[6],
                    'Notes': sale_data[7]
                }
    else:
        print(f"No sales file found for farmer {farmer_name}.")


# Function to calculate the period totals (weekly, monthly, yearly)
def calculate_period_totals(period="weekly"):
    total_sales = 0
    total_expenses = 0

    # Adjust the date range based on the period (weekly, monthly, yearly)
    current_date = datetime.now()
    if period == "weekly":
        start_date = current_date - timedelta(weeks=1)
    elif period == "monthly":
        start_date = current_date - timedelta(weeks=4)
    elif period == "yearly":
        start_date = current_date - timedelta(days=365)

    # Filter sales and expenses within the date range
    for sale in sales.values():
        if sale['Sale Date'] >= start_date:
            total_sales += sale['Total Sale']

    for expen in expenses.values():
        if expen['Date'] >= start_date:
            total_expenses += expen['Amount']

    for fert in fertilizer.values():
        if fert['Application Date'] >= start_date:
            total_expenses += fert['Supplier Cost']

    for pest in pesticide_medicine.values():
        if pest['Application Date'] >= start_date:
            total_expenses += pest['Supplier Cost']

    total_profits = total_sales - total_expenses
    return total_sales, total_expenses, total_profits


# Function to calculate overall totals (current total sales, expenses, profits)
def calculate_overall_totals():
    total_sales = 0
    total_expenses = 0

    # Calculate overall sales (all sales since the beginning)
    for sale in sales.values():
        total_sales += sale['Total Sale']

    # Calculate overall expenses (all expenses since the beginning)
    for expen in expenses.values():
        total_expenses += expen['Amount']

    for fert in fertilizer.values():
        total_expenses += fert['Supplier Cost']

    for pest in pesticide_medicine.values():
        total_expenses += pest['Supplier Cost']

    total_profits = total_sales - total_expenses
    return total_sales, total_expenses, total_profits

from colorama import Fore, Style
from tabulate import tabulate

def generate_report(farmer_name):
    # Load data specific to the farmer's folder
    load_crops(farmer_name)
    load_expenses(farmer_name)
    load_fertilizer(farmer_name)
    load_pesticide_medicine(farmer_name)
    load_sales(farmer_name)

    # Initialize the table data
    table_data = []

    # Define periods (weekly, monthly, yearly)
    periods = ["weekly", "monthly", "yearly"]

    # Variables to track overall totals
    overall_sales, overall_expenses, overall_profits = calculate_overall_totals()

    # Loop through the periods and calculate totals for each
    for period in periods:
        total_sales, total_expenses, total_profits = calculate_period_totals(period)

        # Determine the emoji to display based on the profits
        if total_profits < 0:
            profit_emoji = "🍅"  # Tomato emoji for negative profits
        else:
            profit_emoji = "🌽"  # Corn emoji for positive profits

        # Determine color for profits and expenses
        profit_color = Fore.RED if total_profits < 0 else Fore.GREEN
        expense_color = Fore.RED  # Expenses are always negative

        # Append the data with color and emojis
        table_data.append([f"💰 Total Sales ({period.capitalize()})", f"{Fore.CYAN}₱{total_sales:,.2f}{Style.RESET_ALL}"])
        table_data.append([f"📈 Total Expenses ({period.capitalize()})", f"{expense_color}₱{total_expenses:,.2f}{Style.RESET_ALL}"])
        table_data.append([f"💸 Total Profits ({period.capitalize()})", f"{profit_color}₱{total_profits:,.2f} {profit_emoji}{Style.RESET_ALL}"])

    # Add the overall totals to the table with emojis
    table_data.append([f"💵 Overall Total Sales", f"{Fore.CYAN}₱{overall_sales:,.2f}{Style.RESET_ALL}"])
    table_data.append([f"💸 Overall Total Expenses", f"{Fore.RED}₱{overall_expenses:,.2f}{Style.RESET_ALL}"])
    table_data.append([f"💰 Overall Total Profits", f"{Fore.GREEN}₱{overall_profits:,.2f}{Style.RESET_ALL}"])

    # Personal greeting and report header
    print(f"{Fore.YELLOW}🌾 Hello Farmer {farmer_name}! 🌾")
    print(f"{Fore.GREEN}Here's your profit report below:{Style.RESET_ALL}\n")

    # Defining the headers
    headers = ["Description", "Amount in PHP"]

    # Printing the table with formatting
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    print(f"{Fore.GREEN}Report generated successfully!{Style.RESET_ALL}")


