import subprocess


def main(path: str):
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
            cwd=path # Or path to your dbt project
        )
        print("dbt run completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"dbt run failed: {e.stderr}")
        raise e
    
if __name__ == "__main__":
    main('rental_data_analytics')