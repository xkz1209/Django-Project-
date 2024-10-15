# Create your views here.
from django.shortcuts import render
from . models import *
from django.views.generic import ListView,DetailView,CreateView
from .forms import CreateProfileForm,CreateStatusMessageForm
from typing import Any
from django.urls import reverse_lazy,reverse ## NEW


class ShowAllProfilesView(ListView):
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profile'
    
    
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'single_profile'
    
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    success_url = reverse_lazy('show_all_profiles')
    
    
    
    def form_valid(self, form):
        '''this method executes after form submission'''
        print(f'CreateProfileView.form_valid(): form={form.cleaned_data}')
        print(f'CreateProfileView.form_valid(): self.kwargs={self.kwargs}')
        # find the article with the PK from the URL
        # delegaute work to the superclass version of this method
        return super().form_valid(form)
    def get_success_url(self):
        profile = self.object
        return  profile.get_absolute_url()

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('show_profile', kwargs={'pk': pk})

