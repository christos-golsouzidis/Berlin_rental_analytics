from prefect import flow, task
from datetime import datetime, timedelta
from elt_tobronze import extract_props
from elt_tosilver import transform_props

@task
def elt_bronze(date: str, main_dir: str):
    return extract_props(date, main_dir)

@task
def elt_silver(date: str, main_dir: str):
    transform_props(date, main_dir)

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
    print(f"✅ Extraction completed!")

    

if __name__ == "__main__":
    rental_pipeline.serve(
        name="rental-pipeline", 
        cron="* * * * *",
    )