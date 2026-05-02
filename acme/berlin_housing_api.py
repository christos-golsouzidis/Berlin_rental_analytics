
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
from enum import Enum
from berlin_housing import HousingDataGenerator, Property
from datetime import datetime

app = FastAPI(title="berlin_housing_API", version="1.0.0")


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Endpoints
@app.get("/")
async def root():
    return {
        "version": "1.1.4",
        "message": "List of accesible endpoints for the Housing Rental API",
        "endpoints": {
            "GET api/properties": "List all properties posted at the current date",
            "GET api/properties/{created_at}": "Get properties by date",
            "GET api/properties/entries/{created_at}" : "Get the number of properties posted at the specific date"
        }
    }


@app.get("/api/properties/",response_model=List[Property])
async def get_properties(limit: int = Query(1000, ge=1, description="Number of properties to return (1-1000)")):
    '''
    Get all properties posted today.
    '''
    try:
        props = []
        property_obj = HousingDataGenerator()
        props_gen = (property_obj.generate().model_dump() for _ in range(property_obj.number_of_properties_to_generate(m=50, s=27)))
        for _ in range(limit):
            try:
                props.append(next(props_gen))
            except StopIteration:
                break
        return props
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/properties/{created_at}", response_model=List[Property])
async def get_property(created_at: str, limit: int = Query(1000, ge=1, description="Number of properties to return (1-1000)")):
    
    if datetime.fromisoformat(created_at).date() > datetime.now().date():
        raise HTTPException(status_code=400, detail="created_at cannot be in the future")
    try:
        props = []
        property_obj = HousingDataGenerator(creation_date=created_at)
        props_gen = (property_obj.generate().model_dump() for _ in range(property_obj.number_of_properties_to_generate(m=50, s=27)))
        for _ in range(limit):
            try:
                props.append(next(props_gen))
            except StopIteration:
                break
        return props
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/api/properties/entries/{created_at}", response_model=int)
async def get_number_of_properties(created_at: str):
    
    if datetime.fromisoformat(created_at).date() > datetime.now().date():
        raise HTTPException(status_code=400, detail="created_at cannot be in the future")
    try:
        property_obj = HousingDataGenerator(creation_date=created_at)
        return len([property_obj.generate().model_dump() for _ in range(property_obj.number_of_properties_to_generate(m=50, s=27))])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=12345)
