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

    username = forms.CharField(label="username", required=True)
    password1 = forms.CharField(label="password1", required=True)
    password2 = forms.CharField(label="password2", required=True)


class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']

    message = forms.CharField(label="Message",required=True)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['firstName', 'lastName' , 'user']  # first_name, and last_name fields

    city = forms.CharField(label="City", required=True)
    email = forms.CharField(label="Email", required=True)
    image_url = forms.CharField(label="Image URL", required=True)


class UpdateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']
    message = forms.CharField(label="Message",required=True)
