import os
import datetime
from collections import defaultdict
from tabulate import tabulate

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
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

    for line in read_file(sales_file):
        sale_id, date, crop_type, quantity_sold, price_per_kg, total_sale, buyer, notes = line.strip().split(',')
        total_sales += float(total_sale)
        total_quantity_sold += int(quantity_sold)
        buyer_count[buyer] += 1

    most_frequent_buyers = sorted(buyer_count.items(), key=lambda x: x[1], reverse=True)

    return total_sales, total_quantity_sold, most_frequent_buyers


# Function to calculate total expenses and breakdown by expense type
def get_expenses(expenses_file, expense_removal_log_file):
    total_expenses = 0
    expense_type_breakdown = defaultdict(float)
    expense_removals = []

    for line in read_file(expenses_file):
        expen_id, date, expen_type, expen_desc, expen_cost, expen_notes = line.strip().split(',')
        total_expenses += float(expen_cost)
        expense_type_breakdown[expen_type] += float(expen_cost)

    for line in read_file(expense_removal_log_file):
        timestamp, expen_id, expen_type, removed_by = line.strip().split(' - ')
        expense_removals.append(f"{timestamp} - {expen_id} {expen_type} Removed by {removed_by}")

    return total_expenses, expense_type_breakdown, expense_removals


# Function to calculate activity summary (crops, fertilizers, pesticides)
def get_activity_summary(crops_file, crop_removal_log_file, fertilizer_file, pesticide_file,
                         fertilizer_removal_log_file, pesticide_removal_log_file):
    crops_added = len(read_file(crops_file))
    crops_removed = []
    fertilizers_used = len(read_file(fertilizer_file))
    pesticides_used = len(read_file(pesticide_file))
    fertilizer_removals = []
    pesticide_removals = []

    for line in read_file(crop_removal_log_file):
        timestamp, crop_id, crop_name, removed_by = line.strip().split(' - ')
        crops_removed.append(f"{timestamp} - {crop_id} {crop_name} Removed by {removed_by}")

    for line in read_file(fertilizer_removal_log_file):
        timestamp, fert_id, fert_name, removed_by = line.strip().split(' - ')
        fertilizer_removals.append(f"{timestamp} - {fert_id} {fert_name} Removed by {removed_by}")

    for line in read_file(pesticide_removal_log_file):
        timestamp, pestmed_id, name, removed_by = line.strip().split(' - ')
        pesticide_removals.append(f"{timestamp} - {pestmed_id} {name} Removed by {removed_by}")

    return crops_added, crops_removed, fertilizers_used, pesticides_used, fertilizer_removals, pesticide_removals


# Function to calculate profits (by periods)
def calculate_profits(sales_file, expenses_file, period='monthly'):
    sales = defaultdict(float)
    expenses = defaultdict(float)

    for line in read_file(sales_file):
        sale_id, date, crop_type, quantity_sold, price_per_kg, total_sale, buyer, notes = line.strip().split(',')
        sale_date = parse_date(date)
        sales[sale_date] += float(total_sale)

    for line in read_file(expenses_file):
        expen_id, date, expen_type, expen_desc, expen_cost, expen_notes = line.strip().split(',')
        expen_date = parse_date(date)
        expenses[expen_date] += float(expen_cost)

    # Grouping by period
    start_date = datetime.date.today()
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
    crop_operations = len(read_file(crops_file))
    expense_operations = len(read_file(expenses_file))
    fertilizer_operations = len(read_file(fertilizer_file))
    pesticide_operations = len(read_file(pesticide_file))
    sales_operations = len(read_file(sales_file))

    return crop_operations, expense_operations, fertilizer_operations, pesticide_operations, sales_operations


