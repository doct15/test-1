################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Accounts View.                                               ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.shortcuts import render
# from django.contrib.auth import get_user_model
# from django.http import HttpResponseRedirect
# from django.shortcuts import render, get_object_or_404, redirect
# # from django.views import View
# from django.views.generic import DetailView
# from django.views.generic.edit import FormView


################################################################################
## Import Third Party Models.                                                 ##
################################################################################


################################################################################
## Import Defined Models.                                                     ##
################################################################################
# from .models import UserProfile




################################################################################
## Define the Accounts Login.                                                 ##
################################################################################
# class UserDetailView(DetailView):
#     template_name = 'accounts/user_detail.html'
#
#     def get_object(self):
#         return get_object_or_404(
#                     User,
#                     )
#     def get_context_data(self, *args, **kwargs):
#         context = super(UserDetailView, self).get_context_data(*args, **kwargs)
#         following = UserProfile.objects.is_following(self.request.user, self.get_object())
#         return context
