import pandas as pd
from datetime import datetime, timezone
import logging

def transform_continent_data(raw_data):
    if not raw_data:
        logging.warning("⚠️ Warning: No data to transform.")
        return pd.DataFrame(), pd.DataFrame()

    continent_records = []
    country_records = []

    for continent in raw_data:
        etl_time = datetime.now(timezone.utc)

        base_record = {
            "continent": continent.get("continent", ""),
            "cases": continent.get("cases", 0),
            "deaths": continent.get("deaths", 0),
            "recovered": continent.get("recovered", 0),
            "active": continent.get("active", 0),
            "critical": continent.get("critical", 0),
            "tests": continent.get("tests", 0),
            "population": continent.get("population", 0),
            "updated": pd.to_datetime(continent.get("updated"), unit="ms", errors="coerce"),
            "lat": continent.get("continentInfo", {}).get("lat", None),
            "long": continent.get("continentInfo", {}).get("long", None),
            "etl_timestamp": etl_time
        }
        continent_records.append(base_record)

        for country in continent.get("countries", []):
            country_records.append({
                "continent": base_record["continent"],
                "country": country,
                "etl_timestamp": etl_time
            })

    return pd.DataFrame(continent_records), pd.DataFrame(country_records)