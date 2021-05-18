import sys
import praw #pip install praw
import time
import urllib
import random
from instabot import Bot #pip install InstagramApi
from dotenv import dotenv_values #pip install python-dotenv
import config
import shutil

env = dotenv_values(".env")

# =========== REDDIT API SETUP ===========
reddit = praw.Reddit(client_id=env.get('PRAW_CLIENT_ID'),
						client_secret=env.get('PRAW_CLIENT_SECRET'),
						user_agent=env.get('PRAW_USER_AGENT'))


# previous_memes 
previous_memes = []

# Remove previous config
try: shutil.rmtree('./config')
except: pass

# Read previous meme urls
with open(config.MEME_LOG, 'r') as filehandle:
	for line in filehandle:
		currentPlace = line[:-1]

		previous_memes.append(currentPlace)


def return_meme():
	# Returns meme which passws criterias
	global sub
	global previous_memes
	done = True
	while done:
		subb = reddit.subreddit(random.choice(config.source_subreddits)).random()
		if (not subb.stickied and all(y in subb.url for y in ['.jpg', 'redd']) and not subb.over_18 and subb.upvote_ratio >= config.MIN_UPVOTE_RATIO and subb.url not in previous_memes and 0.8 <= (subb.preview.get('images')[0].get('source').get('width') / subb.preview.get('images')[0].get('source').get('height')) <= 1.91):
			print("Image Passed, proceeding...")
			return subb
		else:
			print("Image criteria failed, trying new")

print("Started Script")
meme = return_meme()

# Writes new meme URL to file
print("Started Writing URL to file")
with open(config.MEME_LOG, 'a') as filehandle:
	filehandle.write('%s\n' % meme.url)
	print("Written URL to file")

# Downloads file from URL
print("Downloading file...")
urllib.request.urlretrieve(meme.url, "meme.jpg")
print("Downloaded File !")


# === INSTAGRAM BOT ===

# Login to insta
bot = Bot()
bot.login(username=env.get('INSTA_USERNAME'), password=env.get('INSTA_PASSWORD'))

# Uplaod file to instagram
bot.upload_photo('meme.jpg', caption=meme.title)
print('\nPOST SUBMITTED\n')

# Exit program
sys.exit()