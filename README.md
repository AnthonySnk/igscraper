
<p align="center">
  <img width="200" src="https://i.imgur.com/zwBVOeQ.png">
</p>

# IGScraper
**IGScraper** is an Instagram scraper developed in Python 3.8, use this scraper to get information (in `JSON` format) useful for account analysis:

- Global number of likes
- Global number of comments
- Number of followers
- Number of following
- Profile photo in original size
- All posts 
  + Post URL
  + Text of the publication
  + Location (name and coordinates)
  + Date

- And more

## Install

You can install this tool using `pip`
```
pip3 install git+https://github.com/jxlil/igscraper#egg=igscraper --upgrade
```

## Use
Below is a small example of the use of the tool

```
#!/usr/bin/env python3.8

from igscraper.scraper import IGScraper
import json


scraper = IGScraper("my_username", "my_password")

username = "example"
username_info = scraper.username_info(username)

with open(f"{username}.json", "+w") as f:
    f.write(json.dumps(username_info, indent=2))
```

Output:

```
{
  "username": "example",
  "name": "John Doe",
  "followers": 1364,
  "following": 607,
  "media_count": 10,
  "biography": "This is my biography",
  "hd_profile_pic": "https://example.com/original.jpg",
  "website": "https://example.com/",
  "likes_count": 784,
  "comment_count": 16,
  "engagement_rate": 59,
  "frequency_posts": "32 days",
  "phone_numbers": [],
  "emails": [],
  "is_bussines": "None",
  "is_verified": "None",
  "is_private": "False",
  "posts": {
    "1": {
      "date": "2021-01-28 14:15:23",
      "url": "https://instagram.com/p/XXXXXXXXXX-XXXXXXXXXXXX_XXXXXXX_XXXXXX/",
      "comment_count": 0,
      "like_count": 45,
      "text": "my post"
    },

```
