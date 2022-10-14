import os
import time
import tweepy
from authfld import keys
import pics
import cv2
import hashtagmaker as ht


def api():
    auth=tweepy.OAuthHandler(keys.api_key, keys.api_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    return tweepy.API(auth)

def tweetforme(api:tweepy.API, msg:str, img_path:str, picid:str):
    pic = api.media_upload(img_path)
    maintweet = api.update_status(msg, media_ids=[pic.media_id_string])
    time.sleep(2)
    api.update_status(f"https://digitalcollections.iu.edu/concern/images/{picid}", in_reply_to_status_id=maintweet.id)

def formatDesc(path:str):
    desc = []
    with open(f'{path}.meta', 'r') as file:
        ln = 0
        for line in file:
            if line[:-1] == "None":
                desc.append('')
            else:
                if ln in [1,2]:
                    desc.append(f"{line[:-1]}, ")
                else:
                    desc.append(line[:-1] )
            ln=ln+1
    if desc[1] == '' and desc[2]=='':
        desc[2]="Unknown"
    if desc[1] == desc[2]:
        desc[1] = ''
    return desc

def addHashtags(desc:str):
    tags=ht.craftHashtags(desc, keys.bearer_token)
    n=0
    while n<len(tags) and len(desc+tags[n][0])<280 and tags[n][1] >1000:
        wtag=tags[n][0]
        if f"#{wtag}" not in desc:
            desc=desc+f"#{wtag} "
        n=n+1

    desc=desc+'\n'
    
    while n<len(tags):
        desc=desc+f"{tags[n][0]}({tags[n][1]}) "
        n=n+1
    
    return desc



if __name__ == '__main__':
    api=api()
    picid, picurl = pics.randCushman()
    pic=cv2.imread(f'dl/{picid}.jp2')
    cv2.imwrite(f'dl/{picid}.jpeg', pic)

    desc = formatDesc(f"dl/{picid}")

    tweetbody= f"""{desc[4]}
{desc[0]}
{desc[1]}{desc[2]} {desc[3]}
{desc[5]}
"""
    print(tweetbody)
    tweetbody = addHashtags(tweetbody)
    tweetforme(api,tweetbody, f"dl/{picid}.jpeg", picurl)
    print(tweetbody)

    os.remove(f"dl/{picid}.jpeg")
    os.remove(f"dl/{picid}.jp2")
    os.remove(f"dl/{picid}.meta")


