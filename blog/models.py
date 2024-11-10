from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  ##NEW
# Create your models here.
#define data models for this application by creating class definition

class Article(models.Model):
    '''Encapsulate the data for a blog Article is a model'''
    #each article will be associated with a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    #data attribute:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    #image_url = models.URLField(blank=True) #new added
    #new added field
    image_file = models.ImageField(blank=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
     
    def get_comments(self):
        '''retrieve all comments for this articles''' 
        comments = Comment.objects.filter(article=self)
        return comments
    
    def get_absolute_url(self):
        '''return a url to view one instance of this object'''
        #pk = self.pk is the primary key for an object instance
        return reverse('article', kwargs={'pk':self.pk})
     
class Comment(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return f'{self.text}'