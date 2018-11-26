from flask import Flask, request, jsonify
from geopy import geocoders
import json
import urllib.request


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