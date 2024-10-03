# Create your views here.
from django.shortcuts import render
from . models import *
from django.views.generic import ListView

class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profile'