import datetime
from collections import defaultdict
from userFarmerFunctions import make_farmer_folder

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping...")
        return []
    with open(file_path, 'r') as file:
        return file.readlines()

# Helper function to parse the date in the format YYYY-MM-DD
def parse_date(date_str):
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


# Function to get the farmer's folder path based on their name
def get_farmer_folder(farmer_name):
    folder_path = os.path.join('Farmers', farmer_name)
    print(f"Searching for folder: {folder_path}")  # Debug print
    print(f"Checking folder: {folder_path}")  # Debug print
    if os.path.exists(folder_path):
        return folder_path
    else:
        print(f"Folder for farmer {farmer_name} not found.")
        return None


# Function to calculate the total sales and quantity sold
def get_sales_and_buyers(sales_file):
    total_sales = 0
    total_quantity_sold = 0
    buyer_count = defaultdict(int)

    # Only process the file if it exists
    sales_data = read_file(sales_file)
    if sales_data:  # Proceed if there is data
        for line in sales_data:
            sale_id, date, crop_type, quantity_sold, price_per_kg, total_sale, buyer, notes = line.strip().split(',')
            total_sales += float(total_sale)
            total_quantity_sold += int(quantity_sold)
            buyer_count[buyer] += 1

    # Sort buyers by frequency (most frequent first)
    most_frequent_buyers = sorted(buyer_count.items(), key=lambda x: x[1], reverse=True)

    return total_sales, total_quantity_sold, most_frequent_buyers



# Function to calculate total expenses and breakdown by expense type
def get_expenses(expenses_file, expense_removal_log_file):
    total_expenses = 0
    expense_type_breakdown = defaultdict(float)
    expense_removals = []

    # Only process the files if they exist
    expense_data = read_file(expenses_file)
    expense_removal_log = read_file(expense_removal_log_file)

    if expense_data:  # Proceed if there is expense data
        for line in expense_data:
            expen_id, date, expen_type, expen_desc, expen_cost, expen_notes = line.strip().split(',')
            total_expenses += float(expen_cost)
            expense_type_breakdown[expen_type] += float(expen_cost)

    if expense_removal_log:  # Proceed if there is expense removal data
        for line in expense_removal_log:
            try:
                timestamp, expen_id, expen_type, removed_by = line.strip().split(' - ')
                expense_removals.append(f"{timestamp} - {expen_id} {expen_type} Removed by {removed_by}")
            except ValueError:
                print(f"Skipping invalid line in removal log: {line.strip()}")  # Print invalid lines for debugging

    return total_expenses, expense_type_breakdown, expense_removals



# Function to calculate activity summary (crops, fertilizers, pesticides)
def get_activity_summary(crops_file, crop_removal_log_file, fertilizer_file, pesticide_file, fertilizer_removal_log_file, pesticide_removal_log_file):
    crops_added = 0
    crops_removed_count = 0
    fertilizers_used = 0
    pesticides_used = 0
    fertilizer_removals_count = 0
    pesticide_removals_count = 0

    crops_data = read_file(crops_file)
    crop_removal_log_data = read_file(crop_removal_log_file)
    fertilizer_data = read_file(fertilizer_file)
    pesticide_data = read_file(pesticide_file)
    fertilizer_removal_data = read_file(fertilizer_removal_log_file)
    pesticide_removal_data = read_file(pesticide_removal_log_file)

    if crops_data:
        crops_added = len(crops_data)

    if crop_removal_log_data:
        crops_removed_count = len(crop_removal_log_data)  # Count of crop removals

    if fertilizer_data:
        fertilizers_used = len(fertilizer_data)

    if pesticide_data:
        pesticides_used = len(pesticide_data)

    if fertilizer_removal_data:
        fertilizer_removals_count = len(fertilizer_removal_data)  # Count of fertilizer removals

    if pesticide_removal_data:
        pesticide_removals_count = len(pesticide_removal_data)  # Count of pesticide removals

    return crops_added, crops_removed_count, fertilizers_used, pesticides_used, fertilizer_removals_count, pesticide_removals_count

