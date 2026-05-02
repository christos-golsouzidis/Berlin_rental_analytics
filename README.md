
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

#### 3.2.2 Silver Layer (Parquet)

- Hive partition schema for applying to any data architecture
- Parquet files save less space and can speed up the process of analytics
- Partition per day
- Column pruning
- Data deduplication

#### 3.2.3 Gold Layer (DuckDB)

- `rent_trend`: Quarterly average warm rent
- `nb_rent_ranking`: Neighborhoods ranked by rent
- `nb_listings`: Property count per neighborhood
- `furnished_impact`: Rent comparison by furnishing
- `furnished_percentage`: Market share distribution

### 3.3 Orchestration

The entire ELT process is orchestrated. Some features include:  

- Task dependency management
- Error handling and retries
- Scheduled execution (cron-based)
- Docker container support

**Note:**  
To reproduce the pipeline for debugging / testing comment the part `rental_pipeline.deploy(...)`, uncomment `rental_pipeline.serve(...)` and run it with:
``` bash
uv run pipeline_prefect.py
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







