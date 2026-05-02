
# Berlin rental analysis

## 1. Description  

### 1.1 Project

This data engineering project is the development of an ELT pipeline regarding rental data in Berlin.

### 1.2 Process

The pipeline extracts data from external sources. Here, the data are provided by the fictional company ACME through its API, and through transformations we will generate dashboards for getting some insights. The pipeline is fully automated leveraging an orchestration flow through sceduling tasks.  

## 2. Architecture  

![elt_pipeline](/elt_pipeline.png)

## 3. Technical details

### 3.1 Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Prefect | Workflow management |
| **Data Validation** | JSON Schema | Type safety |
| **Data Processing** | Polars | High-performance DataFrame operations |
| **Storage** | Parquet + DuckDB | Columnar storage & analytics |
| **Transformation** | dbt | SQL-based modeling |
| **Visualization** | Streamlit + Plotly | Interactive dashboards |


### 3.2 Medallion data architecture

(Bronze -> Silver -> Gold)

| Bronze | Silver | Gold |
|-|-|-|
| json | parquet | DuckDB |
| raw, immutable data | cleaned data | aggregated |

#### 3.2.1 Bronze Layer (Json)

- raw immutable data
- saved as extracted to `bronze/` with no transformations involved preverving original data

The code in `elt_bronze.py`:  

``` python
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
```

#### 3.2.2 Silver Layer (Parquet)

- Hive partition schema for applying to any data architecture
- Parquet files save less space and can speed up the process of analytics
- Partition per day
- Column pruning
- Data deduplication

The code in `elt_silver.py`:

``` python
import polars as pl
import sys
from pathlib import Path

def transform_props(created_at: str, main_directory: str = "."):
    bronze_dir = Path(main_directory) / "bronze"
    silver_dir = Path(main_directory) / "silver" / f'date={created_at}'

    # add Hive style partitioning to the output path
    input_path = bronze_dir / f"props_{created_at}.json"
    silver_dir.mkdir(parents=True, exist_ok=True)
    output_path = silver_dir / f"props_{created_at}.parquet"

    df = pl.read_json(
        input_path,
        schema={
            "id": pl.String,
            "title": pl.String,
            "description": pl.String,
            "property_type": pl.String,
            "cold_rent": pl.Int64,
            "warm_rent": pl.Int64,
            "deposit": pl.Int64,
            "area_m2": pl.Float64,
            "rooms": pl.Int64,
            "bathrooms": pl.Int64,
            "location": pl.Struct([pl.Field("lat", pl.Float64), pl.Field("lng", pl.Float64)]),
            "address": pl.String,
            "neighborhood": pl.String,
            "zip_code": pl.String,
            "floor": pl.Int64,
            "total_floors": pl.Int64,
            "year_built": pl.Int64,
            "furnishing": pl.String,
            "has_gas": pl.Boolean,
            "heating_type": pl.String,
            "has_elevator": pl.Boolean,
            "has_parking": pl.Boolean,
            "has_balcony": pl.Boolean,
            "pets_allowed": pl.Boolean,
            "available_from": pl.String,
            "nearest_u_s_distance": pl.Int64,
            "nearest_bus_tram_distance": pl.Int64,
            "nearest_school_distance": pl.Int64,
            "nearest_hospital_distance": pl.Int64,
            "nearest_supermarket_distance": pl.Int64,
            "air_quality_index": pl.Int64,
            "noise_level": pl.Float64,
            "energy_efficiency": pl.String,
            "created_at": pl.String,
        }
    )

    initial_len = df.height
    df = df.unique(subset=["id"], keep="first")
    dropped = initial_len - df.height
    if dropped:
        print(f"Dropped {dropped} duplicates.")

    # Drop columns (ignore missing to avoid error)
    df = df.drop(["id", "title", "description", "address"], strict=False)

    df.write_parquet(output_path)


def main(created_at: str, main_directory: str = "."):
    silver_dir = Path(main_directory) / "silver"
    silver_dir.mkdir(parents=True, exist_ok=True)
    transform_props(created_at=created_at, main_directory=main_directory)

if __name__ == "__main__":
    main(*sys.argv[1:])
```

#### 3.2.3 Gold Layer (DuckDB)

- `rent_trend`: Quarterly average warm rent
- `nb_rent_ranking`: Neighborhoods ranked by rent
- `nb_listings`: Property count per neighborhood
- `furnished_impact`: Rent comparison by furnishing
- `furnished_percentage`: Market share distribution

The code in `elt_gold.py`:

``` python
import subprocess
import sys

def dbt_transform(path: str = './rental_dbt'):
    """
    Runs dbt run to transform Silver -> Gold tables.
    """
    try:
        # Run dbt in the project directory
        result = subprocess.run(
            ["dbt", "run"],
            check=True,
            capture_output=True,
            text=True,
            cwd=path
        )
        print("dbt run completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"dbt run failed: {e.stderr}")
        raise e
    
if __name__ == "__main__":
    dbt_transform(*sys.argv[1:])
```

Here is a query for getting the neighborhood rent rankings:

