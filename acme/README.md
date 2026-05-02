# ACME Berlin housing API

## Description

ACME is a fictional company that provides fake data about renting properties (appartments, houses and studios) in the city of Berlin in Germany.
The API is very simple and minimal and is used only for generating a synthetic dataset, trying though to simulate a real world dataset.
Although APIs are normally more complex than this, it is sufficient for the purposes of data analysis on the real estate dataset.

## Endpoints

- `GET '/'`:
    Shows if the server runs providing the info of using the API endpoints

- `GET '/api/properties/'`
    Gets all the available entries of a property registered at the current date.
    - Query params:
        limit (ge=1 le=1000)

- `GET '/api/properties/{date}'`
    Gets all the available entries of a property registered at the specified date.
    - Query params:
        limit (ge=1 le=1000)

- `GET '/api/properties/entries/{date}'`
    Gets the number of all properties registered at the specified date.

## Examples

- GET `/`:
    ```json
    {
        "message": "List of accesible endpoints for the Housing Rental API",
        "endpoints": {
            "GET api/properties": "List all properties with filters",
            "GET api/properties/{created_at}": "Get properties by date",
            "GET api/properties/entries/{created_at}" : "Get the number of properties posted at the specific date"
        }
    }
    ```

- GET `/api/properties?limit=2`
    ```json
    [
        {
            "id": "b1515425-423e-474f-a919-c846736b3d17",
            "title": "Charming studio with Character in Pankow",
            "description": "Recently renovated studio with modern finishes. Close to public transport.",
            "property_type": "studio",
            "cold_rent": 772,
            "warm_rent": 954,
            "deposit": 2316,
            "area_m2": 43.99,
            "rooms": 1,
            "bathrooms": 1,
            "location": {
            "lat": 52.55938,
            "lng": 13.42679
            },
            "address": "Brücke Weg 168",
            "neighborhood": "Pankow",
            "zip_code": "13109",
            "floor": 1,
            "total_floors": 5,
            "year_built": 2020,
            "furnishing": "semi-furnished",
            "has_gas": false,
            "heating_type": "fernheizung",
            "has_elevator": true,
            "has_parking": true,
            "has_balcony": false,
            "pets_allowed": null,
            "available_from": "2026-04-01",
            "nearest_u_s_distance": 2227,
            "nearest_bus_tram_distance": 814,
            "nearest_school_distance": 2910,
            "nearest_hospital_distance": 717,
            "nearest_supermarket_distance": 1262,
            "air_quality_index": 32,
            "noise_level": 3.0,
            "energy_efficiency": "E",
            "created_at": "2026-03-19"
        },
        {
            "id": "9262c129-70e1-4014-9b29-2060a4976b93",
            "title": "Stylish apartment in Prime Location",
            "description": "Beautiful apartment located in the heart of Lichtenberg. Features include ample storage space.",
            "property_type": "apartment",
            "cold_rent": 1023,
            "warm_rent": 1178,
            "deposit": 3069,
            "area_m2": 46.41,
            "rooms": 2,
            "bathrooms": 1,
            "location": {
            "lat": 52.50065,
            "lng": 13.49946
            },
            "address": "Brücke Weg 81",
            "neighborhood": "Lichtenberg",
            "zip_code": "13045",
            "floor": 0,
            "total_floors": 1,
            "year_built": 1998,
            "furnishing": "unfurnished",
            "has_gas": true,
            "heating_type": "gas",
            "has_elevator": true,
            "has_parking": true,
            "has_balcony": false,
            "pets_allowed": true,
            "available_from": "2026-05-09",
            "nearest_u_s_distance": 856,
            "nearest_bus_tram_distance": 198,
            "nearest_school_distance": 1478,
            "nearest_hospital_distance": 7696,
            "nearest_supermarket_distance": 646,
            "air_quality_index": 33,
            "noise_level": 2.0,
            "energy_efficiency": "A+",
            "created_at": "2026-03-19"
        }
    ]
    ```

- GET `/api/properties/2026-01-15?limit=2`
    ```json
    [
        {
            "id": "f5e6b104-0a83-46b9-b569-f157f2412243",
            "title": "Renovated apartment Near Public Transport",
            "description": "Beautiful apartment located in the heart of Neukölln. Features include central air conditioning.",
            "property_type": "apartment",
            "cold_rent": 1758,
            "warm_rent": 2052,
            "deposit": 5274,
            "area_m2": 94.1,
            "rooms": 4,
            "bathrooms": 2,
            "location": {
            "lat": 52.43619,
            "lng": 13.46296
            },
            "address": "Tor Allee 59",
            "neighborhood": "Neukölln",
            "zip_code": "12203",
            "floor": 3,
            "total_floors": 4,
            "year_built": 1960,
            "furnishing": "semi-furnished",
            "has_gas": false,
            "heating_type": "electric",
            "has_elevator": true,
            "has_parking": null,
            "has_balcony": true,
            "pets_allowed": true,
            "available_from": "2026-02-10",
            "nearest_u_s_distance": 1191,
            "nearest_bus_tram_distance": 691,
            "nearest_school_distance": 2581,
            "nearest_hospital_distance": 5241,
            "nearest_supermarket_distance": 915,
            "air_quality_index": 48,
            "noise_level": 5.0,
            "energy_efficiency": "F",
            "created_at": "2026-01-15"
        },
        {
            "id": "009e3ec4-4052-42d2-bd09-255b17e10e27",
            "title": "Charming apartment with Character in Spandau",
            "description": "Luxury living in this stunning apartment. Includes premium appliances and finishes.",
            "property_type": "apartment",
            "cold_rent": 1087,
            "warm_rent": 1274,
            "deposit": 3261,
            "area_m2": 47.72,
            "rooms": 2,
            "bathrooms": 1,
            "location": {
            "lat": 52.53755,
            "lng": 13.16107
            },
            "address": "Otto Weg 38",
            "neighborhood": "Spandau",
            "zip_code": "13582",
            "floor": 4,
            "total_floors": 5,
            "year_built": 1972,
            "furnishing": "furnished",
            "has_gas": false,
            "heating_type": "oil",
            "has_elevator": true,
            "has_parking": null,
            "has_balcony": true,
            "pets_allowed": false,
            "available_from": "2026-02-05",
            "nearest_u_s_distance": 616,
            "nearest_bus_tram_distance": 246,
            "nearest_school_distance": 3941,
            "nearest_hospital_distance": 2244,
            "nearest_supermarket_distance": 528,
            "air_quality_index": 36,
            "noise_level": 3.0,
            "energy_efficiency": "G",
            "created_at": "2026-01-15"
        }
    ]
    ```
    
- GET `/api/properties/entries/2026-01-15`  
    `48`