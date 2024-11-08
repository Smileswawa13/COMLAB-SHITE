"""
Final Project: Agri-Memory
Created By Group 1:
Neil Justin V. Bermoy
Raffy A. Panawidan
Neil M. Olbes
Robert Paul C. Nery
Created: Month of Oct.
Modified: 11-08-24
"""
import time  # To control display timings for added effect
import expensesManagement
import fertManagement
import harvestManagement
import pestdieManagement
import profitManagement
import salesManagement
import summaryFunction
from summaryFunction import generate_report  # Ensure correct import
from userFarmerFunctions import make_farmer_folder
import cropManagement

# Title and descriptions
title = " 📝 AGRI-MEMORY! 📝"
subtitle = "Created by:"
names = ["Neil Justin V. Bermoy", "Raffy A. Panawidan", "Neil M. Olbes", "Robert Paul C. Nery"]
description = """Welcome to Your Very Own Digital Farming Logbook! 📔🌱
Keep track of all your farming activities, tasks, and milestones with ease. 
Whether you're planning crop rotations, tracking harvest dates, or generating
a report, this digital logbook is designed to be your perfect companion 
in the field.
Ready to grow your digital farm records? Let’s get started!"""
separator = "/=/" * 30

# Define the console width
width = 80

# Main Function of the entire program
def main():
    # Declare the global variable for farmer's name
    farmer_name = ""

    # Text wrapping for the description
    words = description.split()
    wrapped_lines = []
    while words:
        current_line = words.pop(0)
        while len(current_line) < width and words:
            next_word = words[0]
            if len(current_line) + len(next_word) + 1 <= width:
                current_line += " " + words.pop(0)
            else:
                break
        wrapped_lines.append(current_line)

    # Print the title and descriptions with effects
    print("\033[1;33m" + title.center(width) + "\033[0m")  # Yellow for title
    time.sleep(0.3)
    print("\033[1;32m" + subtitle.center(width) + "\033[0m")  # Green for subtitle

    for name_ in names:
        time.sleep(0.3)
        print("\033[1;35;3m" + name_.center(width) + "\033[0m")  # Purple names
        time.sleep(0.3)
    print("\033[1;37m" + separator.center(width) + "\033[0m")  # White separator
    for line in wrapped_lines:
        time.sleep(0.3)
        print("\033[3m" + line.center(width) + "\033[0m")  # Italic description
    print("\033[1;37m" + separator.center(width) + "\033[0m")
    time.sleep(2)
    print('\033[3mProcessing...\033[0m')
    time.sleep(3)
    input("\033[3mPress \033[1mENTER\033[0m\033[3m to start the program...\033[0m")
    print("\033[1;37m" + separator.center(width) + "\033[0m")

    # Loop until a valid farmer name is entered
    while not farmer_name:
        farmer_name = input("Hi farmer! May we know your name?\nEnter here: ").strip()
        if not farmer_name:
            print("You must enter a name to continue.")
    print("\033[1;37m" + separator.center(width) + "\033[0m")
    print(f"\nHello farmer {farmer_name}! How do you want to proceed?")

    # Main loop with if-else structure for choices
    while True:
        print("\n\033[1;34mAGRI-MEMORY FEATURES!\033[0m")  # Blue heading
        print("\033[1;37m" + "+" + "-" * (width - 2) + "+" + "\033[0m")  # Top border

        # Display options manually without using a dictionary
        print("\033[1;37m| 1. Crop Management".ljust(width - 4) + " | \033[0m")  # Crop Management
        print("\033[1;37m| 2. Fertilizer Management".ljust(width - 4) + " | \033[0m")  # Fertilizer Management
        print("\033[1;37m| 3. Pesticide and Disease Management".ljust(width - 4) + " | \033[0m")  # Pesticide Management
        print("\033[1;37m| 4. Harvest Management".ljust(width - 4) + " | \033[0m")  # Harvest Management
        print("\033[1;37m| 5. Maintenance and Expenses Management".ljust(width - 4) + " | \033[0m")  # Expenses Management
        print("\033[1;37m| 6. Sales Management".ljust(width - 4) + " | \033[0m")  # Sales Management
        print("\033[1;37m| 7. Profit Calculation".ljust(width - 4) + " | \033[0m")  # Profit Calculation
        print("\033[1;37m| 8. Summary Report".ljust(width - 4) + " | \033[0m")  # Summary Report
        print("\033[1;37m| 9. Quit Agri-Memory?".ljust(width - 4) + " | \033[0m")  # Quit Option
        print("\033[1;37m" + "+" + "-" * (width - 2) + "+" + "\033[0m")  # Bottom border
        print("\033[1;33mWhat do you want to do, Farmer? 🌾\033[0m")  # Yellow question

        # Main code for action selection
        action_input = input("Enter here using the corresponding number: ").strip()  # User selects an action number

        if action_input.isdigit():
            action = int(action_input)  # Convert input to integer

            if action == 1:
                print("Opening... 'Crop Management'.")
                cropManagement.crop_menu(farmer_name)
            elif action == 2:
                print("Opening... 'Fertilizer Management'.")
                fertManagement.fertilizer_menu(farmer_name)
            elif action == 3:
                print("Opening... 'Pesticide and Disease Management'.")
                pestdieManagement.pesticide_medicine_menu(farmer_name)
            elif action == 4:
                print("Opening... 'Harvest Management'.")
                harvestManagement.harvest_menu(farmer_name)
            elif action == 5:
                print("Opening... 'Maintenance and Expenses Management'.")
                expensesManagement.expenses_menu(farmer_name)
            elif action == 6:
                print("Opening... 'Sales Management'.")
                salesManagement.sales_menu(farmer_name)
            elif action == 7:
                print("Opening... 'Profit Calculation'.")
                profitManagement.generate_report(farmer_name)
            elif action == 8:
                print("Opening... 'Summary Report'.")
                summaryFunction.generate_report(farmer_name)
            elif action == 9:
                print("Exiting Agri-Memory.")
                exit()  # Exit the program
            else:
                print("\033[1;31mPlease select a valid option between 1 and 9.\033[0m")  # Invalid range
        else:
            print("\033[1;31mPlease enter a valid number.\033[0m")  # Invalid input type

# The holder of reality
if __name__ == "__main__":
    main()
