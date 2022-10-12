from pics import cushman
import random

def randCushman():
    
    id = random.sample(cushman.getPicList(), 1)[0]
    print(id)

    return [cushman.dl_pic(id), id]

