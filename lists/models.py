################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlist Models.                                            ##
################################################################################

################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.conf import settings
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone

################################################################################
## Import Third Party Modules.                                                 ##
################################################################################
from simple_history.models import HistoricalRecords

################################################################################
## Import Core Modules.                                                 ##
################################################################################
import uuid
import requests
import os

################################################################################
## Import Defined Models.                                                     ##
################################################################################

################################################################################
## Import Utilities                                                           ##
################################################################################
from .twitter_utilities import (
    HEADERS, BASE_URL,
    get_twitter_user_data,
)
from base_utilities import (
    OverwriteStorage,
    set_image_from_url,
)

IMAGE_EXTENSION = ".png"

################################################################################
## Define Users Watchlist.                                                    ##
################################################################################
class Watchlist(models.Model):

    # Reverse relationship to the user who owns this watchlist
    user            = models.OneToOneField(settings.AUTH_USER_MODEL)
    # Signifies if this user can access their watchlist
    active          = models.BooleanField(default=True)
    modified        = models.DateTimeField(auto_now=True)
    created         = models.DateTimeField(default=timezone.now)

    class Meta:

        ordering = ["-created", "-modified"]

    def __str__(self):

        return "%s's Watchlist" % self.user

################################################################################
## Define SocialProfile Note Class.                                           ##
################################################################################
# Represents a note the user can make on a person's social profile
class SocialProfileNote(models.Model):

    # Reverse relationship to the watchlist this note belongs to
    # NOTE: Since we have that a SocialProfile has a ManyToMany relationship
    # to this model we may gain all notes that corresponds to a user
    # in a specific user's watchlist by doing
    #   (instance).notes.filter(watchlist=user.watchlist)
    # where instance is a SocialProfile instance and user is the currently
    # logged in user.
    watchlist       = models.OneToOneField(Watchlist)
    note            = models.TextField(blank=True)
    created         = models.DateTimeField(default=timezone.now)
    modified        = models.DateTimeField(auto_now=True)
    # Historical record for this model
    history         = HistoricalRecords()

    def __str__(self):

        return self.note

# class LinkedInProfile(models.Model):

#     pass

def get_upload_path(instance, filename):

    dirname = instance.__class__.__name__
    return os.path.join("images", dirname, str(instance), filename)

# class TwitterFriendship(models.Model):

#     handle           = models.CharField(max_length=255, blank=True)
#     profile_url      = models.URLField(max_length=2000, blank=True, null=True)
#     created          = models.DateTimeField(default=timezone.now)
#     modified         = models.DateTimeField(auto_now=True)

