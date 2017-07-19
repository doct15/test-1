################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Defined ReUsable App Utilities.                                     ##
################################################################################



################################################################################
## Import Required Python Libraries.                                          ##
################################################################################
import random
import string





################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.text import slugify
from storages.backends.s3boto import S3BotoStorage




################################################################################
## Define AWS S3 Storage Requirements.                                        ##
################################################################################
StaticRootS3BotoStorage = lambda: S3BotoStorage(location='static')
MediaRootS3BotoStorage  = lambda: S3BotoStorage(location='media')


################################################################################
## Define the Unique Strings Generator.                                       ##
################################################################################
def unique_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))

################################################################################
## Define sitewide Slug generation.                                           ##
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
