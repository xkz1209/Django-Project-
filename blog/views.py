# Create your views here.
from django.shortcuts import render, redirect
from . models import *
from django.views.generic import ListView,DetailView, CreateView
import random
from . forms import *
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin ##new added
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login

class ShowAllView(ListView):
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
    
    
    def dispatch(self,*args, **kwargs):
        print(f"self.request.user={self.request.user}")
        return super().dispatch(*args, **kwargs)
    
    
class RandomArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    
    def get_object(self):
        '''return the instance of the article object to show'''
        #get all articles and pick one at random
        all_articles = Article.objects.all()    # select *
        return random.choice(all_articles)
    
class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'
    
class CreateCommentView(LoginRequiredMixin, CreateView):
    
    '''a view to show/process the create comment form:
        GET: sends back the form
        POST: read the form data, create an instance of COmment; save to database
    '''
    

    '''a view to show/process the create comment form'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    
    def get_success_url(self) -> str:
        '''return the URL to redirect to after successful create'''
        #return reverse("show_all")
        return reverse("article", kwargs=self.kwargs)
    
    def form_valid(self,form):
        '''execute after form submission'''
        print('CreateCommentView.form_valid(): form={form.cleaned_data}')
        print('CreateCommentView.form_valid(): self.kwargs={self.kwargs}')
        #find the article with the PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])
        
        #attach the article to the comment
        #form.instance is the new comment object
        form.instance.article = article

        #delegate work to the superclass version of this method
        return super().form_valid(form)
        
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''build the template context data - a dict of key-value paris'''
        #get the super class version of context data
        context = super().get_context_data(**kwargs)
        #add the article to the context data
          #find the article with the PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['article'] = article
        
        return 
        
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''View to create a new Article instance'''
    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"
    
        
    def get_login_url(self) -> str:
        '''return the url required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        '''adding some debugging statements'''
        print(f'CreateArticleView: from.cleaned_data={form.cleaned_data}')
        #find which users is logged in 
        
        
        #attach the user to the new article instance
        user = self.request.user
        print(f'CreateArticleView:form_valid() user={user}')
        form.instance.user = user

    
        #delegate work to superclass
        return super().form_valid(form)
    
class RegistrationView(CreateView):
    '''Display and process the UsereCreationForm for account registration'''
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    
    def dispatch(self, *args, **kwargs):
        '''handle the user creation process'''
        #we handle the HTTP POST request -> form submission
        if self.request.POST:
            print(f"self.request.POST={self.request.POST}")
            #reconstruct the UserCreationForm from the HTTP POST
            form = UserCreationForm(self.request.POST)
            #save the new User object
            user = form.save() #create a new instance of User object in the database, and return a reference to it. we save it to user
            print(f"RegistrationView.dispatch: created user {user}")
            #log in the user
            login(self.request, user)
            print(f"RegistrationView.dispatch,user {user} is logged in")
            #redirect the user to some page view...
            
            return redirect(reverse('show_all'))
        
        
        #let the superclass createView  handle the HTTP GET:
        return super().dispatch(*args, **kwargs)
    
    
    
    
    
    
    