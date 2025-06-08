import requests

def fetch_covid_data(url="https://disease.sh/v3/covid-19/continents"):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching COVID data: {e}")
        raise