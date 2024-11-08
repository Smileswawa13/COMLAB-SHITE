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
title = "AGRI-MEMORY!"
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

    # Main program choices
    choices = {
        "Crop Management": cropManagement.crop_menu,
        "Fertilizer Management": fertManagement.fertilizer_menu,
        "Pesticide and Disease Management": pestdieManagement.pesticide_medicine_menu,
        "Harvest Management": harvestManagement.harvest_menu,
        "Maintenance and Expenses Management": expensesManagement.expenses_menu,
        "Sales Management": salesManagement.sales_menu,
        "Profit Calculation": profitManagement.generate_report,
        "Summary Report": summaryFunction.generate_report,
        "Quit Agri-Memory?": exit
    }

    # Main loop with bordered choices
    while True:
        print("\n\033[1;34mAGRI-MEMORY FEATURES!\033[0m")  # Blue heading
        print("\033[1;37m" + "+" + "-" * (width - 2) + "+" + "\033[0m")  # Top border
        for index, (management, _) in enumerate(choices.items(), 1):
            print(f"\033[1;37m| {index}. {management.ljust(width - 4)} | \033[0m")  # Choices with border
        print("\033[1;37m" + "+" + "-" * (width - 2) + "+" + "\033[0m")  # Bottom border
        print("\033[1;33mWhat do you want to do, Farmer? 🌾\033[0m")  # Yellow question

        try:
            action = int(input("Enter here using the corresponding number: "))
            if 1 <= action <= len(choices):
                selected_action = list(choices.keys())[action - 1]
                selected_function = choices[selected_action]
                print(f"Opening... '{selected_action}'.")
                if callable(selected_function):
                    selected_function(farmer_name)
                else:
                    print(f"Error: {selected_action} is not callable.")
            else:
                print("Please select a valid option.")
        except ValueError:
            print("Please enter a valid number.")

# Utility function for non-empty input
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")

# The holder of reality
if __name__ == "__main__":
    main()
