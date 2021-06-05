from urllib.parse import urlencode
import urllib.request  #to handle the url requests
from bs4 import BeautifulSoup #to parse the html
import re #to clean parsed data
import json
import requests
import time
from vaccine_availability import *

def Listen(bot_id):
    print("Listening...")
    update_id = 0
    while True:
        #making the api request to get the messages
        #Bot id should be added
        print(update_id)
        
        fp = urllib.request.urlopen("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_id,str(update_id)))
        news = json.load(fp)
        
        try:
            #parsing through all the messages and looking for specific commands
            for l in news['result']:
                update_id = l['update_id']
                update_id+=1
                chat_id = l['message']['chat']['id']
                print(l['message']['text'])
                if l['message']['text']=="/start":
                    update_id = Reply(bot_id,chat_id,update_id)   

        except:
            continue            

def Reply(bot_id,chat_id,update_id):
    print("In Reply")
    still_in = True
    while still_in:
        key = {"keyboard":[[{"text":"Can I take the vaccine?"}],[{"text":"Check vaccine availability"}],[{"text":"End Chat"}]],"one_time_keyboard":True}
        key = json.dumps(key)
        message = "Welcome..\nMake your choice"
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}".format(bot_id,chat_id,message,key)
        requests.get(url1)
        while True:
            fp = urllib.request.urlopen("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_id,str(update_id)))
            news = json.load(fp)
            if news['result']:
                for l in news['result']:
                    update_id = l['update_id']
                    update_id +=1
                    chat = l['message']['chat']['id']
                    if chat == chat_id and l['message']['text']=="Can I take the vaccine?":
                        update_id = Questionnaire(bot_id,chat_id,update_id)
                    elif chat == chat_id and l['message']['text']=="Check vaccine availability":
                        update_id = availability(bot_id,update_id,chat_id)
                    else:
                        still_in = False    
                break        
            else:
                continue    
    print("Leaving Reply")         
    return update_id          

def Questionnaire(bot_id,chat_id,update_id):
    print("In questionnaire")
    key = {"keyboard":[[{"text":"YES"}],[{"text":"NO"}]],"one_time_keyboard":True}
    key = json.dumps(key)
    questions = ['Well, please answer this questionnaire to know!!\n\n1. Are you below 18?','2. Are you awaiting pregnancy results or pregnant or breastfeeding?','3. Have you had an allergic reaction to the previous dose of CoViD vaccine or experienced allergic reactions to any ingredients in the vaccine?',
    '4. Have you ever experienced an immediate or a delayed-onset anaphylaxis or allergic reaction to any of the following?\n>vaccines\n>injectable therapies\n>pharmaceutical products\n>food items','5. Have you recently recovered from CoViD-19?',
    '6. Have you been administered monoclonal antibodies or convalescent plasma treatment as part of CoViD-19 treatment?','7. Do you have any active symptoms of CoViD-19?',
    '8. Are you suffering from any other acute illnesses?','9. Do you have thrombocytopenia(abnormally low platelets count)?','10. Do you have any autoimmune diseases or are you on any immuno-suppressant drugs?']
    answers = ['Since you are below 18, you are not advised to take the CoViD vaccine currently. Trials are starting for people below 18. And once the vaccine is approved for people below 18, you can take the vaccine.',
    'Women who are expecting pregnancy or are pregnant or breastfeeding are not advised to take the vaccine.',
    'You are not advised to take the vaccine since you may experience severe allergic reactions.',
    'You may have to wait for at least 4 to 8 weeks before you can take the vaccine after recovering from CoViD.',
    'Please get tested for CoViD-19. It is advisable to take the vaccine with active CoViD-19 symptoms.',
    'It is not advisable to take the vaccine if you are not well. Please wait till you feel completely healthy.',
    'The trials did not include enough people with auto-immune diseases or thrombocytopenia. Therefore it is advisable to consult your doctor before taking the vaccine.',
    'Well, you are good to go ahead with vaccine administration. Book your appointment at the CoWin platform. Check vaccine availability by selecting the relevant option.']

    responses = []
    count = 0
    for question in questions:
        count += 1
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}".format(bot_id,chat_id,question,key)
        requests.get(url1)
        time.sleep(3)
        while True:
            fp = urllib.request.urlopen("https://api.telegram.org/bot{}/getUpdates?offset={}".format(bot_id,str(update_id)))
            news = json.load(fp)    
            if news['result']:
                #parsing through all the messages and looking for specific commands
                for l in news['result']:
                    update_id = l['update_id']
                    update_id +=1
                    responses.append(l['message']['text'])
                    if chat_id == l['message']['chat']['id'] and l['message']['text']=='YES' and count==1:
                        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[0])
                        requests.get(url1)
                        return update_id   
                    elif chat_id == l['message']['chat']['id'] and l['message']['text']=='YES' and count==2:
                        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[1])
                        requests.get(url1)   
                        return update_id

                break
            else:
                continue
    if responses[2]=='YES' or responses[3]=='YES':
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[2])
        requests.get(url1)
    elif responses[4]=='YES' or responses[5]=='YES':
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[3])
        requests.get(url1)    
    elif responses[6]=="YES":
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[4])
        requests.get(url1)
    elif responses[7]=="YES":
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[5])
        requests.get(url1)    
    elif responses[8]=="YES" or responses[9]=="YES":
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[6])
        requests.get(url1)
    else:
        url1 = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(bot_id,chat_id,answers[7])
        requests.get(url1)   
    return update_id   
                     
                   
if __name__ == '__main__':   
    bot_id = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    Listen(bot_id)    