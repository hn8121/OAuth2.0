#!usr/bin/env python3

# Note: to run in the terminal, call python <cr>
#       then 'from geocode import getGeocodeLocation'
import httplib2
import json

def getGeocodeLocation(inLocation):
    #Use Google Maps API to convert a location into Lat/Long coordinates. 
    #Use the cooridnates to get a restaurant from foursquare

    #Format: https://maps.googleapis.com/maps/api/geocode/json?key=XXXXXXXXXXXXXXXXXXX&address=Tokyo,+Japan

    google_api_key  = "AIzaSyA1lZQpUjAhZhS6cWiam_iOoVzdpIVExmo" 
    addrStr = inLocation.replace(" ","+")
    uri = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (addrStr, google_api_key)

    #sent http request and get the HTTP response and result content
    h = httplib2.Http()
    response, content = h.request(uri, "GET")

    result = json.loads(content)
    print('response header: %s\n\n' % response)
    print('return: %s' % result)
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)
    #return result

if __name__ == "__main__":
    getGeocodeLocation('Allentown, PA')

