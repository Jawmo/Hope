from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=254, help_text='', label="Character First Name")
    email = forms.EmailField(max_length=254, help_text='', label="Email")
    password1 = forms.CharField(max_length=254, widget=forms.PasswordInput, help_text='', label="Password:")
    password2 = forms.CharField(max_length=254, widget=forms.PasswordInput, help_text='', label="Confirm Password:")


    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')