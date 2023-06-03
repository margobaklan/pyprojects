from datetime import datetime
from itertools import dropwhile, takewhile

import instaloader

L = instaloader.Instaloader()
L.download_pictures = False
PROFILE = "guweiz"
profile = instaloader.Profile.from_username(L.context, PROFILE)
posts = instaloader.Profile.from_username(L.context, "guweiz").get_posts()

SINCE = datetime(2023, 2, 6)
UNTIL = datetime(2023, 1, 1)

captions = []

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date < SINCE, posts)):
    print(post.date)
    L.download_post(post, "guweiz")
