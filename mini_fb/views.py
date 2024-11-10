# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.shortcuts import get_object_or_404,redirect,render
from . models import *
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import CreateProfileForm,CreateStatusMessageForm,UpdateProfileForm,UpdateStatusMessageForm
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
    def get_object(self,queryset=None):
        return get_object_or_404(Profile,pk=self.kwargs['pk'])
    
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    success_url = reverse_lazy('show_all_profiles')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        '''this method executes after form submission'''
        print(f'CreateProfileView.form_valid(): form={form.cleaned_data}')
        print(f'CreateProfileView.form_valid(): self.kwargs={self.kwargs}')
        # find the article with the PK from the URL
        # delegaute work to the superclass version of this method
        print(self.request.POST)
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request,user)
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return  super().form_valid(form)
        else:
            print(user_form.errors)
            form.add_error(None,user_form.errors)
            return super().form_invalid(form)
    def get_success_url(self):
        profile = self.object
        return  profile.get_absolute_url()

class CreateStatusMessageView(LoginRequiredMixin,CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        
        for file in files:
            image = Image(
                status=sm,  
                image_file=file 
            )
            image.save()
        
        
        return super().form_valid(form)
    
    
    def get_success_url(self):
        pk = Profile.objects.get(user=self.request.user).pk
        return reverse_lazy('show_profile', kwargs={'pk': pk})


class UpdateProfileView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    success_url = reverse_lazy('show_profile')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
    def get_success_url(self):
        return reverse_lazy('show_profile', kwargs={'pk': self.object.pk})


class DeleteStatusMessageView(LoginRequiredMixin,DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    success_url = reverse_lazy('show_profile')
    def get_success_url(self):
        # Redirect to the profile page of the user who posted the status message
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})
    success_url = reverse_lazy('show_profile')

class UpdateStatusMessageView(LoginRequiredMixin,UpdateView):
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'
    context_object_name = 'status_message'

    success_url = reverse_lazy('show_profile')
    def get_success_url(self):
        # Redirect to the profile page of the user who posted the status message
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(LoginRequiredMixin,View):
    def dispatch(self,request,*args,**kwargs):
        other_pk = self.kwargs['other_pk']
        profile1 = get_object_or_404(Profile,user=request.user)
        other_profile = get_object_or_404(Profile,pk=other_pk)

        profile1.add_friend(other_profile)

        return redirect('show_profile',pk=profile1.pk)

class FriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    def get_object(self,queryset=None):
        return Profile.objects.get(user=self.request.user)



class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self,queryset=None):
        return Profile.objects.get(user=self.request.user)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['news_feed'] = profile.get_news_feed()
        return context