################################################################################
## Define TwitterProfile Class.                                               ##
################################################################################
# This model represents a local copy of a twitter user
class TwitterProfile(models.Model):

    avatar           = models.ImageField(upload_to=get_upload_path, storage=OverwriteStorage(), null=True)
    # IE can't handle rougly more than 2,000 characters for a URL so this is the
    # upper bound we can be sure of even for extremely long image urls.
    # URLs / Images
    avatar_url       = models.URLField(max_length=2000, blank=True, null=True)
    banner           = models.ImageField(upload_to=get_upload_path, storage=OverwriteStorage(), blank=True, null=True)
    banner_url       = models.URLField(max_length=2000, blank=True, null=True)
    latest_photo     = models.ImageField(upload_to=get_upload_path, storage=OverwriteStorage(), blank=True, null=True)
    latest_photo_url = models.URLField(max_length=2000, blank=True, null=True)
    
    latest_tweet     = models.CharField(max_length=255, blank=True, null=True)
    # Counts
    media_count      = models.IntegerField(blank=True, null=True)
    tweet_count      = models.IntegerField(blank=True, null=True)

    # following        = models.ManyToManyField(TwitterFriendship, symmetrical=False, blank=True)
    following_count  = models.IntegerField(blank=True, null=True)
    # followers        = models.ManyToManyField(TwitterFriendship, symmetrical=False, blank=True)
    followers_count  = models.IntegerField(blank=True, null=True)
    listed_count     = models.IntegerField(blank=True, null=True)
    like_count       = models.IntegerField(blank=True, null=True)

    # Miscellaneous twitter profile data
    handle           = models.CharField(max_length=255, blank=True)
    bio              = models.TextField(blank=True)
    website          = models.CharField(max_length=2000, blank=True, null=True)
    verified         = models.BooleanField(default=False)
    location         = models.CharField(max_length=255, blank=True)

    # Dates
    join_date        = models.CharField(max_length=255, blank=True)
    dob              = models.CharField(max_length=255, blank=True)
    created          = models.DateTimeField(default=timezone.now)
    modified         = models.DateTimeField(auto_now=True)
    # Historical record for this model so that we can track bio and
    # other changes
    history          = HistoricalRecords()

    class Meta:

        ordering = ['handle']

    # This updates the previous historical model to point to the last
    # avatar / banner / latest_photo url according to which of these
    # "field_name" presides to. This is because of the way the fields
    # use the custom OverwriteStorage to only keep two images new vs. old
    # and thus we need to reflect the rename (to old for previous new image on update)
    # in the historical model as this side-effect is not handled by the 
    # OverwriteStorage
    def fix_old_media_path(self, historical_record, field_name):

        old_media_path = getattr(historical_record, field_name)
        old_path, ext  = os.path.splitext(old_media_path.url)
        if "-new" in old_path:
            old_path = old_path[:-4] + "-old" + ext
            most_recent = HistoricalTwitterProfile.objects.filter(handle=self.handle).order_by("-history_date")[0]
            setattr(most_recent, field_name, old_path.replace(settings.MEDIA_URL, ""))
            most_recent.save()

    # data_dict contains the fields of this model as the keys and their values
    # as the (key, value) pairs and thus we may iterate over the dictionary
    # setting the field values. Note that the images are also set from the url
    # dynamically in accordance with set_image_from_url
    def set_attributes_from_dict(self, data_dict):

        try:
            history = self.history.most_recent()
        except Exception as e:
            history = None
        if not isinstance(data_dict, dict):
            data_dict = {k:v for (k,v) in data_dict}
        for key, value in data_dict.items():
            setattr(self, key, value)
            # If there isn't an image obviously we don't want to try
            # to send a request and set an image which == None
            if 'url' in key and value is not None:
                # Note that this assumes the naming schema follows this
                # convention:
                #     fieldname_url = models.URLField(...)
                #     fieldname     = models.ImageField(...)
                field_name          = "_".join(key.split("_")[:-1])
                filename            = value.split("/")[-1]
                filename, extension = os.path.splitext(filename)
                # The images will be saved like this:
                # media_cdn / TwitterProfile / handle / (avatar)(banner)(latest_photo)-(new)(old).extension
                # for fluid layout.
                set_image_from_url(
                    getattr(self, field_name), 
                    field_name + IMAGE_EXTENSION, 
                    value,
                )
                if history:
                    self.fix_old_media_path(history, field_name)

    # Upon initial TwitterProfile creation this method simply needs to be called and
    # then all fields will scraped from the twitter users page and filled with initial
    # data upon which further changes (from cron job scraping) can be compared against.
    def set_initial_twitter_data(self):

        r         = requests.get(BASE_URL.format(handle=self.handle), headers=HEADERS)
        data_dict = get_twitter_user_data(r)
        self.set_attributes_from_dict(data_dict)
        self.save()

    # Returns the representation of this object in a dictionary / "json" fashion
    # for easy comparison of changes when scraping.
    def get_dict_representation(self):

        return {
            'avatar_url':       self.avatar_url,
            'banner_url':       self.banner_url,
            'website':          self.website,
            'location':         self.location,
            'join_date':        self.join_date,
            'dob':              self.dob,
            'bio':              self.bio,

            'latest_tweet':     self.latest_tweet,
            'media_count':      self.media_count,
            'latest_photo_url': self.latest_photo_url,

            'tweet_count':      self.tweet_count,
            'followers_count':  self.followers_count,
            'following_count':  self.following_count,
            'like_count':       self.like_count,
            # Number of public lists this user is a part of...
            'listed_count':     self.listed_count,
            'handle':           self.handle,
            'verified':         self.verified,
        }

    # Updates the twitter user from the changes in diff, updates the historical
    # record change reason, and emails users who have an *** active *** watchlist
    # so that they are notified. Note we only wish to use active users since
    # users may have this twitter user in their watchlist but their trial period
    # may have ended and they have no active subscription.
    def update(self, diff):

        self.set_attributes_from_dict(diff)
        self.changeReason = "Cron Job Update"
        self.save()
        # Get unique list of watchlists pertaining to users so that users
        # only get the email once rather than potential duplicates if they
        # have this user in multiple watchlists.
        watchlists = self.socialprofile.watchlists.filter(active=True).distinct()
        send_mail(
            "%s Updated!" % (self.handle),
            "\n".join("%s changed to %s" % (k, v) for k, v in diff),
            settings.EMAIL_MAIN,
            # We want to send an email upon a different updated bio
            # to each user which has this twitter user in their watchlist

            # Note that since we are iterating over each twitter user in
            # the database which corresponds to every single user across
            # all watchlists and each watchlist can only have the user
            # once then there is a one to one correspondence ==> each
            # user will get an email for each update / changed twitter
            # user in their watchlist if and only if the user has an
            # updated bio as required.
            [watchlist.user.email for watchlist in watchlists],
            fail_silently=False,
        )

    # Compares the data just scraped vs the old data if there is a difference
    # i.e. - the twitter profile has been updated for any of the fields
    # this will appear in "difference" and then this difference list is
    # sent off to update_twitter_user for side-effects + emailing.
    def compare_instance_data(self):

        r            = requests.get(BASE_URL.format(handle=self.handle), headers=HEADERS)
        new_data     = get_twitter_user_data(r)
        current_data = self.get_dict_representation()
        difference   = set(new_data.items()) - set(current_data.items())
        if difference:
            self.update(difference)

    def __str__(self):

        return self.handle

