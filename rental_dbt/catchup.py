from elt_tobronze import extract_props
from elt_tosilver import transform_props
from datetime import datetime, timedelta
import os
import sys

def elt_props_range(start_date: str, end_date: str, directory: str = "."):
    '''
    Extract property data from the API of ACME for a range of dates. The dates should be in the format YYYY-MM-DD.
    The data will be saved in the `<directory>/bronze/` with the name `props_{created_at}.json`.
    '''
    # start_date must be less than end_date
    if datetime.fromisoformat(start_date).date() > datetime.fromisoformat(end_date).date():
        print("Error: Start_date must be less than end_date")
        return
    
    created_at = start_date
    while True:
        if not extract_props(created_at, directory):
            print(f"Error: Failed to extract data for date: {created_at}")
            return
        
        transform_props(created_at, directory)

        if created_at == end_date:
            break
        created_at = (datetime.fromisoformat(created_at) + timedelta(days=1)).date().isoformat()


def main(start_date: str, end_date: str, directory: str):
    elt_props_range(start_date, end_date, directory)

if __name__ == "__main__":
    main(*sys.argv[1:])