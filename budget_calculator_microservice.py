import json
import os
import time

# Global Constants for I/O Json Files.
INPUT_FILE = "input.json"       # <--- Change to whatever is best file name to use. Will update entire microservice.
OUTPUT_FILE = "output.json"     # <--- Change to whatever is best file name to use. Will update entire microservice.

def read_input_file(file_path):
    """
    Reads the INPUT_FILE json file and parsing the categories.
    Will raise an exepction when there is an error reading the file. 
    Takes on argument, INPUT_FILE
    Retruns the JSON is read from INPUT_FILE in a dictionary.
    """
    try:
        # Try to open the file & load JSON in the current directory.
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        # Print and return None on an error.
        print(f"Error reading {file_path}: {e}")
        return None

def calculate_allocations(data):
    """
    Calculates the allocations and returns only amounts + total.
    Takes one agrhument, the data read, INPUT_FILE JSON.
    Returns a dictionary called result, to be used for the OUTPUT_FILE.
    """

    try:
        # Try to get the total from INPUT_FILE, defaulting to 0 when missing.
        total = data.get("total", 0)
        # Initalize a new temp dictionary called result.
        result = {"total": total}
        
        # Iterate the kep:value pairs of the INPUT_FILE.
        for k, v in data.items():
            # SKipping the total key:value pair. 
            if k != "total":
                # v represents the value (percentage)
                # Multiply then use floor division to round & then appened to result.
                allocated = (v * total) // 100  
                result[k] = allocated
        
        # Return once completed.
        return result
    
    except Exception as e:
        # Print and return None on an error.
        print(f"Error calculating allocations: {e}")
        return None

def write_output_file(file_path, data):
    """
    Writes the result to the output JSON file
    Takes two aruments, OUTPUT_FILE name/path, and result dictionary.
    Does not return anything.
    """
    
    try:
        # Try to open the OUTPUT_FILE to write & Dump JSON.
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        # Alert when microservice is complete.
        print(f"Output written to {file_path}")
    
    except Exception as e:
        # Print the error if it occurs. 
        print(f"Error writing {file_path}: {e}")


if __name__ == "__main__":
    # Alert microservice is listening for the INPUT_FILE.
    print(f"Listening for {INPUT_FILE}...")

    # Check for INPUT_FILE in main directory every 1 second.
    while not os.path.exists(INPUT_FILE):
        time.sleep(1)  

    # Alert microservice has found and is begining to work.
    print(f"{INPUT_FILE} found.")
    print("Working...")
    input_data = read_input_file(INPUT_FILE)
    
    # If INPUT_FILE is able to be read, perform calculations and construct.
    if input_data:
        output_data = calculate_allocations(input_data)
        # If output_data is valid, write it to the OUTPUT_FILE json file. 
        if output_data:
            write_output_file(OUTPUT_FILE, output_data)
