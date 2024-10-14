from django.db import models

# Create your models here.
#define data models for this application by creating class definition

class Article(models.Model):
    '''Encapsulate the data for a blog Article is a model'''
    #data attribute:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) #new added
    
    def __str__(self):
        return f"{self.title} by {self.author}"
     
    def get_comments(self):
        '''retrieve all comments for this articles''' 
        comments = Comment.objects.filter(article=self)
        return comments
     
class Comment(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return f'{self.text}'