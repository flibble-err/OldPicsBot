from cgitb import html
from dataclasses import replace
from fileinput import filename
from genericpath import isfile
import time
import bs4
import requests
import re
import shutil
import os.path




def getFromSoup(att:str, soup):
    try:
        u=soup.find('li', class_=att).text
        return u
    except AttributeError:
        return "None"

def dl_pic(id:str):

    htm=requests.get(f"https://digitalcollections.iu.edu/concern/images/{id}").text

    soup=bs4.BeautifulSoup(htm, 'html.parser')

    imageid=getFromSoup('attribute-source_metadata_identifier', soup)

    dllink=soup.find('td', class_='attribute-filename').find('a')['href']
    hmm=requests.get(f"https://digitalcollections.iu.edu{dllink}").text
    goulash=bs4.BeautifulSoup(hmm, 'html.parser')
    getdl=goulash.find('a', id='file_download')['href']
    response = requests.get(f"https://digitalcollections.iu.edu{getdl}", stream=True)

    #year=getFromSoup('attribute-date_created', soup)[0:3].replace('/','')

    os.makedirs('dl', exist_ok=True)

    with open(f"dl/{imageid}.jp2", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


    with open(f'dl/{imageid}.meta', 'a') as f:
        f.write(getFromSoup('attribute-date_created', soup)+"\n")
        f.write(getFromSoup('attribute-city', soup)+"\n")
        f.write(getFromSoup('attribute-us_state', soup)+"\n")
        f.write(getFromSoup('attribute-country', soup)+"\n")
        f.write(getFromSoup('attribute-title', soup)+"\n")
        f.write(getFromSoup('attribute-abstract', soup)+"\n")

    print(f"Downloaded {getFromSoup('attribute-title', soup)} ({getFromSoup('attribute-date_created', soup)})")
    return imageid
    

def dlAndFormat(page:int):
    regex=re.compile('/concern/images/.*\?locale=en')
    print(f"Starting list {page}")

    htmm= requests.get(f"https://digitalcollections.iu.edu/collections/2801pg36g?per_page=1000&page={page}").text
    print(f"Req success")

    soup=bs4.BeautifulSoup(htmm, 'html.parser')
    idlocal=[]


    reff=soup.find_all('a')

    for i in reff:
        if i.has_attr('href'):
                #print(i['href'])
                x = i['href']
                if re.match(regex,x):
                    idlocal.append(x.replace('/concern/images/','').replace('?locale=en','').replace('/edit#share',''))
    locid=list(dict.fromkeys(idlocal))
    print("Total: ",len(locid), " entries")
    return locid

def getPicList():

    


    ids=[]

    if os.path.isfile("images.list"):
        print("Found the images.list file, reusing")
        with open('images.list', 'r') as file:
            for line in file:
                ids.append(line[:-1])
    else:
        print('images.list not found, pulling new image db, this will take a while')
        for i in range(15):
            ids.extend(dlAndFormat(i+1))
        with open('images.list', 'a') as file:
            for id in ids:
                file.write(f"{id}\n")
     
    return ids




        
