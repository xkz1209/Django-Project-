# Create your views here.
from django.shortcuts import render
from . models import *
from django.views.generic import ListView,DetailView


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profile'
    
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'single_profile'