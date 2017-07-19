################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlists Admin.                                            ##
################################################################################

################################################################################
## Import Required Libraries.                                                 ##
################################################################################
import itertools
import requests
import os

################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings


################################################################################
## Import Defined Models.                                                     ##
################################################################################

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class NeverCacheMixin(object):

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        
        return super(NeverCacheMixin, self).dispatch(*args, **kwargs)

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):

        filename, ext  = os.path.splitext(name)
        if "-new" in filename or "-old" in filename:
            filename   = filename[:-4]
        new_name       = filename + "-new" + ext
        old_name       = filename + "-old" + ext
        old_path       = os.path.join(settings.MEDIA_ROOT, old_name)
        new_path       = os.path.join(settings.MEDIA_ROOT, new_name)
        if os.path.exists(old_path) and os.path.exists(new_path):
            os.remove(old_path)
            os.rename(new_path, old_path)
            name = new_name
        # Edge case for when the initial scrape grabbed the first 
        # image. In which case.. we want to save this as the new
        # - i.e. second image - from which the "if" condition above
        # will be hit from this point onwards.
        elif os.path.exists(old_path):
            name = new_name
        else:
            name = old_name
        return name

# Takes the field on a model which references a models.ImageField the
# path which the file is to be uploaded to in settings.MEDIA_ROOT and
# the url at which the image we are setting is located.
def set_image_from_url(field, path, url):

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        img_content = ContentFile(response.content)
        # Note that this is just saving the new location and the side-effects
        # aren't seen until the actual model is saved. Hence, the layout
        # is still conistent.

        # Save = False is important here otherwise it would call
        # instance.save() in ImageField's .save() method reflecting
        # a new history entry which we want to limit.
        field.save(path, img_content, save=False)

# Just an extension of my_slugify so we can fluidly add restrictions for
# certain fields for dynamic slug creation as we wish arbitrarily.
# Can be extended with more conditions / specifications as they arise.
def get_slug_attr(instance, field_name, restrictions):

    field = getattr(instance, field_name)
    if field_name in restrictions:
        if 'max_length' in restrictions[field_name]:
            max_length = restrictions[field_name]['max_length']
            field = str(field)[:max_length]
    return field

################################################################################
## Define the Slugify Function.                                               ##
################################################################################
def my_slugify(instance, fields, _model, delimiter=" ", restrictions=None):

    length = _model._meta.get_field('slug').max_length
    instance.slug = original = slugify(
        delimiter.join(
            str(get_slug_attr(instance, field, restrictions)) 
            if not isinstance(getattr(instance, field), str) else
                get_slug_attr(instance, field, restrictions) 
            for field in fields
        )
    )[:length]

    #We want to loop until we find a slug name that does not already
    #exist in the database.

    for x in itertools.count(1):
        if not _model.objects.filter(slug=instance.slug).exists():
            break
        instance.slug = original[:length - len(str(x)) - 1]
    return instance.slug
