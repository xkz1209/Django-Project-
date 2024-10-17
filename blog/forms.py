from django import forms
from .models import Comment,Article

class CreateCommentForm(forms.ModelForm):
    '''A form to create comment data'''
    
    class Meta:
        '''associate this form with the comment model'''
        model = Comment
        #remove the article becasuse we 
        fields = ['author','text']
        
class CreateArticleForm(forms.ModelForm):
    '''A form to create a new Article'''
    class Meta:
        '''associate this form with a Model, specify which fields to create'''
        model = Article
        fields = ['author','title','text','image_file']
        
        