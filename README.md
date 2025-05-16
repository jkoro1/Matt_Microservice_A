Microservice A - Matt

----------------------------------------------------------------------
This microservice calculates budgeted categories based on a total budget and percentages.
The microservice continuously checks the main working directory for an "input.json" file - this is adjustable.
When found the microservice will perform calculations and write the results to an "output.json" file - this is adjustable.
All comminication with the microservice is done via file reads and writes.

----------------------------------------------------------------------
REQUESTING DATA:

To request data from the microservice you must:
1. Create and write an "input.json" file in the same directory as the microservice.

2. The JSON must contain the following format:
   - A "total" key with an integer representing the total budget.
   - One or more category keys each with a value of an int representing the percentage allocation.

Example python code to create the request file:
----------------------------

import json

request_data = {
    "total": 1000,
    "rent": 50,
    "utilities": 30,
    "entertainment": 20
}

with open("input.json", "w") as f:
    json.dump(request_data, f, indent=4)

----------------------------
Something to note:
- The microservice will assumes  "input.json" is valid meaning percentages must sum to 100%.

----------------------------------------------------------------------
RECEIVING DATA:

To receive data from the microservice your main program must:
1. Wait for the microservice to create an "output.json".
2. Once the file appears then read and parse the JSON.

Example python code to read the response:
----------------------------

import json
import os
import time

output_file = "output.json"

while not os.path.exists(output_file):
    time.sleep(1)

with open(output_file, "r") as f:
    response_data = json.load(f)

print(json.dumps(response_data, indent=4))

----------------------------
Something to note:
- The output file will contain:
  - The same "total" key.
  - Each category with its allocated amount in whole dollars, rounded down.

----------------------------------------------------------------------
File Examples:

Example input.json:
{
    "total": 1000,
    "housing": 60,
    "groceries": 40
}

Example output.json:
{
    "total": 1000,
    "housing": 600,
    "groceries": 400
}