################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlists Admin.                                            ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.contrib import admin


################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from simple_history.admin import SimpleHistoryAdmin



################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .models import (
    Watchlist,
    SocialProfile,
    SocialProfileNote,
    TwitterProfile,
)





################################################################################
## Define the Watchlist Admin Class.                                          ##
################################################################################
class WatchlistAdmin(admin.ModelAdmin):

    list_display        = ["user", "created", "modified"]
    list_display_links  = ["user", "modified"]
    list_filter         = ["created", "modified"]
    search_fields       = ["user"]

    class Meta:

        model           = Watchlist


################################################################################
## Register with Admin.                                                       ##
################################################################################
admin.site.register(Watchlist, WatchlistAdmin)





################################################################################
## Define the SocialProfile Admin Class.                                      ##
################################################################################
class SocialProfileAdmin(SimpleHistoryAdmin):

    list_display        = ["title", "first_name", "last_name", "twitter", "created"]
    list_display_links  = ["title", "first_name", "last_name", "twitter"]
    list_filter         = ["created"]
    search_fields       = ["twitter", "active", "title", "first_name", "last_name"]

    class Meta:

        model           = Watchlist


################################################################################
## Register with Admin.                                                       ##
################################################################################
admin.site.register(SocialProfile, SocialProfileAdmin)





################################################################################
## Define the SocialProfile Note Admin Class.                                 ##
################################################################################
class SocialProfileNoteAdmin(SimpleHistoryAdmin):

    # list_display        = ["note", "watchlist", "created", "modified"]
    # list_display_links  = ["note", "watchlist"]
    # list_filter         = ["note", "watchlist"]
    # search_fields       = ["note", "watchlist", "created", "modified"]

    class Meta:

        model           = SocialProfileNote


################################################################################
## Register with Admin.                                                       ##
################################################################################
admin.site.register(SocialProfileNote, SocialProfileNoteAdmin)





################################################################################
## Define the TwitterProfile Admin Class.                                     ##
################################################################################
class TwitterProfileAdmin(SimpleHistoryAdmin):

    list_display       = ['handle', 'bio', 'created', 'modified']
    list_display_links = ['handle']
    list_filter        = ['handle']
    search_fields      = ['handle', 'created', 'modified']

    class Meta:

        model           = TwitterProfile


################################################################################
## Register with Admin.                                                       ##
################################################################################
admin.site.register(TwitterProfile, TwitterProfileAdmin)
