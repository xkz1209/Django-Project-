## hw/url.py
## the app-specific URLS for the hw applicaton

from django.urls import path
from django.conf import settings
from . import views

#create a list of URLs for this app
urlpatterns = [
    path(r'',views.base, name="base"),        #our first , r for regular expressions matching
    path('quote/', views.quote, name="quote"),
    path('show_all/', views.show_all, name="show_all"),
    path('about/', views.about, name="about")
]