import requests
import json
from bs4 import BeautifulSoup
from bs4.element import (
    NavigableString, Tag
)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
BASE_URL = "https://twitter.com/{handle}/"

# PRE:  Takes a BeautifulSoup "soup" object for HTML parsing.
# POST: The media count for this user has been found from the soup if it 
# exists and converted into an integer format. Otherwise, the media_count
# is vacously zero since it is not displayed in the soup.
def get_media_count(soup):

    media_count_anchor = soup.find("a", {'class': 'PhotoRail-headingWithCount'})
    media_count = 0
    if media_count_anchor:
        media_count_text = media_count_anchor.text.strip().split(" ")
        integer_found    = False
        index            = 0
        while not integer_found and index < len(media_count_text):
            item = media_count_text[index].replace(",", "")
            if item.isdigit():
                media_count   = int(item)
                integer_found = True
            else:
                index += 1
    return media_count

# PRE: Takes the twitter handle signifying the url routing to the page:
# https://twitter.com/handle/media/ so that we may parse the users media
# page for the url to this users first photo
# POST: The url has been found if they exist otherwise None is returned.
def get_latest_photo(handle):

    r                = requests.get(BASE_URL.format(handle=handle) + "media/")
    soup             = BeautifulSoup(r.text, "html.parser")
    media            = soup.find_all("div", {'class': 'AdaptiveMedia-container'})
    index            = 0
    found_img        = False
    latest_photo_url = None
    while not found_img and index < len(media):
        img = media[index].find("img")
        if img is not None and img.has_attr("src"):
            latest_photo_url = img['src']
            found_img = True
        else:
            index += 1
    return latest_photo_url

# PRE: Takes a BeautifulSoup object representing the "soup" of the twitter
# users home page.
# POST: Their home page has been parsed for their first non-pinned tweet,
# if it exists, otherwise None is returned signifying that there is no
# such tweet.
def get_latest_tweet(soup):

    tweets       = soup.find_all("div", {'class': "js-stream-tweet"})
    first_tweet  = None
    found        = False
    index        = 0
    while not found and index < len(tweets):
        tweet     = tweets[index]
        has_class = tweet.has_attr("class")
        if has_class and not "user-pinned" in tweet['class']:
            text_container = tweet.find("div", {'class': 'js-tweet-text-container'})
            if text_container is not None:
                first_tweet = ""
                p = text_container.p
                for i, item in enumerate(p):
                    if isinstance(item, NavigableString):
                        first_tweet += item.string
                    else:
                        first_tweet += item.text
                    if i != len(p) - 1:
                        first_tweet += " "
                found = True
        else:
            index += 1
    return first_tweet

def get_followers(handle):

    pass

# PRE: Takes a requests.get Response instance signifying the response
# of getting the HTML page for further parsing
# POST: The json dict twitter provides of the users "init-data" has
# been parsed for all relevant fields + manual parsing for the dob,
# media_count, latest_photo, and latest_photo_url and returned as
# dict with the key values matching the declared fields on the 
# the TwitterProfile model for fluid updating / comparison.
def get_twitter_user_data(response):

    soup         = BeautifulSoup(response.text, "html.parser")
    init_data    = soup.find("input", {'id': 'init-data'})
    json_data    = json.loads(init_data['value'])
    profile_data = json_data['profile_user']
    handle       = profile_data['screen_name']

    media_count  = get_media_count(soup)
    dob          = soup.find('span', {'class': "ProfileHeaderCard-birthdateText"})
    if dob:
        dob = dob.text.strip()
    latest_photo_url = get_latest_photo(handle)
    latest_tweet     = get_latest_tweet(soup)

    return {
        'avatar_url':       profile_data['profile_image_url'],
        'banner_url':       profile_data['profile_banner_url'] if 'profile_banner_url' in profile_data else None,
        'website':          profile_data['url'],
        'location':         profile_data['location'],
        'join_date':        profile_data['created_at'],
        'dob':              dob,
        'bio':              profile_data['description'],

        'latest_tweet':     latest_tweet,
        'media_count':      media_count,
        'latest_photo_url': latest_photo_url,

        'tweet_count':      profile_data['statuses_count'],
        'followers':        ,
        'followers_count':  profile_data['followers_count'],
        'following':        ,
        'following_count':  profile_data['friends_count'],
        'like_count':       profile_data['favourites_count'],
        # Number of public lists this user is a part of...
        'listed_count':     profile_data['listed_count'],
        'handle':           handle,
        'verified':         profile_data['verified'],
    }