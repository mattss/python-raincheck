from flask import Flask
from flask import render_template
from weather import RainChecker

app = Flask(__name__)


@app.route("/check/<location>")
def checkit(location):
    latitude, longitude = location.split(',')
    checker = RainChecker(latitude, longitude)
    weather = checker.check()
    return render_template('hello.html', weather=weather)


@app.route("/")
def home():
    return render_template('hello.html', weather=None)

if __name__ == "__main__":
    app.run()
