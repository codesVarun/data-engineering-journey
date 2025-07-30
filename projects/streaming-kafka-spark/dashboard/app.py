# dashboard/app.py
import streamlit as st
import pandas as pd
import psycopg2
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 10 seconds (10,000 milliseconds)
st_autorefresh(interval=10_000, key="datarefresh")

st.set_page_config(page_title="Streaming Events Dashboard", layout="wide")
st.title("📊 Streaming Events (Kafka → Spark → Postgres)")

# Connect to PostgreSQL running in Docker
conn = psycopg2.connect(
    host="postgres_streaming",
    port="5432",
    database="streaming_db",
    user="postgres",
    password="postgres"
)

query = """
SELECT 
    event_id, user_id, product, action, timestamp, 
    session_id, price, quantity, category, country, city, created_at
FROM events
ORDER BY created_at DESC
LIMIT 100;
"""

df = pd.read_sql(query, conn)
conn.close()

st.dataframe(df, use_container_width=True)

if not df.empty:
    st.subheader("🔁 Action Counts")
    st.bar_chart(df["action"].value_counts())