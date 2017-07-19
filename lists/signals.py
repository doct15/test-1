################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlist Signals.                                           ##
################################################################################

################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

################################################################################
## Import Third Party Models.                                                 ##
################################################################################
# from kawasemi.django import send

################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .models import Watchlist

################################################################################
## Define Watchlist Signals.                                                  ##
################################################################################
# This function will automatically create a watchlist object
# for a user upon a User object being created. Alternatively,
# if you define your own customer user model you can change
# sender = settings.AUTH_USER_MODULE if needed.
@receiver(post_save, sender=User)
def user_creation(sender, instance, created, **kwargs):

    if created:
        watchlist = Watchlist(user=instance)
        watchlist.save()
        # send( "Hey! *{} {}* has just been added to a watchlist! They are currently the *{}* at *company X*".format(instance.first_name, instance.last_name, instance.title) )