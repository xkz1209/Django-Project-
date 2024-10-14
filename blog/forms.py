from django import forms
from .models import Comment

class CreateCommentForm(forms.ModelForm):
    '''A form to create comment data'''
    
    class Meta:
        '''associate this form with the comment model'''
        model = Comment
        #remove the article becasuse we 
        fields = ['author','text']
        
        