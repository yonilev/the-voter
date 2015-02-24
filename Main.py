import json
from datetime import datetime
import facebook
import requests
import os
import pandas as pd

#do something to clean posts. return None if the post is not "good"

def parse_post_json(candidate):
    posts = []
    dates = []
    candidates = []
    
    for f in os.listdir("data/"+candidate):
        filePath = 'data/'+candidate+'/'+f
        data = json.loads(open(filePath,'r').read().decode())
        for post in data[data.keys()[1]]:
            try:
                p = post['message']
                posts.append(p)
                dates.append(datetime.strptime(post['created_time'],'%Y-%m-%dT%H:%M:%S+0000'))
                candidates.append(candidate)
            except:
                continue
    return posts,dates,candidates

def clean_df(df,minNumberOfWords=6,minNumberOfChars=30):
    #remove duplicate posts from the same candidate
    df = df.drop_duplicates(subset=['post','candidate'])
    
    #remove posts with less words than minNumberOfWords or less characters than minNumberOfChars
    df = df[df.post.apply(lambda x: x.count(' ')>minNumberOfWords and len(x)>minNumberOfChars)]
    
    #start posts from the same date
    minDate = max([df[df.candidate==name].date.min() for name in df.candidate.unique()])
    df = df[df.date>=minDate]
    return df

def create_posts_df():
    candidates = os.listdir("data")
    post = []
    date = []
    candidate = []
    
    for c in candidates:
        data = parse_post_json(c)
        post += data[0]
        date += data[1]
        candidate += data[2]
    
    df = pd.DataFrame({'post':post,'date':date,'candidate':candidate})
    return clean_df(df)

    



def get_all_posts(fbUser,folderName,access_token):
    folder = 'data/'+folderName + '/'
    if not os.path.isdir(folder):
        os.mkdir(folder)
        
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(fbUser)
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
        


