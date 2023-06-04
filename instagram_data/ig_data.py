from datetime import datetime
from itertools import dropwhile, takewhile
import instaloader
import pandas as pd
import re

L = instaloader.Instaloader()
L.download_pictures = False
PROFILE = "guweiz"
profile = instaloader.Profile.from_username(L.context, PROFILE)
posts = instaloader.Profile.from_username(L.context, "guweiz").get_posts()

SINCE = datetime(2023, 2, 6)
UNTIL = datetime(2023, 1, 1)
captions = []
dates = []
emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
                           "]+", flags=re.UNICODE)

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date < SINCE, posts)):
    # print(post.date)
    # captions.append(post.caption)
    captions.append(emoji_pattern.sub(r'', post.caption))
    dates.append(post.date)
    L.download_post(post, "guweiz")

df = pd.DataFrame()
df['Date'] = dates
df['Caption'] = captions
df.to_csv("ig_posts.csv")
print(df)
