################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define RadHR Twitter Models.                                        ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
## Required For Elastic Beanstalk.                                            ##
import sys,os
os.environ['DJANGO_SETTINGS_MODULE'] = 'radhr.settings'
from datetime import datetime

## General Requirements.                                                      ##
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db import models

################################################################################
## Import Third Party Models.                                                 ##
################################################################################
import requests, json
from bs4 import BeautifulSoup

################################################################################
## Import Defined Models.                                                     ##
################################################################################
from lists.models import Watchlist, TwitterProfile, SocialProfile

################################################################################
## Import Twitter Utilities                                                  ##
################################################################################
from lists.twitter_utilities import (
    HEADERS, 
    BASE_URL,
    get_twitter_user_data,
)

################################################################################
## Define the Command Function.                                               ##
################################################################################
class Command(BaseCommand):

    args = ''
    help = 'Grabs things we need from Twitter Bio and stores them in the DB'

    #################################################################
    ## Parse the Twitter User.                                                ##
    ############################################################################
    # CAN UPDATE THIS TO USER TWEEPY OR TWILIO NOTE THAT THERE IS A RATE LIMIT
    # WHICH RESETS EVERY 15 MINUTES (SPECIFIC TO EACH API KEY)
    # WILL BE SLIGHTLY, BUT ONLY VERY SLIGHTLY, FASTER.
    def parse_twitter_user(self, twitter_user):

        response = requests.get(BASE_URL.format(handle=twitter_user.handle), headers=HEADERS)
        # If the twitter user is still valid and we can parse their biography for
        # potential side effects...
        if response.status_code != 404:
            twitter_user.compare_instance_data()
        else:
            # POSSIBLY SEND NOTIFICATION TO USER OR SOMETHING ELSE???
            print("Error! Twitter returned a 404 status code for twitter user: %s" % twitter_user,
                  "\nPlease verify that this user has not deleted their account.")

    ############################################################################
    ## Define the Handle Function.                                            ##
    ############################################################################
    def handle(self, *args, **options):

        # All twitter_users which have been added to any watchlist stored in
        # the database. This prevents unnecessary iterations / database hits
        # We can just grab the users which have this twitter user added to their
        # watchlist from the watchlist_set foreign key relations
        twitter_users = TwitterProfile.objects.all()
        for twitter_user in twitter_users:
            self.parse_twitter_user(twitter_user)