################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Watchlist Views.                                             ##
################################################################################

################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import reverse, get_object_or_404, redirect

################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from django.utils import timezone
import requests
from bs4 import BeautifulSoup

################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .forms import SocialProfileAddForm
from .models import SocialProfile, TwitterProfile, Watchlist
from base_utilities import (
    NeverCacheMixin,
    my_slugify,
)

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

# Create
# Retreive
# Update
# Delete
# List
# Search

################################################################################
## Watchlist - List View.                                                     ##
################################################################################
# This view represents the users watchlist which contains
# the list of all SocialProfile objects which they are
# monitoring.
class WatchlistView(LoginRequiredMixin, ListView):

    paginate_by = 12
    template_name = "lists/watchlist_list.html"
    context_object_name = "social_profiles"

    def get_queryset(self):

        # We want to filter the SocialProfile objects which are
        # only in this users watchlist.
        queryset = SocialProfile.objects.filter(watchlists__in=[self.request.user.watchlist])
        query = self.request.GET.get("q")
        # We can then filter further according to the query
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)|
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            ).distinct()
        # Let's display them alphabetically for a nice UI for the user...
        return queryset.order_by("last_name")

################################################################################
## SocialProfile - Create View.                                               ##
################################################################################
# This view represents a form / create view in which the user can add
# the abstract social profile model to their watchlist.
# Note that the form encapsulates setting up the other social profiles
# and is extensible past twitter.
class SocialProfileAddView(LoginRequiredMixin, CreateView):

    model             = SocialProfile
    form_class        = SocialProfileAddForm
    template_name     = "lists/watchlist_add_form.html"
    SLUG_FIELDS       = ['first_name', 'last_name', 'uuid']
    SLUG_RESTRICTIONS = {
        'uuid': {
            'max_length': 8,
        }
    }

    def get_form_kwargs(self, *args, **kwargs):

        kwargs = super(SocialProfileAddView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):

        return reverse("lists:watchlist")

    def form_valid(self, form):

        # We need to save twitter first so that we can properly set
        # that the astract social profile created has a twitter page.
        twitter = form['twitter'].save(commit=False)
        twitter.set_initial_twitter_data()
        social = form['social'].save(commit=False)
        social.twitter = twitter
        # Unique slug from UUID, first, last name and my function.
        # Note that function isn't needed here but I left it since you
        # just have to change the fields list [] below if you want
        # to change how the slugs work....
        social.slug = my_slugify(social, self.SLUG_FIELDS, self.model, restrictions=self.SLUG_RESTRICTIONS)
        social.save()
        social.watchlists.add(self.request.user.watchlist)
        # Let's redirect the user back to their watchlist.
        return redirect(self.get_success_url())

################################################################################
## SocialProfile - Update View.                                               ##
################################################################################
# This isn't implemented yet....
class SocialProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = SocialProfile
    form_class = SocialProfileAddForm
    template_name = "lists/watchlist_update_form.html"

    def get_form_kwargs(self):

        kwargs = super(SocialProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs.update(instance={
            'social':  self.object,
            'twitter': self.object.twitter,
        })
        return kwargs

    def get_success_url(self):

        return reverse("lists:watchlist")

################################################################################
## TwitterProfile - Detail View.                                              ##
################################################################################
# This view represents the detail view of a specific TwitterProfile
# which is a part of the broader abstract SocialProfile which a user
# is watching in their watchlist.

# Note that we have required login so that anyone cannot scrape this page
# for data. This would defeat the purpose of memberships / trial period.
class TwitterProfileDetailView(NeverCacheMixin, LoginRequiredMixin, DetailView):

    TWITTER_CRON_REASON = "Cron Job Update"
    model = TwitterProfile
    template_name = "lists/watchlist_twitter_detail.html"
    context_object_name = "twitter"

    # If the object is not found it will raise a 404 page.
    def get_object(self):

        return get_object_or_404(TwitterProfile, socialprofile__slug=self.kwargs.get("slug"))

    # By overriding get_context_data we are sending the current twitter
    # profile model as well as the previous model corresponding to
    # last_update if it exists otherwise we are signifying that there has
    # not been any updates. Note we onyl need to check the length by
    # definition of the cron job.
    def get_context_data(self, *args, **kwargs):

        context = super(TwitterProfileDetailView, self).get_context_data(*args, **kwargs)
        history = self.object.history.all().order_by("-history_date")
        context['updated'] = False
        update             = None
        # There must be at least two items in the history
        if len(history) > 1:
            update = history[1]
            context['updated'] = True
            # found_latest_cron_job = False
            # # With luck the latest cron job will be the first index since
            # # we sorted by the date created last. However, first could
            # # be simple updatedsthrough admin panel etcetera.
            # index                 = 0
            # while not found_latest_cron_job and index < len(history):
            #     update  = history[index]
            #     if (update.history_change_reason == self.TWITTER_CRON_REASON and 
            #         not update is self.object):
            #         found_latest_cron_job = True
            #         context['updated']     = True
            #     else:
            #         index += 1
        context['last_update'] = update
        return context

################################################################################
## SocialProfile - Detail View.                                              ##
################################################################################
# This view corresponds to the general detail view in which the
# user can view all of the data across all social profiles
# Given the definition of the OneToOneField's definining the specific
# social profiles you may access them through:
#     instance.twitter.(field), instance.github.(field), etcetera
# For displaying the data specific to those profiles.
# Similarly, we have also overriden get_context_data so that we may
# display the list of notes the user has setup corresponding to this
# social profile they are monitoring.
class SocialProfileDetailView(LoginRequiredMixin, DetailView):

    model = SocialProfile
    template_name = 'lists/watchlist_social_detail.html'
    context_object_name = "profile"

    def get_object(self):

        return get_object_or_404(SocialProfile, slug=self.kwargs.get("slug"))

    # We need to add the notes in to be displayed...
    def get_context_data(self, *args, **kwargs):

        context = super(SocialProfileDetailView, self).get_context_data(*args, **kwargs)
        context['notes'] = self.object.notes.filter(watchlist=self.request.user.watchlist)
        return context