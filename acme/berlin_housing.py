from enum import Enum
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pydantic import BaseModel

# Data Models
class PropertyType(Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    STUDIO = "studio"

class Furnishing(Enum):
    FURNISHED = "furnished"
    SEMI_FURNISHED = "semi-furnished"
    UNFURNISHED = "unfurnished"

class HeatingType(Enum):
    GAS = "gas"
    ELECTRIC = "electric"
    OIL = "oil"
    FERNHEIZUNG = "fernheizung"
    NONE = "none"

class Neighborhood(Enum):
    CHARLOTTENBURG_WILMERSDORF = "Charlottenburg-Wilmersdorf"
    FRIEDRICHSHAIN_KREUZBERG = "Friedrichshain-Kreuzberg"
    LICHTEBERG = "Lichtenberg"
    MARZAHN_HELLERSDORF = "Marzahn-Hellersdorf"
    MITTE = "Mitte"
    NEUKOELLN = "Neukölln"
    PANKOW = "Pankow"
    REINICKENDORF = "Reinickendorf"
    SPANDAU = "Spandau"
    STEGLITZ_ZEHLENDORF = "Steglitz-Zehlendorf"
    TEMPELHOF_SCHOENEBERG = "Tempelhof-Schöneberg"
    TREPTOW_KOEPENICK = "Treptow-Köpenick"


class Property(BaseModel):
    id: str
    title: str
    description: str
    property_type: PropertyType
    cold_rent: int
    warm_rent: int
    deposit: int
    area_m2: float
    rooms: int
    bathrooms: int
    location: Dict[str, float]  # lat, lng
    address: str
    neighborhood: Neighborhood
    zip_code: str
    floor: Optional[int] = None
    total_floors: Optional[int] = None
    year_built: int
    furnishing: Furnishing
    has_gas: Optional[bool] = None
    heating_type: HeatingType
    has_elevator: Optional[bool] = None
    has_parking: Optional[bool] = None
    has_balcony: Optional[bool] = None
    pets_allowed: Optional[bool] = None
    available_from: str
    nearest_u_s_distance: int  # meters
    nearest_bus_tram_distance: int  # meters
    nearest_school_distance: int  # meters
    nearest_hospital_distance: int  # meters
    nearest_supermarket_distance: int  # meters
    air_quality_index: Optional[int]  # 0-100, lower is better
    noise_level: Optional[float]  # 0-10, lower is quieter
    energy_efficiency: str  # A-G
    created_at: str
    

# Data Generator Class
class HousingDataGenerator(Property):
    def __init__(self, creation_date: Optional[str] = None):
        super().__init__(
            id="",
            title="",
            description="", 
            property_type=PropertyType.APARTMENT,
            cold_rent=0,
            warm_rent=0,
            deposit=0,
            area_m2=0.0,
            rooms=0,
            bathrooms=0,
            location={"lat": 0.0, "lng": 0.0},
            address="",
            neighborhood=Neighborhood.MITTE,
            zip_code="",
            floor=None,
            total_floors=None,
            year_built=0,
            furnishing=Furnishing.UNFURNISHED,
            has_gas=None,
            heating_type=HeatingType.NONE,
            has_elevator=None,
            has_parking=None,
            has_balcony=None,
            pets_allowed=None,
            available_from="",
            nearest_u_s_distance=0,
            nearest_bus_tram_distance=0,
            nearest_school_distance=0,
            nearest_hospital_distance=0,
            nearest_supermarket_distance=0,
            air_quality_index=None,
            noise_level=None,
            energy_efficiency="",
            created_at=creation_date or ''
        )
        self.created_at = creation_date or datetime.now().date().isoformat()
        random.seed(self.created_at)

    def generate(self) -> Property:

        property_titles = [
            "Modern {type} in {neighborhood} Berlin",
            "Spacious {type} with Great Views",
            "Renovated {type} Near Public Transport",
            "Luxury {type} with Amenities in {neighborhood}",
            "Cozy {type} in Quiet Area in Berlin",
            "Bright {type} with Natural Light",
            "Newly Built {type} in {neighborhood}",
            "Affordable {type} in {neighborhood} Berlin",
            "Stylish {type} in Prime Location",
            "Charming {type} with Character in {neighborhood}",
            "Elegant {type} with Modern Finishes in {neighborhood}",
            "{rooms}-Room {type} in {neighborhood} Berlin",
            "Spacious {type} with {rooms} Rooms in {neighborhood}",
        ]
        
        property_descriptions = [
            "Beautiful {type} located in the heart of {neighborhood}. Features include {features}.",
            "Recently renovated {type} with modern finishes. Close to public transport.",
            "This charming {type} offers {features}. Located in a safe and convenient area.",
            "Luxury living in this stunning {type}. Includes premium appliances and finishes."
        ]
        
        features = [
            "hardwood floors", "granite countertops", "stainless steel appliances",
            "in-unit laundry", "central air conditioning", "smart home features",
            "large windows", "walk-in closets", "updated kitchen", "modern bathrooms",
            "renovated interior", "energy-efficient appliances", "ample storage space",
        ]
        foo = lambda : random.randbytes(4).hex()
        self.id = '-'.join([foo(), foo()])
        self.neighborhood = random.choice(list(Neighborhood))
        self.available_from = (datetime.fromisoformat(self.created_at) + timedelta(days=random.randint(0, 90))).date().isoformat()
        self.address = " ".join([random.choice(['Hansa', 'Münster', 'Kaiser', 'Garten', 'Linden', 'Friedrich', 'Karl', 'Brunnen', 'Schiller', 'Goethe',
                                      'Haupt', 'Alexander', 'Wilhelm', 'Gustav', 'Heinrich', 'Anton', 'Lüdwig', 'Max', 'Otto', 'Paul', 'Bad',
                                      'Friedrich', 'Karl', 'Tor', 'Brücke', 'Maximilian', 'Gropius', 'Eduard', 'Paul', 'Ritter', 'Einstein'])\
             , random.choice(['Str', 'Ring', 'Allee', 'Platz', 'Weg', 'Bogen']) , str(random.randint(1, 200))])
        self.has_balcony = random.random() < 0.3666
        self.total_floors = random.choice([0, 1, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6])
        self.floor = random.randint(0, self.total_floors)
        self.has_elevator = random.random() < 0.6 if self.total_floors < 5 else True
        self.pets_allowed = random.choice([True, False, None])
        self.has_parking = random.choice([True, False, None])
        self.year_built = random.randint(1950, 2025)
        self.furnishing = random.choice(list(Furnishing))
        self.heating_type = random.choice(list(HeatingType))
        self.has_gas = random.choice([True, False, None]) if self.heating_type != HeatingType.GAS else True
        self.nearest_u_s_distance = random.randint(50, 3000)
        self.nearest_bus_tram_distance = random.randint(50, 1500)
        if self.neighborhood in [Neighborhood.CHARLOTTENBURG_WILMERSDORF, Neighborhood.MARZAHN_HELLERSDORF, Neighborhood.STEGLITZ_ZEHLENDORF]:
            self.nearest_u_s_distance += random.randint(0, 1000)
        self.air_quality_index = random.randint(23, 88)
        self.noise_level = min(8, random.randint(1, 4) + self.air_quality_index // 20)
        self.nearest_school_distance = random.randint(100, 5000)
        self.nearest_hospital_distance = random.randint(200, 10000)
        self.nearest_supermarket_distance = random.randint(50, 2500)
        self.energy_efficiency = random.choice(['A+','A','B','C','D','E','F','G']) if \
            (self.heating_type != HeatingType.FERNHEIZUNG and self.heating_type != HeatingType.GAS) else random.choice(['A+','A','B','C','D','E'])
        
        self.area_m2 = random.normalvariate(mu=60, sigma=29.2)
        if self.area_m2 < 16:
            self.area_m2 += 120
        
        self.rooms = int(max(1, (self.area_m2 - 7) / random.normalvariate(mu=20.5, sigma=3.5))) # remove 7 m2 for bathroom, then divide by average room size with some randomness

        if self.rooms == 1:
            self.property_type = PropertyType.STUDIO
        elif self.total_floors == 0:
            self.property_type = PropertyType.HOUSE
        else:
            self.property_type = PropertyType.APARTMENT
        
        # Bathrooms based on rooms
        if self.area_m2 < 70:
            self.bathrooms = 1
        elif self.area_m2 > 93:
            self.bathrooms = 2
        else:
            self.bathrooms = random.randint(1, 2)
        
        # generate PLZ based on neighborhood
        neighborhood_plz_ranges = {
            Neighborhood.CHARLOTTENBURG_WILMERSDORF: (14015, 14149), #140
            Neighborhood.FRIEDRICHSHAIN_KREUZBERG: (10243, 10299), #102
            Neighborhood.LICHTEBERG: (13015, 13055), #130
            Neighborhood.MARZAHN_HELLERSDORF: (12679, 12789), #126-7
            Neighborhood.MITTE: (10115, 10179), #101
            Neighborhood.NEUKOELLN: (12043, 12359), #120-3
            Neighborhood.PANKOW: (13105, 13189), #131
            Neighborhood.REINICKENDORF: (13403, 13409), #134
            Neighborhood.SPANDAU: (13581, 13599), #135
            Neighborhood.STEGLITZ_ZEHLENDORF: (14157, 14199), #141
            Neighborhood.TEMPELHOF_SCHOENEBERG: (10823, 10969), #108-9
            Neighborhood.TREPTOW_KOEPENICK: (12435, 12559), #124-5
        }

        # Generate location with some randomness around neighborhood center
        neighborhood_centers = {
            Neighborhood.CHARLOTTENBURG_WILMERSDORF: {
                'lat': 52.4968,
                'lng': 13.3230,
            },
            Neighborhood.FRIEDRICHSHAIN_KREUZBERG: {
                'lat': 52.5135,
                'lng': 13.4191
            },
            Neighborhood.LICHTEBERG: {
                'lat': 52.5257,
                'lng': 13.4979
            },
            Neighborhood.MARZAHN_HELLERSDORF: {
                'lat': 52.5143,
                'lng': 13.5851
            },
            Neighborhood.MITTE: {
                'lat': 52.5335,
                'lng': 13.3837
            },
            Neighborhood.NEUKOELLN: {
                'lat': 52.4490,
                'lng': 13.4908
            },
            Neighborhood.PANKOW: {
                'lat': 52.5570,
                'lng': 13.4163
            },
            Neighborhood.REINICKENDORF: {
                'lat': 52.5702,
                'lng': 13.3580
            },
            Neighborhood.SPANDAU: {
                'lat': 52.5380,
                'lng': 13.1319
            },
            Neighborhood.STEGLITZ_ZEHLENDORF: {
                'lat': 52.4393,
                'lng': 13.2530
            },
            Neighborhood.TEMPELHOF_SCHOENEBERG: {
                'lat': 52.4458,
                'lng': 13.2977
            },
            Neighborhood.TREPTOW_KOEPENICK: {
                'lat': 52.4741,
                'lng': 13.3722
            },
        }

        lat = neighborhood_centers[self.neighborhood]["lat"] + random.uniform(-0.03, 0.03)
        lng = neighborhood_centers[self.neighborhood]["lng"] + random.uniform(-0.03, 0.03)
        self.location = {'lat':lat, 'lng':lng}
        self.zip_code = str(random.randint(*neighborhood_plz_ranges[self.neighborhood]))
        
        # Generate title and description
        title_template = random.choice(property_titles)
        self.title = title_template.format(type=self.property_type.value, neighborhood=self.neighborhood.value, rooms=self.rooms)
        
        description_template = random.choice(property_descriptions)
        self.description = description_template.format(
            type=self.property_type.value,
            neighborhood=self.neighborhood.value,
            features=random.choice(features)
        )

        furnishing_factor = {
            Furnishing.FURNISHED: 1.4,
            Furnishing.SEMI_FURNISHED: 1.2,
            Furnishing.UNFURNISHED: 1.0
        }

        energy_factor = {
            'A+': 1.6,
            'A': 1.4,
            'B': 1.2,
            'C': 1.0,
            'D': 0.8,
            'E': 0.6,
            'F': 0.4,
            'G': 0.2
        }
        rental_year = datetime.fromisoformat(self.created_at).year

        self.cold_rent = 100 + \
            int(random.normalvariate(mu=30, sigma=5) * self.rooms) + \
            int(random.normalvariate(mu=(rental_year - 2001), sigma=4) * 10) + \
            int(random.normalvariate(mu=50, sigma=11.5) if self.property_type == PropertyType.HOUSE else 0) + \
            int(random.normalvariate(mu=11, sigma=1.3) * energy_factor[self.energy_efficiency]) + \
            int(random.normalvariate(mu=19, sigma=1.5) * self.area_m2) + \
            int(random.normalvariate(mu=10, sigma=1.9) * self.floor) + \
            int(random.normalvariate(mu=20, sigma=1.3) * int(self.has_balcony)) + \
            int(random.normalvariate(mu=5, sigma=1.6) * int(self.has_elevator)) + \
            int(random.normalvariate(mu=10, sigma=1.3) * (self.year_built - 1940) / 1000) + \
            int(random.normalvariate(mu=15, sigma=1.3) * furnishing_factor[self.furnishing]) + \
            int(random.normalvariate(mu=8, sigma=1.2) * self.air_quality_index / 10) - \
            int(random.normalvariate(mu=8, sigma=1.3) * self.noise_level) - \
            int(random.normalvariate(mu=13, sigma=1.3) * self.nearest_u_s_distance / 500) - \
            int(random.normalvariate(mu=16, sigma=1.3) * self.nearest_bus_tram_distance / 500) - \
            int(random.normalvariate(mu=16, sigma=1.3) * self.nearest_school_distance / 500) 
        
        self.warm_rent = self.cold_rent + random.randint(0, 100) + self.cold_rent // 9
        self.deposit = self.cold_rent * int(random.normalvariate(mu=3.3, sigma=0.3))

        # finally round area_m2 to 2 decimals and location to 5 decimals for realism
        self.area_m2 = round(self.area_m2, 2)
        self.location['lat'] = round(self.location['lat'], 5)
        self.location['lng'] = round(self.location['lng'], 5)

        return Property(
            id=self.id,
            title=self.title,
            description=self.description,
            property_type=self.property_type,
            cold_rent=self.cold_rent,
            warm_rent=self.warm_rent,
            deposit=self.deposit,
            area_m2=self.area_m2,
            rooms=self.rooms,
            bathrooms=self.bathrooms,
            location=self.location,
            address=self.address,
            neighborhood=self.neighborhood,
            zip_code=self.zip_code,
            floor=self.floor,
            total_floors=self.total_floors,
            year_built=self.year_built,
            furnishing=self.furnishing,
            has_gas=self.has_gas,
            heating_type=self.heating_type,
            has_elevator=self.has_elevator,
            has_parking=self.has_parking,
            has_balcony=self.has_balcony,
            pets_allowed=self.pets_allowed,
            available_from=self.available_from,
            nearest_u_s_distance=self.nearest_u_s_distance,
            nearest_bus_tram_distance=self.nearest_bus_tram_distance,
            nearest_school_distance=self.nearest_school_distance,
            nearest_hospital_distance=self.nearest_hospital_distance,
            nearest_supermarket_distance=self.nearest_supermarket_distance,
            air_quality_index=self.air_quality_index,
            noise_level=self.noise_level,
            energy_efficiency=self.energy_efficiency,
            created_at=self.created_at
        )
    
    def number_of_properties_to_generate(self, m: int = 50, s: int = 27) -> int:
        return max(0, int(random.normalvariate(mu=m, sigma=s)))
                
    def __repr__(self):
        return self.model_dump_json(indent=2)
    
    