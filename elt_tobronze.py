
import sys
import requests
import json
import os
from datetime import datetime, timedelta

def extract_props(created_at: str, directory: str = ".") -> bool:
    '''Extract property data from the API of ACME for a specific date. The data will be saved in
    `<directory>/bronze/` with the name `props_{created_at}.json`.
    '''
    # Make a GET request to the API endpoint
    try:
        # Extract property data from the API of ACME
        response = requests.get(f"http://localhost:12345/api/properties/{created_at}", timeout=10)
    except requests.RequestException:
        print("Error: Cannot connect to the API. Please check if the API is running and the URL is correct.")
        return False

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Save the data to a json file
        with open(os.path.join(directory, 'bronze', f"props_{created_at}.json"), "w") as f:
            json.dump(data, f, indent=2)
    else:
        print(f"Error: Failed to fetch data from API. Status code: {response.status_code}")
        return False

    return True


def main(start_date: str, directory: str = "."):
    extract_props(start_date, directory)
    

if __name__ == "__main__":
    main(*sys.argv[1:])