# Generate a farmer report
# Inside the main loop where generate_report is called
def generate_report(farmer_name):
    farmer_folder = f"Farmers\\{farmer_name}"
    print(f"Searching for folder: {farmer_folder}")

    if os.path.exists(farmer_folder):
        print(f"Folder found: {farmer_folder}")

        # Example of loading a file and checking its content
        crop_file = os.path.join(farmer_folder, "crops.txt")
        if os.path.exists(crop_file):
            print(f"Found crops file: {crop_file}")
            with open(crop_file, "r") as f:
                crops = f.readlines()
                print(f"Loaded crops: {crops[:5]}")  # Show first 5 lines of crops.txt
        else:
            print("Error: crops.txt not found!")

        # You can add other file loading logic here as needed

        # Report generation logic: Show or save the generated report
        print(f"Generating summary report for {farmer_name}...")
        # Insert your actual report logic here
        print("Report generation complete.")
    else:
        print(f"Error: Folder {farmer_folder} does not exist.")

    # Wait for the user to press Enter before returning to the menu
    input("Press Enter to return to the main menu...")

    # File paths for the current farmer
    crops_file = os.path.join(farmer_folder, 'crops.txt')
    crop_removal_log_file = os.path.join(farmer_folder, 'crop_removal_log.txt')
    expenses_file = os.path.join(farmer_folder, 'expenses.txt')
    expense_removal_log_file = os.path.join(farmer_folder, 'expense_removal_log.txt')
    fertilizer_file = os.path.join(farmer_folder, 'fertilizer.txt')
    fertilizer_removal_log_file = os.path.join(farmer_folder, 'fertilizer_removal_log.txt')
    pesticide_file = os.path.join(farmer_folder, 'pesticide_medicine.txt')
    pesticide_removal_log_file = os.path.join(farmer_folder, 'pesticide_medicine_removal_log.txt')
    sales_file = os.path.join(farmer_folder, 'sales.txt')
    sale_removal_log_file = os.path.join(farmer_folder, 'sale_removal_log.txt')

    # 1. Sales and Buyers Summary
    total_sales, total_quantity_sold, most_frequent_buyers = get_sales_and_buyers(sales_file)

    # 2. Expenses Summary
    total_expenses, expense_type_breakdown, expense_removals = get_expenses(expenses_file, expense_removal_log_file)

    # 3. Activity Summary
    crops_added, crops_removed, fertilizers_used, pesticides_used, fertilizer_removals, pesticide_removals = get_activity_summary(
        crops_file, crop_removal_log_file, fertilizer_file, pesticide_file, fertilizer_removal_log_file,
        pesticide_removal_log_file)

    # 4. Profits
    profits = calculate_profits(sales_file, expenses_file, period='monthly')  # Change to other periods as needed

    # 5. Overall Work Done
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
            'Expense Removal Log': expense_removals
        },
        'Activity Summary': {
            'Crops Added': crops_added,
            'Crops Removed': crops_removed,
            'Fertilizers Used': fertilizers_used,
            'Pesticides Used': pesticides_used,
            'Fertilizer Removal Log': fertilizer_removals,
            'Pesticide Removal Log': pesticide_removals
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
    table_data.append(["Total Sales", f"₱{report['Sales and Buyers Summary']['Total Sales']:,.2f}"])
    table_data.append(["Total Quantity Sold", f"{report['Sales and Buyers Summary']['Total Quantity Sold']} kg"])
    table_data.append(["Most Frequent Buyers", ', '.join([f"{buyer}: {count}" for buyer, count in report['Sales and Buyers Summary']['Most Frequent Buyers']])])

    # Expenses Summary
    table_data.append(["Total Expenses", f"₱{report['Expenses Summary']['Total Expenses']:,.2f}"])
    table_data.append(["Expense Breakdown", ', '.join([f"{expen_type}: ₱{cost}" for expen_type, cost in report['Expenses Summary']['Expense Breakdown'].items()])])
    table_data.append(["Expense Removal Log", ', '.join(report['Expenses Summary']['Expense Removal Log'])])

    # Activity Summary
    table_data.append(["Crops Added", report['Activity Summary']['Crops Added']])
    table_data.append(["Crops Removed", ', '.join(report['Activity Summary']['Crops Removed'])])
    table_data.append(["Fertilizers Used", report['Activity Summary']['Fertilizers Used']])
    table_data.append(["Pesticides Used", report['Activity Summary']['Pesticides Used']])
    table_data.append(["Fertilizer Removal Log", ', '.join(report['Activity Summary']['Fertilizer Removal Log'])])
    table_data.append(["Pesticide Removal Log", ', '.join(report['Activity Summary']['Pesticide Removal Log'])])

    # Profits
    for period, profit in report['Profits'].items():
        table_data.append([f"Profit ({period.strftime('%Y-%m')})", f"₱{profit:,.2f}"])

    # Overall Work Done
    table_data.append(["Crop Operations", report['Overall Work Done']['Crop Operations']])
    table_data.append(["Expense Operations", report['Overall Work Done']['Expense Operations']])
    table_data.append(["Fertilizer Operations", report['Overall Work Done']['Fertilizer Operations']])
    table_data.append(["Pesticide Operations", report['Overall Work Done']['Pesticide Operations']])
    table_data.append(["Sales Operations", report['Overall Work Done']['Sales Operations']])

    print(tabulate(table_data, headers=["Metric", "Value"], tablefmt="grid"))

    # After report generation, return to the menu or call any final step
    print("Report generated successfully!")
    return  # This ensures we don't loop back to asking for input again.


