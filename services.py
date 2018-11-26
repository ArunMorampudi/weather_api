from flask import Flask, request, jsonify, render_template
from geopy import geocoders
import json
import urllib.request
import os

def function_for_places(placename):
    response = urllib.request.urlopen(
        'http://api.geonames.org/findNearbyPostalCodesJSON?placename={}&maxRows=1&username=morampudiarun'.format(
            placename)).read()
    return returning(response), 200

def returning(response, lat=0, lng=0):
    res = json.loads(response.decode('utf8').replace("'", '"'))
    try:
        response2 = urllib.request.urlopen(
            'https://api.darksky.net/forecast/9cd31935eccea7bb67cb818d18cb4edc/{},{}?exclude=minutely,hourly,daily,alerts,flags'.format(
                res['postalCodes'][0]['lat'], res['postalCodes'][0]['lng'])).read()
        res2 = json.loads(response2.decode('utf8').replace("'", '"'))
        res2['postalCode'] = res['postalCodes'][0]['postalCode']
        res2['State'] = res['postalCodes'][0]['adminName1']
        res2['placeName'] = res['postalCodes'][0]['placeName']
        res2['countryCode'] = res['postalCodes'][0]['countryCode']
        return jsonify(res2)
    except:
        try:
            response2 = urllib.request.urlopen(
                'https://api.darksky.net/forecast/9cd31935eccea7bb67cb818d18cb4edc/{},{}?exclude=minutely,hourly,daily,alerts,flags'.format(
                    lat, lng)).read()
            res2 = json.loads(response2.decode('utf8').replace("'", '"'))
            res2['postalCode'] = '-'
            res2['State'] = '-'
            res2['placeName'] = '-'
            res2['countryCode'] = '-'
            return jsonify(res2)
        except:
            return ("Invalid input"), 400


def main_function():
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