from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rides.models import Profile
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number','car','bio','hometown')
        