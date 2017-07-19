################################################################################
## MAAS Digital.                                                              ##
## RadHR.                                                                     ##
## Language: Python 3.6                                                       ##
## About: Define RadHR Main URLs.                                             ##
################################################################################
"""radhr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
################################################################################
## Import Required Libraries.                                                 ##
################################################################################
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


################################################################################
## Import Third Party Models.                                                 ##
################################################################################
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls


################################################################################
## Import Defined Models.                                                     ##
################################################################################
## from accounts.views import (login_view, register_view, logout_view)


################################################################################
## Define the Main URL Patterns.                                              ##
################################################################################
urlpatterns = [
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    # url(r'^pages/', include(wagtail_urls)),


    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^comments/', include("comments.urls", namespace='comments')),

    # url(r'^register/', register_view, name='register'),
    # url(r'^login/', login_view, name='login'),
    # url(r'^logout/', logout_view, name='logout'),
    url(r'^lists/', include("lists.urls", namespace='lists')),


    url(r'^posts/', include("posts.urls", namespace='posts')),
    #url(r'^posts/', include("posts.urls", namespace='posts')),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

    # url(r'^user/', include('accounts.urls', namespace='profiles')),

    # Wagtail will handle URLs under /pages/, leaving the root URL and other paths to be handled as normal by your Django project.
    # If you want Wagtail to handle the entire URL space including the root URL, this can be replaced with:
    url(r'', include(wagtail_urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
