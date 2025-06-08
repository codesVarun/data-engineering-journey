import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import pandas as pd  # required to avoid hidden runtime issues

load_dotenv()

def get_database_uri():
    return f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@" \
           f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

def load_data(df_continents: pd.DataFrame, df_countries: pd.DataFrame):
    engine = create_engine(get_database_uri())

    if not isinstance(engine, Engine):
        raise TypeError("Expected a SQLAlchemy Engine object")

    with engine.connect() as connection:
        df_continents.to_sql("covid_continent_stats", connection, if_exists="append", index=False)
        df_countries.to_sql("covid_continent_countries", connection, if_exists="append", index=False)