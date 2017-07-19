################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Defined ReUsable App Utilities.                                     ##
################################################################################



################################################################################
## Import Required Python Libraries.                                          ##
################################################################################
import datetime
import math
import re
import random
import string


################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from django.utils.html import strip_tags
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.text import slugify




################################################################################
## Create Slug Function.                                                      ##
################################################################################
def create_slug(instance, new_slug=None):
    if not new_slug:
        slug = slugify(instance.title)
    else:
        slug = new_slug
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        string_unique = unique_string_generator()
        newly_created_slug = slug + "-{id_}".format(id_=string_unique)
        return create_slug(instance, new_slug=newly_created_slug)
    return slug




################################################################################
## Count Words Function.                                                      ##
################################################################################
def count_words(html_string):
    # html_string = """
    # <h1>This is a title</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words) #joincfe.com/projects/
    return count




################################################################################
## Get Read Time Function.                                                    ##
################################################################################
def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0) #assuming 200wpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)
