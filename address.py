import urllib.request, urllib.parse, urllib.error
import json
import ssl
import csv
import pandas as pd

#If the billing is enabled and you have a working API, you can use that to access the googleapis
api_key = False


if api_key is False:
    api_key = 42
    serviceurl = 'http://py4e-data.dr-chuck.net/json?'
else :
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def Return_coordinates(address):
    
    if len(address) < 1: return
    try:
        df = pd.read_csv('address_details.csv',index_col = 0)
        print('This is pandas address-',df.loc[address][0],df.loc[address][1],df.loc[address][2])
        return [df.loc[address][0],df.loc[address][1],df.loc[address][2]]
 
    except:

        with open('address_details.csv','a',newline="") as file:
            writer = csv.writer(file)
            parms = dict()
            parms['address'] = address
            if api_key is not False: parms['key'] = api_key
            url = serviceurl + urllib.parse.urlencode(parms)

            uh = urllib.request.urlopen(url, context=ctx)
            data = uh.read().decode()

            try:
                js = json.loads(data)
            except:
                js = None

            if not js or 'status' not in js or js['status'] != 'OK':
                print("Data fetch unsuccessful")
                return 

            #print(json.dumps(js, indent=4))

            lat = js['results'][0]['geometry']['location']['lat']
            lng = js['results'][0]['geometry']['location']['lng']
            print('lat', lat, 'lng', lng)
            location = js['results'][0]['formatted_address']
            print(location)
            writer.writerow([address,location,lat,lng])
            return [location,lat,lng]
    
