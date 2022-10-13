from pydoc import cli
import sys
import tweepy
from dateutil.parser import parse
import hashtagmaker.tools as tools
import re
import hashtagmaker.english as eng

def craftHashtags(input:str , twitter_bearer_token:str):
    output = []
    input = input.splitlines()
    for n in range(len(input)):
        input[n] = re.sub(r'\W+', ' ', input[n])
    print(len(input))


    for line in input: #TODO Testing Dates
        try: 
            output.append((str(parse(line, fuzzy=False).year),99999999))
            input.remove(line)     
        except ValueError:
            pass
    
    
    input=[line.split() for line in input]

    for i in input:
        print(i)

    client=tweepy.Client(twitter_bearer_token)

    for line in input:
        for word in line:
            if word.lower().strip() in eng.prepositions + eng.determiners + eng.conjunctions+eng.trashed or len(word) <= 2:
                continue
            output.append(tools.getTagPopularity(word.lower().capitalize(), client))
        
        if len(line) >= 2:
            for n in range(1,len(line)):
                word=line[n-1].lower().capitalize()+line[n].lower().capitalize()
                if word.lower().strip() in eng.trashed:
                    continue
                output.append(tools.getTagPopularity(word, client))
        
        if len(line) >=3:
            for n in range(1,len(line)-1):
                word=line[n-1].lower().capitalize()+line[n].lower().capitalize()+line[n+1].lower().capitalize()
                if word.lower().strip() in eng.trashed:
                    continue
                output.append(tools.getTagPopularity(word, client))            

    output.sort(key=lambda x:x[1], reverse=True)
    output=list(dict.fromkeys(output))
    output = [i for i in output if i[1]>1000]

    for i in output:
        print(i)

    return output
    


        
