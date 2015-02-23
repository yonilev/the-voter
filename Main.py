import json
from datetime import datetime
import pandas as pd
import re
import os

#do something to clean posts. return None if the post is not "good"
def cleanPost(post):
    if len(post)<80:
        return None
    return post

def parsePostsJson(candidate):
    posts = []
    dates = []
    candidates = []
    
    for f in os.listdir("data/"+candidate):
        filePath = 'data/'+candidate+'/'+f
        data = json.loads(open(filePath,'r').read().encode('utf-8'))
        for post in data['posts']['data']:
            try:
                p = cleanPost(post['message'])
                if p!=None:
                    posts.append(p)
                    dates.append(datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))
                    candidates.append(candidate)
#                     x = datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
#                     epoch = datetime.utcfromtimestamp(0)
#                     delta = x - epoch
#                     delta.total_seconds()
            except:
                continue
    return posts,dates,candidates


posts,dates,candidates = parsePostsJson('galon')
df = pd.DataFrame({'post':posts,'postedDate':dates,'candidate':candidates})



