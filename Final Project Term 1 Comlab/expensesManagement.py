from datetime import datetime
from tabulate import tabulate
import os
from userFarmerFunctions import make_farmer_folder

# Global dictionary to store expenses and maintenance records
expenses = {}

# Function to validate date input
def get_valid_date(prompt):
    while True:
        date_input = input(prompt)
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter a date in YYYY-MM-DD format.")

# Function for the main expenses and maintenance menu
def expenses_menu(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    if not farmer_subfolder:
        print("Farmer folder not created, exiting expenses management.")
        return

    load_expenses(farmer_subfolder)

    while True:
        print(f"~~ Expenses and Maintenance Management - Farmer {farmer_name} ~~")
        options = {
            "Add Expense": add_expense,
            "Edit Expense": edit_expense,
            "View Expenses": view_expenses,
            "Delete Expense": delete_expense,
            "Quit Management": None
        }

        for index, action in enumerate(options, 1):
            print(f"{index}. {action}")

        try:
            action = int(input("Enter your choice using the corresponding number: "))
            if 1 <= action <= 4:
                selected_function = list(options.values())[action - 1]
                if callable(selected_function):
                    if selected_function == view_expenses:
                        selected_function(farmer_name)
                    else:
                        selected_function(farmer_subfolder, farmer_name)
            elif action == 5:
                print("Exiting Expenses and Maintenance Management")
                break
            else:
                print("Invalid choice. Choose between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

# Function to load expenses data from a file
def load_expenses(farmer_subfolder):
    expenses_file_path = os.path.join(farmer_subfolder, 'expenses.txt')
    if os.path.exists(expenses_file_path):
        with open(expenses_file_path, 'r') as file:
            for line in file:
                data = line.strip().split(",")
                try:
                    expen_id = int(data[0])
                    expenses[expen_id] = {
                        'Date': datetime.strptime(data[1], "%Y-%m-%d"),
                        'Expense Type': data[2],
                        'Description': data[3],
                        'Amount': float(data[4]),
                        'Notes': data[5] if len(data) > 5 else ""
                    }
                except ValueError as e:
                    print(f"Error loading expense data: {e}. Skipping line.")
        print("Expenses loaded successfully.")
    else:
        print("No expenses file found. Starting with an empty list.")

# Function to save expenses data to a file
def save_expenses(farmer_subfolder):
    expenses_file_path = os.path.join(farmer_subfolder, 'expenses.txt')
    with open(expenses_file_path, 'w') as file:
        for expen_id, data in expenses.items():
            date = data['Date'].strftime("%Y-%m-%d")
            file.write(f"{expen_id},{date},{data['Expense Type']},{data['Description']},{data['Amount']},{data['Notes']}\n")
    print("Expenses data saved successfully.")

# Function to add expense data
def add_expense(farmer_subfolder, farmer_name):
    print("~~ Adding New Expense ~~")
    try:
        expen_id = int(input("Please enter a unique expense ID: "))
        if expen_id in expenses:
            print(f"Expense with ID '{expen_id}' already exists!")
            return
    except ValueError:
        print("Invalid ID. It should be numeric.")
        return

    date = get_valid_date("Enter the date of the expense (YYYY-MM-DD): ")
    expen_type = input("Enter the type of expense (e.g., maintenance, labor): ").strip()
    expen_desc = input("Enter a description of the expense: ").strip()
    try:
        expen_cost = float(input("Enter the expense amount: ").strip())
    except ValueError:
        print("Invalid input for amount.")
        return

    expen_notes = input("[Optional] Additional notes: ").strip()

    expenses[expen_id] = {
        'Date': date,
        'Expense Type': expen_type,
        'Description': expen_desc,
        'Amount': expen_cost,
        'Notes': expen_notes
    }

    save_expenses(farmer_subfolder)
    print("Expense added successfully.")

# Function to edit expense data
def edit_expense(farmer_subfolder, farmer_name):
    view_expenses(farmer_name)
    try:
        expen_id = int(input("Enter the expense ID to edit: "))
        if expen_id not in expenses:
            print("Expense not found.")
            return

        current_data = expenses[expen_id]

        # Prompt for each field, keeping the existing value if the user skips
        date = get_valid_date("Enter the new date (YYYY-MM-DD) or press Enter to keep the current date: ")
        expenses[expen_id]['Date'] = date if date else current_data['Date']

        expen_type = input(f"Enter the new expense type [{current_data['Expense Type']}]: ").strip()
        expenses[expen_id]['Expense Type'] = expen_type if expen_type else current_data['Expense Type']

        expen_desc = input(f"Enter the new description [{current_data['Description']}]: ").strip()
        expenses[expen_id]['Description'] = expen_desc if expen_desc else current_data['Description']

        amount = input(f"Enter the new amount [{current_data['Amount']}]: ").strip()
        if amount:
            try:
                expenses[expen_id]['Amount'] = float(amount)
            except ValueError:
                print("Invalid input for amount. Keeping current value.")
        else:
            expenses[expen_id]['Amount'] = current_data['Amount']

        notes = input(f"[Optional] Additional notes [{current_data['Notes'] or 'No notes'}]: ").strip()
        expenses[expen_id]['Notes'] = notes if notes else current_data['Notes']

        save_expenses(farmer_subfolder)
        print(f"Expense ID {expen_id} edited successfully.")
    except ValueError:
        print("Invalid ID.")

# Function to view all expenses
def view_expenses(farmer_name):
    farmer_subfolder = make_farmer_folder(farmer_name)
    load_expenses(farmer_subfolder)

    if not expenses:
        print("No expenses found.")
        return

    headers = ["ID", "Date", "Expense Type", "Description", "Amount (PHP)", "Notes"]
    table_data = []

    for expen_id, data in expenses.items():
        row = [
            expen_id,
            data['Date'].strftime("%Y-%m-%d"),
            data['Expense Type'],
            data['Description'],
            f"₱{data['Amount']:.2f}",  # Format the amount with PHP symbol
            data['Notes'] or "No notes"
        ]
        table_data.append(row)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to delete an expense with confirmation
def delete_expense(farmer_subfolder, farmer_name):
    view_expenses(farmer_name)
    try:
        expen_id = int(input("Enter the expense ID to delete: "))
        if expen_id in expenses:
            # Prompt for confirmation
            confirmation = input(f"Are you sure you want to delete expense ID {expen_id}? Type 'yes' to confirm: ").strip().lower()
            if confirmation == "yes":
                expen_type = expenses[expen_id]['Expense Type']
                del expenses[expen_id]
                save_expenses(farmer_subfolder)
                log_expense_removal(farmer_subfolder, expen_id, expen_type, farmer_name)
                print(f"Expense ID {expen_id} deleted successfully.")
            else:
                print("Deletion canceled.")
        else:
            print("Expense not found.")
    except ValueError:
        print("Invalid ID.")

# Function to log expense removal
def log_expense_removal(farmer_subfolder, expen_id, expen_type, farmer_name):
    log_file_path = os.path.join(farmer_subfolder, 'expense_removal_log.txt')
    log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ID: {expen_id}, Type: {expen_type}, Removed by: {farmer_name}\n"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)
    print("Removal logged successfully.")


# This function will keep asking for input until it's not empty
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")
