################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlists URLs.                                             ##
################################################################################

################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.conf.urls import url, include
from django.contrib import admin

################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .views import (
	WatchlistView,
    SocialProfileAddView,
    SocialProfileUpdateView,
    SocialProfileDetailView,
    TwitterProfileDetailView,
	#post_create,
	#post_update,
	#post_delete,
	)

################################################################################
## Define the Lists App URL Patterns.                                         ##
################################################################################
urlpatterns = [
	url(r'^$', WatchlistView.as_view(), name='watchlist'),
    url(r'^add/$', SocialProfileAddView.as_view(), name='create'),
    url(r'^(?P<slug>[\w\-]+)/$', SocialProfileDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w\-]+)/edit/$', SocialProfileUpdateView.as_view(), name="edit"),
    url(r'^(?P<slug>[\w\-]+)/twitter/$', TwitterProfileDetailView.as_view(), name='twitter'),
]