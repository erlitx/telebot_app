import requests
from dotenv import load_dotenv
import os
import urllib3
import json
import telebot
from logger import logger



load_dotenv()
TOKEN = os.getenv('TOKEN')
TOKEN = '6679562934:AAHyo9Px8tgTfYq607SM7fwZhp7T0W002vU'


url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage'
headers = {'Content-Type': 'application/json'}
data = {'chat_id': -4046108417,
        'parse_mode': 'HTML',
        'text': '/start',
        'disable_web_page_preview': True,}

response = requests.post(url, json=data, headers=headers)
# Check the response status code
if response.status_code == 200:
    print('POST request was successful!')
    print('Response content:')
    print(response.text)
else:
    print(f'POST request failed with status code {response.status_code}')




# def get_groups():
#     bot = telebot.TeleBot(token=TOKEN)

#     # Get a list of updates from the bot
#     updates = bot.get_updates()
#     logger.info(f'Updates: {updates}')
#     # Iterate through updates to extract chat IDs
#     group_chat_ids = []

#     for update in updates:
#         chat = update.message.chat
#         chat_id = chat.id
#         chat_type = chat.type
        
#         # Check if the chat is a group or supergroup (exclude private chats)
#         if chat_type in ('group', 'supergroup'):
#             group_chat_ids.append(chat_id)

#     # Print the list of group chat IDs
#     print("List of group chat IDs:")
#     for chat_id in group_chat_ids:
#         print(chat_id)

# get_groups()




####### SEND MESSAGE VIA REQUEST #######
# url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage'
# headers = {'Content-Type': 'application/json'}
# data = {'chat_id': 6637156383,
#         'parse_mode': 'HTML',
#         'text': 'some text2',
#         'disable_web_page_preview': True,}

# response = requests.post(url, json=data, headers=headers)
# # Check the response status code
# if response.status_code == 200:
#     print('POST request was successful!')
#     print('Response content:')
#     print(response.text)
# else:
#     print(f'POST request failed with status code {response.status_code}')


######### SEND MESSAGE VIA URLLIB3 #########
# http = urllib3.PoolManager()
# response = http.request('POST', url, body=json.dumps(data).encode('UTF-8'), headers=headers)
# data_resp = json.loads(response.data)
# if data_resp.get('error_code') == 400:
#     print('Error 400')


