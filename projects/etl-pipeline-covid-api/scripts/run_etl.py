from extract import fetch_covid_data
from transform import transform_continent_data
from load import load_data

def run_etl():
    raw_data = fetch_covid_data()
    df_continents, df_countries = transform_continent_data(raw_data)
    load_data(df_continents, df_countries)

if __name__ == "__main__":
    run_etl()
    print("🏁 Starting ETL")
    run_etl()
    print("✅ ETL completed successfully")