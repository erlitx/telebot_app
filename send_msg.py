import requests
from dotenv import load_dotenv
import os
import urllib3
import json


load_dotenv()
TOKEN = os.getenv('TOKEN')

url = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage'
headers = {'Content-Type': 'application/json'}
data = {'chat_id': 6637156383,
        'parse_mode': 'HTML',
        'text': 'some text2',
        'disable_web_page_preview': True,}

response = requests.post(url, json=data, headers=headers)
# Check the response status code
if response.status_code == 200:
    print('POST request was successful!')
    print('Response content:')
    print(response.text)
else:
    print(f'POST request failed with status code {response.status_code}')



# http = urllib3.PoolManager()
# response = http.request('POST', url, body=json.dumps(data).encode('UTF-8'), headers=headers)
# data_resp = json.loads(response.data)
# if data_resp.get('error_code') == 400:
#     print('Error 400')
