from flask import Flask
from flask import render_template
from weather import RainChecker

app = Flask(__name__)


@app.route("/check/<key>")
def checkit(key):
    latitude = 51.45
    longitude = 2.5
    checker = RainChecker(key, latitude, longitude)
    weather = str(checker.check())
    return render_template('hello.html', weather=weather)


@app.route("/")
def home():
    return render_template('hello.html', weather='')

if __name__ == "__main__":
    app.run()
