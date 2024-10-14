# Create your views here.
from django.shortcuts import render
from . models import *
from django.views.generic import ListView,DetailView, CreateView
import random
from . forms import *
from django.urls import reverse
from typing import Any

class ShowAllView(ListView):
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'
    
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
    
class CreateCommentView(CreateView):
    
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
        
        
    def get_context_data(self, **kwargs: random.Any) -> dict[str, Any]:
        '''build the template context data - a dict of key-value paris'''
        #get the super class version of context data
        context = super().get_context_data(**kwargs)
        #add the article to the context data
          #find the article with the PK from the URL
        article = Article.objects.get(pk=self.kwargs['pk'])
        context['article'] = article
        
        return 
        
        