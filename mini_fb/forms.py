from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):

    class Meta:
        '''associate this form with the Profile  model; select fields.'''
        model = Profile 
        fields = ['firstName', 'lastName', 'city', 'email', 'image_url' ]  # which fields from Profile  should we use
        
    firstName = forms.CharField(label="First Name", required=True)
    lastName = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="city", required=True)
    email = forms.CharField(label="email", required=True)
    image_url = forms.CharField(label="image_url", required=True)


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']

    message = forms.CharField(label="Message",required=True)
