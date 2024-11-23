from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Ticket,Client


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    passport_id = forms.CharField(max_length=50)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone_number = forms.CharField(max_length=15)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            client = Client.objects.create(
                                 user=user,
                                 first_name=self.cleaned_data['first_name'],
                                 last_name=self.cleaned_data['last_name'],
                                 email=self.cleaned_data['email'],
                                 passport_id=self.cleaned_data['passport_id'],
                                 date_of_birth=self.cleaned_data['date_of_birth'],
                                 gender=self.cleaned_data['gender'],
                                 phone_number=self.cleaned_data['phone_number']
                                )
        return user

class UserLoginForm(AuthenticationForm):
    pass

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['flight', 'quantity']
