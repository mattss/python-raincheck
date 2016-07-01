import requests
import sys
from datetime import datetime, timedelta

API_URL = 'https://api.forecast.io/forecast'
# How many hours ahead should we show alerts for?
FORECAST_HOURS = 18


class RainChecker(object):

    def __init__(self, api_key, lat, lng):
        self.api_key = api_key
        self.latitude = lat
        self.longitude = lng

    def _offset_date(self, thedate, offset_hours):
        """Convert a date to local time using the offset"""
        return thedate + timedelta(hours=offset_hours)

    def _get_feed_data(self):
        """Grab raw data from forecast.io api"""
        url = "{base}/{key}/{lat},{lng}".format(
            base=API_URL,
            key=self.api_key,
            lat=self.latitude,
            lng=self.longitude,
        )
        response = requests.get(url)
        return response.json()

    def _parse_feed_data(self, data):
        """Parse the feed and find the next rain"""
        offset = data['offset']
        items = data['hourly']['data']
        high = None
        low = None
        for i, item in enumerate(items):
            if i >= FORECAST_HOURS:
                break
            if item.get('precipType'):
                prob = item['precipProbability']
                percentage = prob * 100
                amount = item['precipIntensity']
                print(prob, amount)
                if prob > 0.1 and amount > 0.005:
                    date = self._offset_date(
                        datetime.fromtimestamp(item['time']),
                        offset,
                    )
                    result = {
                        'date': date,
                        'summary': item['summary'],
                        'percentage': percentage
                    }
                    if prob > 0.4 and high is None:
                        high = result
                    elif low is None:
                        low = result
        now = self._offset_date(
            datetime.fromtimestamp(data['currently']['time']),
            offset,
        )
        return {
            'low': low,
            'high': high,
            'summary': data['hourly']['summary'],
            'now': now,
            'offset': offset,
        }

    def check(self):
        data = self._get_feed_data()
        parsed = self._parse_feed_data(data)
        return parsed


if __name__ == "__main__":
    api_key = sys.argv[1]
    checker = RainChecker(api_key, 51.45, -2.6)
    result = checker.check()
    print(result)
