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