``` sql
WITH neighborhood_stats AS (
    SELECT 
        neighborhood,
        COUNT(*) as num_properties,
        AVG(warm_rent) as avg_warm_rent,
        MEDIAN(warm_rent) as median_warm_rent,
        MIN(warm_rent) as min_warm_rent,
        MAX(warm_rent) as max_warm_rent
    FROM {{ source('rental_data', 'properties') }}
    WHERE warm_rent IS NOT NULL 
        AND warm_rent > 0
        AND neighborhood IS NOT NULL
        AND neighborhood != ''
    GROUP BY neighborhood
    HAVING COUNT(*) >= 5  -- Only neighborhoods with at least 5 properties
)
SELECT 
    neighborhood,
    num_properties,
    ROUND(avg_warm_rent, 2) as avg_warm_rent,
    median_warm_rent,
    RANK() OVER (ORDER BY avg_warm_rent DESC) as rank_highest,
    RANK() OVER (ORDER BY avg_warm_rent ASC) as rank_lowest
FROM neighborhood_stats
ORDER BY avg_warm_rent DESC
```

### 3.3 Orchestration

The entire ELT process is orchestrated. Some features include:  

- Task dependency management
- Error handling and retries
- Scheduled execution (cron-based)
- Docker container support

The pipeline:  

``` python
from prefect import flow, task
from datetime import datetime, timedelta
from elt_tobronze import extract_props
from elt_tosilver import transform_props
from elt_togold import dbt_transform

@task
def elt_bronze(date: str, main_dir: str):
    return extract_props(date, main_dir)

@task
def elt_silver(date: str, main_dir: str):
    transform_props(date, main_dir)

@task
def elt_gold():
    dbt_transform()

@flow
def rental_pipeline():
    date = (datetime.now() - timedelta(days=1)).date().isoformat()
    print(f"🚀 Running rental pipeline for date: {date}")
    
    # If transform MUST run after extract completes:
    extract_result = elt_bronze(date, 'rental_data')
    if not extract_result:
        raise Exception('Error: Data extraction was unsuccessful.')
    print(f"✅ Extraction completed!")
    elt_silver(date, 'rental_data')
    print(f"✅ Transformation completed!")
    elt_gold()
    print(f"✅ Database updated!")

# if __name__ == "__main__":
#     rental_pipeline.serve(
#         name='rental-pipeline',
#         cron='* * * * *',
#     )

if __name__ == "__main__":
    rental_pipeline.deploy(
        name="my-deployment",
        work_pool_name="my-work-pool",
        image="localhost/rental-pipeline:latest",
        build=False,  # Skip building, use existing image
        push=False,
    )
```

**Note:**  
To reproduce the pipeline for debugging / testing comment the part `rental_pipeline.deploy(...)`, uncomment `rental_pipeline.serve(...)` and run it with:
``` bash
uv run pipeline_prefect.py
```

The end result: data visualizations displayed on web-based dashboards built with Streamlit.

```python
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    conn = duckdb.connect('rental_data/gold/dev.duckdb')
    data = {
        'trend': conn.execute("SELECT * FROM rent_trend").df(),
        'rankings': conn.execute("SELECT * FROM nb_rent_ranking").df(),
        'listings': conn.execute("SELECT * FROM nb_listings").df(),
        'furnished': conn.execute("SELECT * FROM furnished_impact").df(),
        'pct': conn.execute("SELECT * FROM furnished_percentage").df()
    }
    conn.close()
    return data

def main():
    st.set_page_config(layout="wide")
    st.title("Rental Market Analysis")

    data = load_data()

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Rent Trend")
        fig = px.line(data['trend'], x='quarter', y='avg_warm_rent')
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("Properties per Neighborhood")
        fig = px.bar(data['listings'].head(10), x='neighborhood', y='total_properties')
        st.plotly_chart(fig, width='stretch')
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Top Neighborhoods by Rent")
        fig = px.bar(data['rankings'].head(10), x='neighborhood', y='avg_warm_rent')
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.subheader("Furnished Premium")
        fig = px.bar(data['furnished'], x='furnishing_category', y='avg_warm_rent')
        st.plotly_chart(fig, width='stretch')

    with col3:
        st.subheader("Market Composition")
        fig = px.pie(data['pct'], values='percentage', names='percentage')
        st.plotly_chart(fig, width='stretch')

if __name__ == "__main__":
    main()
```

## 4. Setup

1. clone the project.
1. go to `acme/` and run the ACME API by running:
    ``` bash
    podman-compose up -d
    ```
    you should see now that the API runs on `localhost:12345`
    if by giving to the terminal:
    ``` bash
    curl http://localhost:12345/api/properties/2026-01-01
    ```
    you should see a json response.  
    **Note:**  
    For generating a large dataset run the `cachup.py` script. Give the start and the end date of your choice in string isoformat `YYYY-MM-DD` and the path to the `bronze/` directory.  
    E.g.:  
    ```bash
    uv run catchup.py 2022-01-01 2026-04-01 rental_data/bronze
    ```
1. on the main project directory run `podman-compose up`.
you should now see that all services run automatically. The pipeline is sceduled to run once in a day at 02:00.
1. Navigate to `localhost:8501` to view your dashboard analytics.
You should see something similar to this output:

![elt_pipeline](/berlin_rental_analytics.png)

## 5. Future additions

- Addition of unit tests
- Implementation of rerunning the pipeline on failure with exponential decay
- Development of messaging about the pipeline status

## 6. License

No license, developed for demonstration purposes only.







