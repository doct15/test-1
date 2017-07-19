################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Comments Forms.                                              ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django import forms

################################################################################
## Import Third Party Models.                                                 ##
################################################################################


################################################################################
## Import Defined Models.                                                     ##
################################################################################







################################################################################
## Define Comments Forms Class.                                               ##
################################################################################
class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea)
