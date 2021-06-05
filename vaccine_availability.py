from urllib.parse import urlencode
import urllib.request  #to handle the url requests
from bs4 import BeautifulSoup #to parse the html
import re #to clean parsed data
import json
import requests

def availability(bot_id,update_id,chat_id):
    print("In availability")
    query1 = "Please enter the correct Pincode:"
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,query1)
    requests.get(url)
    while True:
        fp = urllib.request.urlopen("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_id,str(update_id)))
        news = json.load(fp)    
        if news['result']:
            #parsing through all the messages and looking for specific commands
            for l in news['result']:
                update_id = l['update_id']
                update_id +=1
                pincode = l['message']['text']
            break  
    query2 = "Please enter the date for which you want to check the availability:\nFormat for date, DD-MM-YYYY"
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,query2)
    requests.get(url)
    while True:
        fp = urllib.request.urlopen("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_id,str(update_id)))
        news = json.load(fp)    
        if news['result']:
            #parsing through all the messages and looking for specific commands
            for l in news['result']:
                update_id = l['update_id']
                update_id +=1
                date = l['message']['text']
            break

    base_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}'.format(pincode,date)
    data = requests.get(base_url)
    data = data.json()
    count = 0
    #print(data)
    message = ""
    for centre in data['sessions']:
        if centre['available_capacity']>0:
            count +=1
            temp_message = str(count)+". \n"
            temp_message += "Centre name: "
            temp_message += centre['name']
            temp_message += "\nCentre address: "
            temp_message += centre['address']
            temp_message += "\nAvailable first dose: "
            temp_message += str(centre['available_capacity_dose1'])
            temp_message += "\nAvailable second dose: "
            temp_message += str(centre['available_capacity_dose2'])
            temp_message += "\n"
            message += temp_message
    
    if not message:
        message = "There are no vaccine centres with available vaccine doses for given Pincode and Date. You may try different Pincodes or Dates."
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,message)
    requests.get(url)
    return update_id        