# Function to calculate profits (by periods)
def calculate_profits(sales_file, expenses_file, period='monthly'):
    sales = defaultdict(float)
    expenses = defaultdict(float)

    sales_data = read_file(sales_file)
    expense_data = read_file(expenses_file)

    if sales_data:
        for line in sales_data:
            sale_id, date, crop_type, quantity_sold, price_per_kg, total_sale, buyer, notes = line.strip().split(',')
            sale_date = parse_date(date)
            sales[sale_date] += float(total_sale)

    if expense_data:
        for line in expense_data:
            expen_id, date, expen_type, expen_desc, expen_cost, expen_notes = line.strip().split(',')
            expen_date = parse_date(date)
            expenses[expen_date] += float(expen_cost)

    period_sales = defaultdict(float)
    period_expenses = defaultdict(float)

    for sale_date, sale_amount in sales.items():
        if period == 'monthly':
            period_key = sale_date.replace(day=1)
        elif period == 'weekly':
            period_key = sale_date - datetime.timedelta(days=sale_date.weekday())
        elif period == 'daily':
            period_key = sale_date
        period_sales[period_key] += sale_amount

    for expen_date, expen_amount in expenses.items():
        if period == 'monthly':
            period_key = expen_date.replace(day=1)
        elif period == 'weekly':
            period_key = expen_date - datetime.timedelta(days=expen_date.weekday())
        elif period == 'daily':
            period_key = expen_date
        period_expenses[period_key] += expen_amount

    profits = {period_key: period_sales[period_key] - period_expenses[period_key] for period_key in period_sales}

    return profits




# Function to get the overall work done
def get_overall_work(crops_file, expenses_file, fertilizer_file, pesticide_file, sales_file):
    # Initialize the operation counts
    crop_operations = 0
    expense_operations = 0
    fertilizer_operations = 0
    pesticide_operations = 0
    sales_operations = 0

    # Check if each file exists and count operations (lines)
    if os.path.exists(crops_file):
        crop_operations = len(read_file(crops_file))
    else:
        print(f"Warning: Crops file '{crops_file}' not found. Skipping.")

    if os.path.exists(expenses_file):
        expense_operations = len(read_file(expenses_file))
    else:
        print(f"Warning: Expenses file '{expenses_file}' not found. Skipping.")

    if os.path.exists(fertilizer_file):
        fertilizer_operations = len(read_file(fertilizer_file))
    else:
        print(f"Warning: Fertilizer file '{fertilizer_file}' not found. Skipping.")

    if os.path.exists(pesticide_file):
        pesticide_operations = len(read_file(pesticide_file))
    else:
        print(f"Warning: Pesticide file '{pesticide_file}' not found. Skipping.")

    if os.path.exists(sales_file):
        sales_operations = len(read_file(sales_file))
    else:
        print(f"Warning: Sales file '{sales_file}' not found. Skipping.")

    return crop_operations, expense_operations, fertilizer_operations, pesticide_operations, sales_operations


# Generate a farmer report
from colorama import Fore, Style
import emoji
import os
from tabulate import tabulate

