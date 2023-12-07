from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input',}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), required=True)



    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

