import json
from datetime import datetime
import facebook
import requests
import pandas as pd
import re
import os

#do something to clean posts. return None if the post is not "good"
def cleanPost(post):
    return post

def parse_post_json(candidate):
    posts = []
    dates = []
    candidates = []
    
    for f in os.listdir("data/"+candidate):
        filePath = 'data/'+candidate+'/'+f
        data = json.loads(open(filePath,'r').read().decode())
        for post in data[data.keys()[1]]:
            try:
                p = cleanPost(post['message'])
                if p!=None:
                    print len(post['likes']['data'])
                    posts.append(p)
                    dates.append(datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))
                    candidates.append(candidate)
            except:
                continue
    return posts,dates,candidates



def get_all_posts(user,access_token):
    folder = 'data/'+user + '/'
    if not os.path.isdir(folder):
        os.mkdir(folder)
        
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(user)
    posts = graph.get_connections(profile['id'], 'posts')
    
    # Wrap this block in a while loop so we can keep paginating requests until
    # finished.
    i = 1
    while True:
        try:
            print i
            with open(folder+str(i)+'.json', 'w') as outfile:
                json.dump(posts, outfile)
            
            # Attempt to make a request to the next page of data, if it exists.
            posts = requests.get(posts['paging']['next']).json()
        except KeyError:
            # When there are no more pages (['paging']['next']), break from the
            # loop and end the script.
            break
        i+=1
    os.remove(folder+str(i)+'.json')
        



posts,dates,candidates = parse_post_json('yairlapid')
df = pd.DataFrame({'post':posts,'date':dates,'candidate':candidates})
print df.describe()