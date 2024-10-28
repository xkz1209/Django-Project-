from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name='show_profile'),#new
  path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'), 
  path(r'create_profile/',views.CreateProfileView.as_view(),name='create_profile'),#new add
  path(r'profile/<int:pk>/update/',views.UpdateProfileView.as_view(),name='update_profile'),#new add
  path(r'profile/<int:pk>/create_status/',views.CreateStatusMessageView.as_view(),name='create_status'),#new add

  path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
  path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),
  
  path('profile/<int:pk>/add_friend/<int:other_pk>/', views.CreateFriendView.as_view(), name='add_friend'),
  path('profile/<int:pk>/friend_suggestions/', views.FriendSuggestionsView.as_view(), name='friend_suggestions'),
  
  path('profile/<int:pk>/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),
]
