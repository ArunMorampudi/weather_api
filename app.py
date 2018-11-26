from flask import Flask, request, jsonify, render_template
from geopy import geocoders
import json
import urllib.request
import os
app = Flask(__name__)

port = int(os.getenv("PORT"))
from services import returning


def function_for_places(placename):
    response = urllib.request.urlopen(
        'http://api.geonames.org/findNearbyPostalCodesJSON?placename={}&maxRows=1&username=morampudiarun'.format(
            placename)).read()
    return returning(response), 200


@app.route('/')
def welcome():
    return render_template("home.html")


@app.route('/v1/weather')
def analyze():
    lat = request.args.get('lat')
    lng= request.args.get('lng')
    placename = request.args.get('placename')
    state = request.args.get('state')
    city = request.args.get('city')
    countrycode = request.args.get('countrycode')
    if placename:
        placename = placename.replace(" ","%20")
    zipcode = request.args.get('zipcode')
    if zipcode:
        response = urllib.request.urlopen(
            'http://api.geonames.org/postalCodeSearchJSON?postalcode={}&maxRows=1&username=morampudiarun'.format(
                zipcode)).read()
        return returning(response), 200
    elif lat or lng:
        response = urllib.request.urlopen(
            'http://api.geonames.org/findNearbyPostalCodesJSON?lat={}&lng={}&maxRows=1&username=morampudiarun'.format(
                lat, lng)).read()
        if lat:
            return returning(response, lat), 200
        elif lng:
            return returning(response, lng), 200
        else:
            return returning(response, lat, lng), 200
    elif placename or city or countrycode or state:
        if placename:
            return function_for_places(placename)
        elif city:
            return function_for_places(city)
        elif state:
            return function_for_places(state)
        elif countrycode:
            return function_for_places(countrycode)
    else:
        return ({"Error":"Please pass proper Query parameters"}), 400

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True, port= port)
