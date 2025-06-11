import streamlit as st
import pandas as pd
import plotly.express as px

from include.config import get_db_connection
from include.sql.query import COVID_CONTINENT_CASES_LAST_30_DAYS


def load_data():
    conn = get_db_connection()
    df = pd.read_sql(COVID_CONTINENT_CASES_LAST_30_DAYS, conn)
    conn.close()
    return df


def show_dashboard(df: pd.DataFrame):
    st.title("COVID-19 Dashboard")
    if df.empty:
        st.warning("No data available for the last 30 days.")
        return

    fig = px.bar(df, x="continent", y="cases", color="continent", title="COVID-19 Cases by Continent")

    st.plotly_chart(fig)


def main():
    df = load_data()
    show_dashboard(df)


if __name__ == "__main__":
    main()
