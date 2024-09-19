## hw/url.py
## the app-specific URLS for the hw applicaton

from django.urls import path
from django.conf import settings
from . import views

#create a list of URLs for this app
urlpatterns = [
    path(r'',views.home, name="home")        #our first , r for regular expressions matching
]