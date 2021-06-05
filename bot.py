#Importing all the required libraries
import urllib.request  #to handle the url requests
from bs4 import BeautifulSoup #to parse the html
import re #to clean parsed data
import json
import time
from address import *
from twitter import *
import requests

#This function listens for incoming messages and checks every 5 sec
#for new messages
def Listen(bot_id,chat_id):
    print("Listening...")
    update_id = ""
    while True:
        #making the api request to get the messages
        #Bot id should be added
        fp = urllib.request.urlopen("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_id,str(update_id)))
        
        #handling the json data
        news = json.load(fp)
        options_flag = []
        try:
            #parsing through all the messages and looking for specific commands

            for l in news['result']:
                update_id = l['update_id']
                print(chat_id," ",l['message']['chat']['id'])
                if l['message']['chat']['id']==chat_id and l['message']['text']=="/bed_availability":
                    pass
                    #options_flag.append(1)
                elif l['message']['chat']['id']==chat_id and l['message']['text']=="/helpline":
                    options_flag.append(2)  
                elif l['message']['chat']['id']==chat_id and l['message']['text']=="/case_stats":
                    options_flag.append(3)
                elif l['message']['chat']['id']==chat_id and l['message']['text']=="/tweets_news":
                    options_flag.append(4)       
                print(l['message']['text'])
                update_id+=1

            if not options_flag:
                continue    
            Reply(options_flag,chat_id,bot_id)  
              
        except:
            continue          


#Reply function that replies based on commands
def Reply(options_flag,chat_id,bot_id):
    print("In reply")
    #for any number of messages with same command listened in due time we reply once
    if 1 in options_flag:

        #Accessing the BBMP website for bed availability data
        print("Opening BBMP url")
        fp = urllib.request.urlopen("http://bbmpgov.com/chbms/")
        mybytes = fp.read()
        
        mystr = mybytes.decode("utf8")
        soup = BeautifulSoup(mystr, "html.parser")
        soup.prettify()
        l1 = soup.find("section", {"id": "B"}).find_all("tr")
        message = "Bed availability at Government Hospitals\n"
        cnt = 1
        for n in l1[2:]:
            try:
                cells = n.find_all("td")
                if cells[16].get_text()=="0":
                    continue

                #Since the message has to sent along with url, it should follow certain conventions
                message +=str(cnt)+"."
                message += cells[1].get_text()
                details = Return_coordinates(cells[1].get_text())
                print(cells[1].get_text(),details)
                message += ", Beds available- "
                message += cells[16].get_text()
                message +="\n"
                message += "Address- "
                message += details[0]
                message +="\n"
                message += "Map Link- "
                link = 'https://www.google.com/maps/search/?api=1&query='+str(details[1])+","+str(+details[2])
                message += link
                message +="\n\n"               
                cnt+=1

            except Exception as e:
                print(e)
                continue    


        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,message)
        requests.get(url)

        l2 = soup.find("section", {"id": "A"}).find_all("tr")
        
        message2 = "Bed availability at Government Medical Collages\n"
        cnt = 1
        for n in l2[2:]:
            cells = n.find_all("td")
            #if cells[16].get_text()=="0":
                #continue
            message2 +=str(cnt)+"."
            message2 += cells[1].get_text()
            details = Return_coordinates(cells[1].get_text())
            message2 += ", Beds available- "
            message2 += cells[16].get_text()
            message2 +="\n"
            message2 += "Address- "
            message2 += details[0]
            message2 +="\n"
            message2 += "Map Link- "
            link = 'https://www.google.com/maps/search/?api=1&query='+str(details[1])+","+str(+details[2])
            message2 += link
            message2 +="\n\n"  
           
            cnt+=1 
        

        #We are sending two different messages for hospitals
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,message2)
        requests.get(url)
        print("Delivered reply for Bed availability")

    if 2 in options_flag:
        msg = "Visit this site\n"
        msg +="https://covid19.karnataka.gov.in/page/Helpline/en"
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,msg)
        requests.get(url)

    if 3 in options_flag:    
        stats = urllib.request.urlopen("https://covid19.karnataka.gov.in/english")
        stts = stats.read()
        myst = stts.decode("utf8")
        soup = BeautifulSoup(myst, "html.parser")
        l1 = soup.find('section')
        string = l1.text
        pattern = "\n" + '{2,}'
        string = re.sub(pattern, "\n", string)
        data = string.split("\n")

        #Constructing the paragraph for delivery
        paragraph = "Across Karnataka\n Confirmed- "+data[12]+"\nActive Cases- "+data[14]+"\nRecovered- "+data[16]+"\nDeceased- "+data[18]  

        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,paragraph)
        requests.get(url)
        #print(paragraph)
        print("Delivered reply for Case statistics")

    if 4 in options_flag:
        text_message = fetch_tweets()
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,text_message)
        requests.get(url)
        print("Delivered tweets")  

if __name__ == '__main__':
    
    bot_id = "XXXXXXXXXXXXXXXXXXXXXXXXX"
    chat_id = 'IIIIIIIIIII'
    Listen(bot_id,chat_id)
