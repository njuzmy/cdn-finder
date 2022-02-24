#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time


# # whatsmycdn
def whatscdn(domain):
    print(domain)
    current_page = "https://www.whatsmycdn.com/?uri=%s&location=GL" % domain
    page = requests.get(current_page)
    soup = BeautifulSoup(page.text)
    items = soup.find_all(attrs={'class':'six columns', "style":"margin-left: 2px; word-wrap:break-word;"})
    for item in items:
        if "edgecast" in item.get_text().lower():   #change edgecast to other cdn company
            return 'e'
        elif item.get_text().lower() == 'incapsula':
            return 'i'
    return 'n'

def isCDN(cdn_name, domain):
    print(domain)
    url = 'https://www.whatsmycdn.com/?uri=' + domain + '&location=GL'
    try:
        r = session.get(url)
        x = r.html.text
        if x.find('Error 1015') != -1:
            print(x)
            return False
        if x.find(cdn_name) != -1:
            print('yes')
            return True
    except Exception as e:
        print(e)
        return False

domain_df = pd.read_csv("../anycast/pingpoints/top-1m.csv")
for i in range(0, 100000):
    res1 = whatscdn("www."+ domain_df["domain"][i])
    if res1 == 'e':
        with open('e1.txt', mode='a') as filename:
            filename.write("www."+ domain_df["domain"][i])
            filename.write('\n')
        print('e')
    elif res1 == 'i':
        with open('i1.txt', mode='a') as filename:
            filename.write("www."+ domain_df["domain"][i])
            filename.write('\n')
        print('i')

# another function to use whatsmycdn api
session = HTMLSession()
domain_df = pandas.read_csv('../anycast/pingpoints/top-1m.csv"')
for i in range(10000, 20000):
    if isCDN('EdgeCast', domain_df["domain"][i]) == True:
        with open('.edgecastCDN.txt', 'a') as f:
            f.write(domain_df["domain"][i] + '\n')
    elif isCDN('EdgeCast', 'www.' + domain_df["domain"][i]) == True:
        with open('.edgecastCDN.txt', 'a') as f:
            f.write('www.' +domain_df["domain"][i] + '\n')
    elif isCDN('Incapsula', domain_df["domain"][i]) == True:
        with open('.incapsulaCDN.txt', 'a') as f:
            f.write(domain_df["domain"][i] + '\n')
    elif isCDN('Incapsula', 'www.' + domain_df["domain"][i]) == True:
        with open('.incapsulaCDN.txt', 'a') as f:
            f.write('www.'+domain_df["domain"][i] + '\n')


# # CDN finder
def initiate(domain):
    url = "https://api.cdnplanet.com/tools/cdnfinder?lookup=website"
    Headers = {"content-type": "application/json","Cdnplanet-Key":"4844a1b8-8d7a-4eb3-b533-8e47078aad76"}
    data = {"query": "https://" + domain}
    response = requests.post(url=url,headers=Headers,json=data)
    return json.loads(response.text)['id']

def lookup(findid):
    url = "https://api.cdnplanet.com/tools/results?service=cdnfinder&id=" + findid
    time.sleep(2)
    response2 = requests.get(url=url)
    try:
        return(json.loads(response2.text)['results'])
    except KeyError:
        time.sleep(5)
        response2 = requests.get(url=url)
        if 'results' in json.loads(response2.text).keys():
            return json.loads(response2.text)['results']
        else:
            return None

def whatcdn(results):
    for dic in results:
        if dic['cdn'].lower() =='edgecast':
            return 'e'
        elif dic['cdn'].lower() =='incapsula':
            return 'i'
    return 'n'

domain_df = pd.read_csv('../anycast/pingpoints/top-1m.csv')
for i in range(0,20000):
    print(domain_df["domain"][i])
    results = lookup(initiate("www."+ domain_df["domain"][i]))
    if results != None:
        flag = whatcdn(results)
        if flag == 'e':
            with open('finder_e.txt', mode='a') as filename:
                filename.write("www."+ domain_df["domain"][i])
                filename.write('\n')
            print('e')
        elif flag == 'i':
            with open('finder_i.txt', mode='a') as filename:
                filename.write("www."+ domain_df["domain"][i])
                filename.write('\n')
            print('i')
