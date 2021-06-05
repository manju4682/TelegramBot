# TelegramBot, the _informer
## About the project  
During these tough times, it's handy to find all the crucial information at one place. Telegram provides a feature to build our bots to   automate reading and sending messages through scripts. A bot is added to a telegram group. The bot reads for messages with specific commands and replies with the required   information. And there also a personal chat Bot which helps with vaccination details, like whether you can take the vaccine or not. It also helps with vaccine availability in your area.

## Implementation  
Telegram bot reads and sends messages by calling the APIs with relevant information like botId, chatId and the text message. The information for specific commands is scraped from several websites like BBMP website, Karnataka Government's   Covid website and then it parses the info and sends it to the group. The personal VaccineBot has several options to check if one can take the vaccine or not and to check for vaccine availability. To determine if one can take vaccine or not the bot asks the user to answer a simple questionnaire. And based on the replies the bot gives a relevant reply. For vaccine availability, bot makes use of CoWiN API to pull the details. 

## Tools used  
* Telegram API to interact with the group using bots.  
* WebScraping to pull the required information from several websites.  
* Twitter API to pull tweets.  
* Several other APIs to pull relevant data.  
* Python packages like json, re, Beautiful soup to handle parsed data and construct messages.  
* Python package, requests to call the APIs.  
 
 ## Conclusion and takeaways  
 There's a lot we can do with Telegram bots. They help us keep up with schedules with reminders, customized news delivery and lot more. And this was just a attempt to exploit that feature to ease the burden, by delivering crucial information about pandemic at one place. 
