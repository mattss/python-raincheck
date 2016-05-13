from flask import Flask
from flask import render_template
from weather import update_weather_data

app = Flask(__name__)


@app.route("/check/<key>")
def checkit(key):
    latitude = 51.45
    longitude = 2.5
    weather = update_weather_data(key, latitude, longitude)
    return render_template('hello.html', weather=weather)


@app.route("/")
def home():
    return render_template('hello.html', weather='')

if __name__ == "__main__":
    app.run()
