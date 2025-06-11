COVID_CONTINENT_CASES_LAST_30_DAYS = """
SELECT DISTINCT ON (continent)
  continent,
  cases,
  deaths,
  recovered,
  TO_TIMESTAMP(updated / 1000)::date AS date,
  TO_TIMESTAMP(etl_timestamp / 1000) AS loaded_at
FROM covid_continent_stats
ORDER BY continent, updated DESC;
"""