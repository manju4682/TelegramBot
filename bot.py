#Importing all the required libraries
import urllib.request  #to handle the url requests
from bs4 import BeautifulSoup #to parse the html
import re #to clean parsed data
import json
import time
from address import *
from twitter import *

#This function listens for incoming messages and checks every 5 sec
#for new messages
def Listen(url):
    print("Listening...")
    update_id = ""
    while True:
        #making the api request to get the messages
        #Bot id should be added
        fp = urllib.request.urlopen("https://api.telegram.org/bot[BOT_API_KEY]/getUpdates?offset="+str(update_id))
        
        #handling the json data
        news = json.load(fp)
        options_flag = []
        try:
            #parsing through all the messages and looking for specific commands

            for l in news['result']:
                update_id = l['update_id']
                if l['message']['chat']['id']==['Chat_Id'] and l['message']['text']=="#bedavailability":
                    options_flag.append(1)
                elif l['message']['chat']['id']==['Chat_Id'] and l['message']['text']=="#helpline":
                    options_flag.append(2)  
                elif l['message']['chat']['id']==['Chat_Id'] and l['message']['text']=="#casestats":
                    options_flag.append(3)
                elif l['message']['chat']['id']==['Chat_Id'] and l['message']['text']=="#twitternews":
                    options_flag.append(4)       
                print(l['message']['text'])
                update_id+=1

            if not options_flag:
                continue    
            Reply(options_flag,url)  
              
        except:
            update_id+=1
            continue  
    #sleep for 5 seconds, It's a wait     
    time.sleep(5)         


#Reply function that replies based on commands
def Reply(options_flag,url):

    #for any number of messages with same command listened in due time we reply once
    if 1 in options_flag:

        #Accessing the BBMP website for bed availability data
        fp = urllib.request.urlopen("http://bbmpgov.com/chbms/")
        mybytes = fp.read()
        
        mystr = mybytes.decode("utf8")
        soup = BeautifulSoup(mystr, "html.parser")
        soup.prettify()
        l1 = soup.find("section", {"id": "B"}).find_all("tr")
        message = "Bed availability at Government Hospitals%0D%0A"
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
                message +="%0D%0A"
                message += "Address- "
                message += details[0]
                message +="%0D%0A"
                message += "Map Link- "
                link = 'https://www.google.com/maps/search/?api=1&query='+str(details[1])+","+str(+details[2])
                message += link
                message +="%0D%0A%0D%0A"               
                cnt+=1

            except Exception as e:
                print(e)
                continue    


        message = message.replace("&","%26")
        message = message.replace(" ","+")
        message = message.replace("#","")

        print(len(message))
        #The message gets delivered when this url is called
        print(url+message)
        urllib.request.urlopen(url+message)

        l2 = soup.find("section", {"id": "A"}).find_all("tr")
        
        message2 = "Bed availability at Government Medical Collages%0D%0A"
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
            message2 +="%0D%0A"
            message2 += "Address- "
            message2 += details[0]
            message2 +="%0D%0A"
            message2 += "Map Link- "
            link = 'https://www.google.com/maps/search/?api=1&query='+str(details[1])+","+str(+details[2])
            message2 += link
            message2 +="%0D%0A%0D%0A"  
           
            cnt+=1 
        
        message2 = message2.replace("&","%26")
        message2 = message2.replace(" ","+")
        message2 = message2.replace("#","")

        #We are sending two different messages for hospitals
        urllib.request.urlopen(url+message2)
        print("Delivered reply for Bed availability")

    if 2 in options_flag:
        msg = "Visit this site%0D%0A"
        msg +="https://covid19.karnataka.gov.in/page/Helpline/en"
        msg = msg.replace(" ","+")
        urllib.request.urlopen(url+msg)
        print("Delivered reply for helpline")

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
        paragraph = "Across+Karnataka%0D%0A%0D%0AConfirmed-+"+data[12]+"%0D%0AActive+Cases-+"+data[14]+"%0D%0ARecovered-+"+data[16]+"%0D%0ADeceased-+"+data[18]  


        urllib.request.urlopen(url+paragraph)
        print("Delivered reply for Case statistics")

    if 4 in options_flag:
        text_message = fetch_tweets()
        urllib.request.urlopen(url+text_message)
        print("Delivered tweets")  

if __name__ == '__main__':

    #This is the url for replying
    url = "https://api.telegram.org/bot['BOT_API_KEY']/sendMessage?chat_id=['Chat_Id']&text="
    Listen(url)
