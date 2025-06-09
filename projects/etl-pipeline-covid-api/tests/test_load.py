from load import load_data
import pandas as pd

df_continents = pd.DataFrame({
    'continent': ['Asia', 'Europe'],
    'cases': [1000, 2000]
})

df_countries = pd.DataFrame({
    'country': ['India', 'Germany'],
    'cases': [500, 700]
})

load_data(df_continents, df_countries)
