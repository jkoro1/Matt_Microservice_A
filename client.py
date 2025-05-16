import json

INPUT_FILE = "input.json"  # <--- Change to whatever is best file name to use. Must allign with the microservice INPUT_FILE name.

def get_total_budget():
    """
    Gets the total budget from the current user. 
    Returns this total to be tracked. 
    No input arguments. 
    """
    while True:
        try:
            # Get number and ensure postive. 
            total = int(input("Enter your total budget amount: "))
            if total > 0:
                return total
            else:
                # Alert when negative.
                print("Please enter a positive number.\n")
        except ValueError:
            # Ensure it is a number. 
            print("Invalid.\nPlease enter a number.\n")

def get_categories_with_percentages():
    """
    Tracks the catgeoriges and % remaining using 100 as the starting point. 
    Continues to reprompt until the reaming percentage is 0.
    Ensures the remaining percentage does not go below 0.
    """

    # Track categories and percentage.
    categories = {}
    remaining_percentage = 100

    print(f"\nYou have {remaining_percentage}% remaining to budget.")
    
    # Collect categories and percentage while there is still some to budget. 
    while remaining_percentage > 0:

        # Collect the category name, drop & strip to lower to ensure no duplicates.
        category = input("Enter a category name (or type 'done' to finish): ").strip()
        
        # Ensure user uses all available allocation before sending to microservice.
        if category.lower() == 'done':
            if remaining_percentage == 0:
                break
            else:
                # Alert the user they still have more to allocate.
                print(f"You still have {remaining_percentage}% remaining. Please allocate it all before finishing.")
                continue
        
        # Ensure category does not already exist.
        if category in categories:
            print("Invalid.\nCategory already used. Please choose a different one.\n")
            continue
        
        try:
            # Try to get the percentage number from the user, alerting them how much they have left. Each iteration.
            percentage = int(input(f"Enter the percentage to allocate to {category} (remaining {remaining_percentage}%): "))
            
            # Ensure the percentage is greater than 0 and less than or equal to the remaining percentage left. 
            if 0 < percentage <= remaining_percentage:
                # Save to categories dictionary and subtract from total.
                categories[category] = percentage
                remaining_percentage -= percentage
                # Alert the user once again how much is now left.
                print(f"Success!\nRemaining: {remaining_percentage}%.\n")
            else:
                # Alert the user when they are 0 or under or above the remaining percentage left. 
                print(f"Invalid.\nEnter a value between 1 and {remaining_percentage}.\n")
        except ValueError:
            # Print an error IF they input a non int.
            print("Invalid.\nPlease enter a number.")

    # Return categories dictionary to be dumped into INPUT_FILE json file.
    return categories

def save_to_json(total, categories):
    """
    Saves the arguged dictionary (categories) to a json file called what the INPUT_FILE is asigned to.
    Takes two arguments, total ($ amount of their budget) and catgeories (dictionary containing the catgeory as a key and percent as value)
    """
    # Temp dictionary - add total and update with the key:value pairs from categories 
    data = {"total": total}
    data.update(categories)
    with open(INPUT_FILE, 'w') as f:
        # Write to JSON file.
        json.dump(data, f, indent=4)
    print(f"\nBudget saved to {INPUT_FILE}.\n")

if __name__ == "__main__":
    print("Buget Calcultor\n")
    total = get_total_budget()
    categories = get_categories_with_percentages()
    save_to_json(total, categories)
