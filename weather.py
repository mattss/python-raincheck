import requests
import os
from datetime import datetime, timedelta

API_URL = 'https://api.forecast.io/forecast'
API_KEY = os.environ['API_KEY']
GEO_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
# How many hours ahead should we show alerts for?
FORECAST_HOURS = 18


class RainChecker(object):

    def __init__(self, lat, lng):
        self.latitude = lat
        self.longitude = lng

    def _offset_date(self, thedate, offset_hours):
        """Convert a date to local time using the offset"""
        return thedate + timedelta(hours=offset_hours)

    def _get_feed_data(self):
        """Grab raw data from forecast.io api"""
        url = "{base}/{key}/{lat},{lng}".format(
            base=API_URL,
            key=API_KEY,
            lat=self.latitude,
            lng=self.longitude,
        )
        response = requests.get(url)
        return response.json()

    def _get_location(self):
        """Grab location data from lat/lng"""
        url = "{base}?latlng={lat},{lng}".format(
            base=GEO_URL,
            lat=self.latitude,
            lng=self.longitude,
        )
        response = requests.get(url)
        results = response.json()['results']
        try:
            return results[0]['formatted_address']
        except IndexError:
            return '(unknown location)'

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
        result = self._parse_feed_data(data)
        location = self._get_location()
        result['location'] = location
        summary = result['summary'].lower()
        if 'sunny' in summary:
            result['icon'] = 'sun'
        elif 'clear' in summary:
            result['icon'] = 'sun'
        elif 'rain' in summary:
            result['icon'] = 'rain'
        else:
            result['icon'] = 'cloud'
        return result


if __name__ == "__main__":
    checker = RainChecker(51.4607289, -2.5870727)
    result = checker.check()
    from pprint import pprint
    pprint(result)
