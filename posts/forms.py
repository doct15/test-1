################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define Posts (Blog) Forms.                                          ##
################################################################################



################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django import forms

################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from pagedown.widgets import PagedownWidget

################################################################################
## Import Defined Models.                                                     ##
################################################################################
from .models import Post






################################################################################
## Define Blog Posts Forms Class.                                             ##
################################################################################
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]
