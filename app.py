from flask import Flask, request, jsonify, render_template
from geopy import geocoders
import json
import urllib.request
import os
app = Flask(__name__)

# port = int(os.getenv("PORT"))
from services import returning, function_for_places, main_function


@app.route('/')
def welcome():
    return render_template("home.html")


@app.route('/v1/weather')
def analyze():
    return main_function()

if __name__ == '__main__':
    app.run(debug=True)
