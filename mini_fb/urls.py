from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),#new
  path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), 
  path(r'create_profile/',views.CreateProfileView.as_view(),name='create_profile'),#new add
  path(r'profile/<int:pk>/create_status/',views.CreateStatusMessageView.as_view(),name='create_status'),#new add
]
