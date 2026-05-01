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