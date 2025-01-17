#!usr/bin/env python3
from geocode import getGeocodeLocation
import json
import requests
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "42MQYMW3CN0CMSNL05N2PHEGMJTVXS2WPU3NYILSWZ33XJKW"
foursquare_client_secret = "VVPEZPL33T4GN15UCZ20YY1VMVVZKSAUTGF3H55VNBUJBBMD"


def findARestaurant(mealType, location):
    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    geoLoc = getGeocodeLocation(location)
    # 1.1 make a comma delimited list of the returned geo location list
    delimLoc = ','.join(str(loc) for loc in geoLoc)
    # print('[%s]' % delimLoc)

    # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    # HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = 'https://api.foursquare.com/v2/venues/explore'
    params = dict(
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        v='20180323',
        ll=delimLoc,
        intent='checkin',
        query=mealType  # ,
        # limit=2
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)['response']

    # keyList = []
    # get_keys(data, keyList)
    # print(keyList)
    # for key in keyList:
    #    print(key)

    if data['groups'][0]['items']:
        # 3. found places, grab the first restaurant
        venue = []
        venue = data['groups'][0]['items'][0]['venue']
        # print(venue)
        venue_id = venue['id']
        name = venue['name']
        addressStr = venue['location']['formattedAddress']
        # cannot join if unicode chars outside ASCII range are used
        #address = ', '.join(str(value).encode('utf-8') for value in addressStr)
        address = ""
        for a in addressStr:
            if address != "":
                address += ", "  # add comma separator
            address += a
        #sys.stdout.write('id=%s: name=%s   address=%s\n' % (str(venue_id), name, address))
    else:
        return 'no venues in %s for %s' % (location, mealType)

    # 4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    #    https://api.foursquare.com/v2/venues/<venue_id>/photos?client_id=<client_id>&client_secret=<client_secret>&v=20180823&{{VENUE_ID}}=49d97513f964a520395e1fe3&limit=10
    url = 'https://api.foursquare.com/v2/venues/' + venue_id + '/photos'
    params = dict(
        client_id=foursquare_client_id,
        client_secret=foursquare_client_secret,
        v='20180323',
        group='venue' # ,
        # limit=2
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)['response']
    #print(data['photos'])

    """keyList = []
    get_keys(data, keyList)
    for key in keyList:
        print(key)
    """

    # 5. Grab the first image
    photo_url = ""
    if data and data['photos']:
        if data['photos']['count'] > 0:
            size = '300x300'
            photo = data['photos']['items'][0]
            photo_url = photo['prefix'] + size + photo['suffix']
        else:
            photo_url = 'static/default.jpg'
    else:
        # 6. If no image is available, insert default a image url
        photo_url = 'static/default.jpg'
    #print(photo_url)

    # 7. Return a dictionary containing the restaurant name, address, and image url
    restaurantDict = {
        'name': name,
        'address': address,
        'image': photo_url
    }
    
    print(restaurantDict)
    return restaurantDict


def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)


if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney, Australia")
