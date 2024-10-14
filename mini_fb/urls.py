from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),#new
  path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), 
]

