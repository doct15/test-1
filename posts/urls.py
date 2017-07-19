################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Posts (Blog) URLs.                                           ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.conf.urls import url
from django.contrib import admin





################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .views import (
	post_list,
	post_create,
	post_detail,
	post_update,
	post_delete,
	)





################################################################################
## Define the Posts App URL Patterns.                                         ##
################################################################################
urlpatterns = [
	url(r'^$', post_list, name='list'),
    url(r'^create/$', post_create),
    # url(r'^(?P<id>\d+)/$', post_detail, name='detail'),
    # url(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
    # url(r'^(?P<id>\d+)/delete/$', post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

	## Update URLs to use Slugs												  ##
	url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]