################################################################################
## Define SocialProfile Class.                                                ##
################################################################################
# This model represents an abstract relationship defining a social profile
# for a user according to their title and first / last name.
# Now... This abstract model will then have a OneToOneField to
# different models representing local copies of social profles
# e.g. - TwitterProfile, LinkedInProfile, etcetera
# and thus this abtract model will encapsulate all social profiles that
# a user might have, along with their data, through the OneToOneField's
class SocialProfile(models.Model):

    title           = models.CharField(max_length=255, blank=False)
    first_name      = models.CharField(max_length=255, blank=False)
    last_name       = models.CharField(max_length=255, blank=False)
    # blank = null = True allows blank OneToOneField and sets them as not required in
    # the form since a user may not have a specific social profile...
    twitter         = models.OneToOneField(TwitterProfile, blank=True, null=True)
    # linkedin        = models.OneToOneField(LinkedInProfile, blank=True, null=True)
    # Holds what watchlists this social profile is in across all users.
    watchlists      = models.ManyToManyField(Watchlist, related_name="watchlists")
    # Holds all notes related to this social profile across all users
    notes           = models.ManyToManyField(SocialProfileNote, related_name="notes", blank=True)
    created         = models.DateTimeField(default=timezone.now)
    active          = models.BooleanField(default=True)
    # Serves for unique generation of slugs.
    uuid            = models.UUIDField(default=uuid.uuid4, editable=False)
    # Holds the slug for this user for URL routing.
    slug            = models.SlugField(unique=True)

    def __str__(self):

        return "%s - %s %s" % (self.title, self.first_name, self.last_name)