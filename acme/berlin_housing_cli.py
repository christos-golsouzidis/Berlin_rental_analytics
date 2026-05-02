
from pprint import pprint
from berlin_housing import HousingDataGenerator
from datetime import datetime
import random
import sys


def main(creation_date: str = "2026-01-01"):
    random.seed(creation_date)
    property_obj = HousingDataGenerator(creation_date=creation_date)
    pprint(property_obj.generate().model_dump())

if __name__ == "__main__":
    main(
        creation_date=sys.argv[1] if len(sys.argv) > 1 else "2026-01-01"
    )
    