def generate_report(farmer_name):
    # Get the farmer's subfolder path by calling make_farmer_folder
    farmer_subfolder = make_farmer_folder(farmer_name)

    if not farmer_subfolder:
        print("Farmer folder not created, exiting report generation.")
        return

    # File paths for the current farmer
    crops_file = os.path.join(farmer_subfolder, 'crops.txt')
    crop_removal_log_file = os.path.join(farmer_subfolder, 'crop_removal_log.txt')
    expenses_file = os.path.join(farmer_subfolder, 'expenses.txt')
    expense_removal_log_file = os.path.join(farmer_subfolder, 'expense_removal_log.txt')
    fertilizer_file = os.path.join(farmer_subfolder, 'fertilizer.txt')
    fertilizer_removal_log_file = os.path.join(farmer_subfolder, 'fertilizer_removal_log.txt')
    pesticide_file = os.path.join(farmer_subfolder, 'pesticide_medicine.txt')
    pesticide_removal_log_file = os.path.join(farmer_subfolder, 'pesticide_medicine_removal_log.txt')
    sales_file = os.path.join(farmer_subfolder, 'sales.txt')
    sale_removal_log_file = os.path.join(farmer_subfolder, 'sale_removal_log.txt')

    # 1. Sales and Buyers Summary (stub functions)
    total_sales, total_quantity_sold, most_frequent_buyers = get_sales_and_buyers(sales_file)

    # 2. Expenses Summary (stub functions)
    total_expenses, expense_type_breakdown, expense_removals = get_expenses(expenses_file, expense_removal_log_file)

    # 3. Activity Summary (stub functions)
    crops_added, crops_removed_count, fertilizers_used, pesticides_used, fertilizer_removals_count, pesticide_removals_count = get_activity_summary(
        crops_file, crop_removal_log_file, fertilizer_file, pesticide_file, fertilizer_removal_log_file,
        pesticide_removal_log_file)

    # 4. Profits (stub function)
    profits = calculate_profits(sales_file, expenses_file, period='monthly')

    # 5. Overall Work Done (stub functions)
    crop_operations, expense_operations, fertilizer_operations, pesticide_operations, sales_operations = get_overall_work(
        crops_file, expenses_file, fertilizer_file, pesticide_file, sales_file)

    # Combine all the summary data
    report = {
        'Sales and Buyers Summary': {
            'Total Sales': total_sales,
            'Total Quantity Sold': total_quantity_sold,
            'Most Frequent Buyers': most_frequent_buyers
        },
        'Expenses Summary': {
            'Total Expenses': total_expenses,
            'Expense Breakdown': expense_type_breakdown,
            'Expense Removal Count': len(expense_removals)  # Number of removed expense entries
        },
        'Activity Summary': {
            'Crops Added': crops_added,
            'Crops Removed': crops_removed_count,
            'Fertilizers Used': fertilizers_used,
            'Pesticides Used': pesticides_used,
            'Fertilizer Removal Count': fertilizer_removals_count,
            'Pesticide Removal Count': pesticide_removals_count
        },
        'Profits': profits,
        'Overall Work Done': {
            'Crop Operations': crop_operations,
            'Expense Operations': expense_operations,
            'Fertilizer Operations': fertilizer_operations,
            'Pesticide Operations': pesticide_operations,
            'Sales Operations': sales_operations
        }
    }

    # Format and print the report using tabular format
    table_data = []

    # Sales and Buyers Summary
    table_data.append([emoji.emojize(":moneybag:") + " Total Sales", f"{Fore.GREEN}₱{report['Sales and Buyers Summary']['Total Sales']:,.2f}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":weight_lifter:") + " Total Quantity Sold", f"{Fore.CYAN}{report['Sales and Buyers Summary']['Total Quantity Sold']} kg{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":bust_in_silhouette:") + " Most Frequent Buyers", ', '.join([f"{buyer}: {count}" for buyer, count in report['Sales and Buyers Summary']['Most Frequent Buyers']])])

    # Expenses Summary
    table_data.append([emoji.emojize(":euro:") + " Total Expenses", f"{Fore.RED}₱{report['Expenses Summary']['Total Expenses']:,.2f}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":chart_with_upwards_trend:") + " Expense Breakdown", ', '.join([f"{expen_type}: ₱{cost}" for expen_type, cost in report['Expenses Summary']['Expense Breakdown'].items()])])
    table_data.append([emoji.emojize(":wastebasket:") + " Expense Removal Count", f"{Fore.YELLOW}{report['Expenses Summary']['Expense Removal Count']}{Style.RESET_ALL}"])

    # Activity Summary
    table_data.append([emoji.emojize(":seedling:") + " Crops Added", f"{Fore.GREEN}{report['Activity Summary']['Crops Added']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":x:") + " Crops Removed", f"{Fore.RED}{report['Activity Summary']['Crops Removed']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":seedling:") + " Fertilizers Used", f"{Fore.YELLOW}{report['Activity Summary']['Fertilizers Used']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":herb:") + " Pesticides Used", f"{Fore.MAGENTA}{report['Activity Summary']['Pesticides Used']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":recycle:") + " Fertilizer Removal Count", f"{Fore.RED}{report['Activity Summary']['Fertilizer Removal Count']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":recycle:") + " Pesticide Removal Count", f"{Fore.RED}{report['Activity Summary']['Pesticide Removal Count']}{Style.RESET_ALL}"])

    # In the table generation part of your code
    for period, profit in report['Profits'].items():
        # Ensure the period is a datetime object, then format it using strftime
        if isinstance(period, datetime.date):
            table_data.append([emoji.emojize(":chart_with_upwards_trend:") + f" Profit ({period.strftime('%Y-%m')})", f"{Fore.GREEN}₱{profit:,.2f}{Style.RESET_ALL}"])
        else:
            table_data.append([emoji.emojize(":chart_with_upwards_trend:") + f" Profit ({period})", f"{Fore.GREEN}₱{profit:,.2f}{Style.RESET_ALL}"])  # If period is a string

    # Overall Work Done
    table_data.append([emoji.emojize(":hammer_and_wrench:") + " Crop Operations", f"{Fore.CYAN}{report['Overall Work Done']['Crop Operations']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":clipboard:") + " Expense Operations", f"{Fore.CYAN}{report['Overall Work Done']['Expense Operations']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":seedling:") + " Fertilizer Operations", f"{Fore.CYAN}{report['Overall Work Done']['Fertilizer Operations']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":herb:") + " Pesticide Operations", f"{Fore.CYAN}{report['Overall Work Done']['Pesticide Operations']}{Style.RESET_ALL}"])
    table_data.append([emoji.emojize(":shopping_cart:") + " Sales Operations", f"{Fore.CYAN}{report['Overall Work Done']['Sales Operations']}{Style.RESET_ALL}"])

    # Print the table
    print(tabulate(table_data, headers=["Metric", "Value"], tablefmt="grid"))

    print(f"{Fore.GREEN}Report generated successfully!{Style.RESET_ALL}")
    return




