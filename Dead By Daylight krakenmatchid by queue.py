import os
import sys
import time
import psutil
import random
import pyperclip
import requests
import urllib
import json

#requests module debug == OFF
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#Clear func settup
clear = lambda: os.system('cls')

#Default values
os.system('title Shard Test')
matchfound=0
cookieautorized=0


#settings.txt
try:
    with open('settings.txt', 'r', encoding='utf-8') as stg:
        tln2=stg.readlines()
        activeuseragent=tln2[2]
        activeuseragent=activeuseragent.strip()
        activecatalog=tln2[4]
        activecatalog=activecatalog.strip()
    stg.close()
except:
    print(f'[CRITICAL ERROR]: {sys.exc_info()[1]}')
    print('[CRITICAL ERROR]: Something went wrong with settings.txt file!')
    print('Working with default settings...')
    activeuseragent = 'DeadByDaylight/++DeadByDaylight+Live-CL-377698 Windows/10.0.19042.1.768.64bit'
    activecatalog = '4.4.0_380690live'
    time.sleep(2)


#bhvrSessionCheck
def VerifybhvrSession():
  global bhvrsessionid
  global cookieautorized
  bhvrsessionid = input("\n\033[33mbhvrsession=\033[96m") # bhvrSession first try
  checkbhvrsession = requests.get('https://steam.live.bhvrdbd.com/api/v1/wallet/currencies', cookies={'bhvrSession': bhvrsessionid},headers={'Host': 'steam.live.bhvrdbd.com','User-Agent': ''+activeuseragent+'','Content-Type': 'application/json; charset=utf-8','x-kraken-client-platform': 'steam'},proxies=(urllib.request.getproxies()),verify=False)
  bhvrstatus = checkbhvrsession.status_code
  if bhvrstatus > 200 or bhvrstatus < 200:
     while cookieautorized < 1:
         if bhvrstatus == 401:
              print("\033[0m\033[91m[ERROR] Unauthorized - Already Connected\033[0m")

         print("\033[0m\033[91m[ERROR] Invalid Cookie\033[0m")
         bhvrsessionid = input("\n\n\033[33mbhvrsession=\033[96m") # bhvrSession loop
         checkbhvrsession = requests.get('https://steam.live.bhvrdbd.com/api/v1/wallet/currencies', cookies={'bhvrSession': bhvrsessionid},headers={'Host': 'steam.live.bhvrdbd.com','User-Agent': ''+activeuseragent+'','Content-Type': 'application/json; charset=utf-8','x-kraken-client-platform': 'steam'},proxies=(urllib.request.getproxies()),verify=False)
         bhvrstatus = checkbhvrsession.status_code
         if bhvrstatus == 200:
             cookieautorized = 1
         else:
             cookieautorized = 0


#Queue
def Proceedqueue():
    QueueEnter = requests.post('https://steam.live.bhvrdbd.com/api/v1/queue', cookies={'bhvrSession': bhvrsessionid},headers={'Host': 'steam.live.bhvrdbd.com','User-Agent': ''+activeuseragent+'','Content-Type': 'application/json; charset=utf-8','x-kraken-client-platform': 'steam'},data='{"additionalUserIds":[],"category":"live-397052-live","checkOnly":false,"countA":1,"countB":4,"latencies":[{"latency":323,"regionName":"ap-south-1"},{"latency":73,"regionName":"eu-west-1"},{"latency":374,"regionName":"ap-southeast-1"},{"latency":398,"regionName":"ap-southeast-2"},{"latency":48,"regionName":"eu-central-1"},{"latency":293,"regionName":"ap-northeast-2"},{"latency":271,"regionName":"ap-northeast-1"},{"latency":132,"regionName":"us-east-1"},{"latency":238,"regionName":"sa-east-1"},{"latency":221,"regionName":"us-west-2"}],"platform":"Windows","props":{"CrossplayOptOut":"false","characterName":"Claudette"},"rank":20,"region":"all","side":"B"}',proxies=(urllib.request.getproxies()),verify=False)
    JS = json.loads(QueueEnter.content)
    STATUS=JS["status"]
    if STATUS == "QUEUED":
        print(f'\033[0m\n\nQueue status is:\033[96m {STATUS} \033[0m')
        Whilequeue()
    else:
        print(f'Something went wrong, Queue status: {STATUS}')


#Queue Check
def Whilequeue():
    global matchfound
    while matchfound == 0:
     time.sleep(10) #Queue check cooldown
     QueueProcessing = requests.post('https://steam.live.bhvrdbd.com/api/v1/queue', cookies={'bhvrSession': bhvrsessionid},headers={'Host': 'steam.live.bhvrdbd.com','User-Agent': ''+activeuseragent+'','Content-Type': 'application/json; charset=utf-8','x-kraken-client-platform': 'steam'},data='{"additionalUserIds":[],"category":"live-397052-live","checkOnly":true,"countA":1,"countB":4,"latencies":[{"latency":323,"regionName":"ap-south-1"},{"latency":73,"regionName":"eu-west-1"},{"latency":374,"regionName":"ap-southeast-1"},{"latency":398,"regionName":"ap-southeast-2"},{"latency":48,"regionName":"eu-central-1"},{"latency":293,"regionName":"ap-northeast-2"},{"latency":271,"regionName":"ap-northeast-1"},{"latency":132,"regionName":"us-east-1"},{"latency":238,"regionName":"sa-east-1"},{"latency":221,"regionName":"us-west-2"}],"platform":"Windows","props":{"CrossplayOptOut":"false","characterName":"Claudette"},"rank":20,"region":"all","side":"B"}',proxies=(urllib.request.getproxies()),verify=False)
     JS = json.loads(QueueProcessing.content)
     try:
         STATUS=JS["status"]
         print(f'Queue status is:\033[96m {STATUS} \033[0m')
         if STATUS == "MATCHED":
             matchfound=1
         else:
             matchfound=0
     except:
         print("sad wolf")
    MatchID = JS["matchData"]["matchId"]
    print(f'\n\n\033[33mMatch succesfully found!\033[96m {MatchID}')
    print('\033[33m[CLIPBOARD] \033[96mkrakenmatchid copied to clipboard!\033[0m')
    pyperclip.copy(MatchID)



VerifybhvrSession()
Proceedqueue()
input("Press ENTER to close")