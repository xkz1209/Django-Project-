from django.urls import path
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views ##new

urlpatterns = [
  path(r'', views.RandomArticleView.as_view(), name='random'), #new
  path(r'show_all', views.ShowAllView.as_view(), name='show_all'), 
  path(r'article/<int:pk>', views.ArticleView.as_view(), name='article'),#new
  #path(r'create_comment', views.CreateCommentView.as_view(), name='create_comment'),
  path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(),name='create_comment'),
  path(r'create_article',views.CreateArticleView.as_view(), name="create_article"),#new added
  #authentication URLS:
  path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
  path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
  path('register/',views.RegistrationView.as_view(), name='register')
]
