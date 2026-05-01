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