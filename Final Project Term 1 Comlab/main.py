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
names = ["Mr.Smiley", "Raffy", "Robs", "Neil"]
description = """Welcome to Your Very Own Digital Farming Logbook! 📔🌱
Keep track of all your farming activities, tasks, and milestones with ease. 
Whether you're planning crop rotations, tracking harvest dates, or generating
a report, this digital logbook is designed to be your perfect companion 
in the field.
Ready to grow your digital farm records? Let’s get started!"""
separator = "/=/" * 30

# Main Function of the entire program
def main():
    # Declare the global variable for farmer's name
    farmer_name = ""

    # Print the title and descriptions once when the program starts
    print(title)
    print(subtitle)
    for name_ in names:
        print(name_)
    print(separator)
    print(description)
    print(separator)
    input("\nPlease press ENTER to proceed with the logbook...")
    print(separator)

    # Loop until a valid farmer name is entered
    while not farmer_name:
        # Ask for the farmer's name before proceeding
        farmer_name = input("Hi farmer! May we know your name?\nEnter here: ").strip()

        # If the name is empty, prompt the user to enter a valid name again
        if not farmer_name:
            print("You must enter a name to continue.")

    print(f"Hello farmer {farmer_name}! How do you want to proceed?")

    # The main features as a dictionary, updated with placeholders
    choices = {
        "Crop Management": cropManagement.crop_menu,
        "Fertilizer Management": fertManagement.fertilizer_menu,
        "Pesticide and Disease Management": pestdieManagement.pesticide_medicine_menu,
        "Harvest Management": harvestManagement.harvest_menu,
        "Maintenance and Expenses Management": expensesManagement.expenses_menu,
        "Sales Management": salesManagement.sales_menu,
        "Profit Calculation": profitManagement.generate_report,
        "Summary Report": summaryFunction.generate_report,
        "Quit Agri-Memory?": None
    }

    # The main loop and choice manager
    while True:
        print("\nAGRI-MEMORY FEATURES!")
        # Display the features to the user
        for index, (management, key) in enumerate(choices.items(), 1):
            print(f"{index}. {management}")
        print("What do you want to do, Farmer?")

        # Ask for user input
        try:
            action = int(input("Enter here using the corresponding number: "))

            # Validating if input is within the range
            if 1 <= action <= 8:
                # Output converted into proper indexing
                selected_action = list(choices.keys())[action - 1]
                selected_function = choices[selected_action]

                print(f"Opening...'{selected_action}'.")
                print(f"Selected action: {selected_action}")
                if callable(selected_function):
                    print(f"Calling function for {selected_action}...")
                    selected_function(farmer_name)
                else:
                    print(f"Error: {selected_action} is not callable.")

            elif action == 9:
                print("You are now exiting Agri-Memory. Cya again Farmer!")
                break

            else:
                print("Your input is not in the corresponding choices. Please enter between 1 and 8.")

        except ValueError:
            print("Please enter a valid number.")


# This function will keep asking for input until it's not empty
def get_non_empty_input(prompt):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("Input cannot be empty. Please try again.")

# The fabric of reality holder
if __name__ == "__main__":
    main()
