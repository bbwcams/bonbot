import os,requests,json,time,random
from atproto import Client,models
P='posted.json';F='https://bngprm.com/promo.php?c=18144&type=api&api_v=1&limit=10&api_type=json'
c=Client();c.login(os.getenv('BLUESKY_HANDLE'),os.getenv('BLUESKY_PASSWORD'))
d=requests.get(F).json()
posted=json.load(open(P)) if os.path.exists(P) else {}
n=time.time();e=[p for p in d if p.get('chat_status')=='public' and (p['username'] not in posted or n-posted[p['username']]>86400)]
if not e:exit()
p=max(e,key=lambda x:x.get('members_count',0));u=p['username']
posted[u]=n;json.dump(posted,open(P,'w'))
t=p['display_name'];a=p['display_age'];m=p.get('members_count',0);u_url=p['chat_url'];img='https:'+p['profile_images']['thumbnail_image_medium'];topic=p.get('chat_topic','')[:80]
tags=' '.join(['#'+tag.replace(' ','').replace('-','')[:18] for tag in p.get('tags',[])[:4]])
text=f"🔥LIVE NOW! {t} ({a}yo) streaming HOT with {m}+ watching 💦\n{topic}\n👉 Join chat: {u_url}\n{tags} #nsfw #nsfwsky"
img_data=requests.get(img).content;blob=c.upload_blob(img_data).blob
embed=models.AppBskyEmbedImagesMain(images=[models.AppBskyEmbedImagesImage(alt=f"Live cam: {t}",image=blob)])
c.send_post(text=text,embed=embed)
