################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Posts (Blog) Admin.                                          ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.contrib import admin

################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .models import Post






################################################################################
## Define the Admin Class.                                                    ##
################################################################################
class PostModelAdmin(admin.ModelAdmin):
    list_display        = ["title", "timestamp", "updated"]
    list_display_links  = ["updated"]
    list_editable       = ["title"]
    list_filter         = ["timestamp", "updated"]
    search_fields       = ["title", "content"]

    class Meta:
        model       = Post


################################################################################
## Register with Admin.                                                       ##
################################################################################
admin.site.register(Post, PostModelAdmin)
