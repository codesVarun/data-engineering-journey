import pandas as pd
from datetime import datetime

def transform_continent_data(raw_data):
    if not raw_data:
        print("⚠️ Warning: No data to transform.")
        return pd.DataFrame(), pd.DataFrame()

    continent_records = []
    country_records = []

    for continent in raw_data:
        base_record = {
            "continent": continent.get("continent"),
            "cases": continent.get("cases"),
            "deaths": continent.get("deaths"),
            "recovered": continent.get("recovered"),
            "active": continent.get("active"),
            "critical": continent.get("critical"),
            "tests": continent.get("tests"),
            "population": continent.get("population"),
            "updated": pd.to_datetime(continent.get("updated"), unit="ms", errors="coerce"),
            "lat": continent.get("continentInfo", {}).get("lat"),
            "long": continent.get("continentInfo", {}).get("long"),
            "etl_timestamp": datetime.utcnow()
        }
        continent_records.append(base_record)

        for country in continent.get("countries", []):
            country_records.append({
                "continent": base_record["continent"],
                "country": country,
                "etl_timestamp": base_record["etl_timestamp"]
            })

    return pd.DataFrame(continent_records), pd.DataFrame(country_records)