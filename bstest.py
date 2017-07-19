# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scape runs)
import time

# set the url as VentureBeat,
url = "https://twitter.com/Ben_Nicoll"
# set the headers like we are a browser,
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# download the homepage
response = requests.get(url, headers=headers)
# parse the downloaded homepage and grab all text, then,


# css_soup = BeautifulSoup('<p class="ProfileHeaderCard-bio u-dir" dir="ltr"></p>')
# css_soup.p['class']

soup = BeautifulSoup(response.text, "lxml")
parsed = soup.find_all("p", "ProfileHeaderCard-bio")

#if str(soup).find("Nicoll") == 1:
#soup.findAll("div", { "class" : "stylelistrow" })
# soup.findAll("p", { "class" : "<p class="ProfileHeaderCard-bio u-dir" dir="ltr">", "</p>" })

print parsed
