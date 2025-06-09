from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import logging

def load_data(df_continents, df_countries):
    try:
        logging.info("Loading data to database...")

        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
        
        # Drop existing tables
        postgres_hook.run("DROP TABLE IF EXISTS covid_continent_stats;")
        postgres_hook.run("DROP TABLE IF EXISTS covid_country_stats;")
        
        logging.info("Creating tables...")
        
        # Get column info from DataFrames and create tables dynamically
        def get_column_type(series):
            if series.dtype == 'object':
                return 'TEXT'
            elif series.dtype in ['int64', 'int32']:
                return 'BIGINT'
            elif series.dtype in ['float64', 'float32']:
                return 'FLOAT'
            else:
                return 'TEXT'
        
        # Create continent table
        continent_cols = []
        for col in df_continents.columns:
            col_type = get_column_type(df_continents[col])
            continent_cols.append(f'"{col}" {col_type}')
        
        create_continent_sql = f"""
        CREATE TABLE covid_continent_stats (
            {', '.join(continent_cols)}
        );
        """
        
        postgres_hook.run(create_continent_sql)
        
        # Create country table
        country_cols = []
        for col in df_countries.columns:
            col_type = get_column_type(df_countries[col])
            country_cols.append(f'"{col}" {col_type}')
        
        create_country_sql = f"""
        CREATE TABLE covid_country_stats (
            {', '.join(country_cols)}
        );
        """
        
        postgres_hook.run(create_country_sql)
        
        # Insert continent data
        logging.info(f"Loading {len(df_continents)} continent records...")
        
        continent_data = []
        for _, row in df_continents.iterrows():
            # Convert row to list, handling NaN values
            row_data = []
            for val in row.values:
                if pd.isna(val):
                    row_data.append(None)
                else:
                    row_data.append(val)
            continent_data.append(tuple(row_data))
        
        postgres_hook.insert_rows(
            table="covid_continent_stats",
            rows=continent_data,
            target_fields=[f'"{col}"' for col in df_continents.columns]
        )
        
        # Insert country data
        logging.info(f"Loading {len(df_countries)} country records...")
        
        country_data = []
        for _, row in df_countries.iterrows():
            # Convert row to list, handling NaN values
            row_data = []
            for val in row.values:
                if pd.isna(val):
                    row_data.append(None)
                else:
                    row_data.append(val)
            country_data.append(tuple(row_data))
        
        postgres_hook.insert_rows(
            table="covid_country_stats",
            rows=country_data,
            target_fields=[f'"{col}"' for col in df_countries.columns]
        )

        logging.info("✅ Data loaded successfully!")

    except Exception as e:
        logging.error(f"❌ Error loading data: {str(e)}")
        logging.error(f"Continent columns: {list(df_continents.columns)}")
        logging.error(f"Country columns: {list(df_countries.columns)}")
        raise