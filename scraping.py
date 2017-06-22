# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 08:02:38 2017

@author: Rajasekhar Matam
"""

import requests
from bs4 import BeautifulSoup

url = "http://vivo.ufl.edu/people"
#url+page2 =url+ '&page = str(2) +'&relese'
#def get_data_from_url (url,10):
r= requests.get (url)
r.content
soup = BeautifulSoup(r.content,'lxml')
print soup.prettify
soup.find_all("a")
for link in soup.find_all("a"):
    print link

for link in soup.find_all("a"):
    print link.get("href")

for link in soup.find_all("a"):
    print link.text
for link in soup.find_all("a"):
    print link.text,link.get("href")

for link in soup.find_all("a"):
    if "http" in link.get(href):
        "<a href='%s'>%s</a>"%(link.get("href"),link.text)	
for link in soup.find_all("a"):
    "<a href='%s'>%s</a>"%(link.get("href"),link.text)	


g_data = soup.find_all("div",{"id":"wrapper-content"})
print g_data

for item in g_data:
    print item.section
    
g_data2 = soup.find_all("section",{"id":"browse-by"})
print g_data2
for ul in g_data2:
    print ul.contents[1].text

for ul in g_data2:
    print ul.text


print item.contents[1].text



for item in g_data:

print item.contents[0].find_all("a",{"class":"business-name"})[0].text

print item.contents[1].find_all("p",{"class":"adr"})[0].text//text

try:

print item.contents[1].find_all("span",{"itemprop":"adress"})[0].text//text

print item.contents[1].find_all("span",{"itemprop":"adressLocality"})[0].text//text

except:

pass

try:

print item.contents[1].find_all("li",{"class":"primary"})[0].text//text

except:

pass