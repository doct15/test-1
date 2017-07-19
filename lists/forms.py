################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlist Forms.                                             ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django import forms
from django.utils.safestring import mark_safe
from django.shortcuts import reverse


################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from betterforms.multiform import MultiModelForm
from collections import OrderedDict
import requests


################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .models import SocialProfile, TwitterProfile


BASE_TWITTER_URL = "https://twitter.com/{handle}/"





################################################################################
## Define the Social Profile Form.                                            ##
################################################################################
class SocialProfileForm(forms.ModelForm):

    class Meta:

        model = SocialProfile
        fields = ['title', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        super(SocialProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=False):

        instance = None
        try:
            instance = SocialProfile.objects.get(
                title=self.cleaned_data['title'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
        except SocialProfile.DoesNotExist:
            instance = super(SocialProfileForm, self).save(commit=False)
        return instance





################################################################################
## Define the Twitter Profile Form.                                           ##
################################################################################
class TwitterProfileForm(forms.ModelForm):

    class Meta:

        model = TwitterProfile
        fields = ['handle']

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop("user", None)
        super(TwitterProfileForm, self).__init__(*args, **kwargs)
        self.fields['handle'].required = False
        self.fields['handle'].label = "Twitter Handle"

    def clean_handle(self):

        handle = self.cleaned_data['handle']
        if handle:
            r = requests.get(BASE_TWITTER_URL.format(handle=handle))
            # Twitter raises a 404 (object not found...) status
            # if the twitter handle does not exist.
            if r.status_code == 404:
                raise forms.ValidationError("That user does not exist!")
            try:
                twitter = TwitterProfile.objects.get(handle=handle)
                try:
                    socialprofile = twitter.socialprofile
                    slug = socialprofile.slug
                    if self.user in [watchlist.user for watchlist in socialprofile.watchlists.all()]:
                        raise forms.ValidationError(mark_safe(
                            ("A user with that twitter account already exists in your watchlist. " +
                             " You may view their <a href='{0}'>profile</a> or <a href='{1}'>edit</a> it.".format(
                                 reverse("lists:detail", kwargs={'slug': slug}),
                                 reverse("lists:edit", kwargs={'slug': slug}))
                            ))
                        )
                except SocialProfile.DoesNotExist:
                    pass
            except TwitterProfile.DoesNotExist:
                pass
        return handle

    def save(self, commit=False):

        instance = None
        try:
            instance = TwitterProfile.objects.get(handle=self.cleaned_data['handle'])
        except TwitterProfile.DoesNotExist:
            instance = super(TwitterProfileForm, self).save(commit=False)
        return instance





################################################################################
## Define the Social Profile ADD Form.                                        ##
################################################################################
class SocialProfileAddForm(MultiModelForm):

    form_classes = OrderedDict((
        ('social', SocialProfileForm),
        ('twitter', TwitterProfileForm),
    ))

    def __init__(self, *args, **kwargs):

        super(SocialProfileAddForm, self).__init__(*args, **kwargs)
