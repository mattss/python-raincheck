import requests
import sys

API_URL = 'https://api.forecast.io/forecast'


def update_weather_data(api_key, lat, lng):
    url = "{base}/{key}/{lat},{lng}".format(
        base=API_URL,
        key=api_key,
        lat=lat,
        lng=lng,
    )
    response = requests.get(url)
    return response.content

if __name__ == "__main__":
    api_key = sys.argv[1]
    result = update_weather_data(api_key, 52, 2.5)
    print(result)
