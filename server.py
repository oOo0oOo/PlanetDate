import logging

from flask import Flask, render_template
from utils import get_planet_dates, PLANETS

app = Flask(__name__)

@app.route('/')
def landing():
    planet_data = [list(PLANETS)] + list(get_planet_dates())
    return render_template('landing.html',
        type=type,planet_data=zip(*planet_data))

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500