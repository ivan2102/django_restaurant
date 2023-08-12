from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, UserProfile
from .validators import image_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
            model = User
            fields = ['first_name', 'last_name', 'username', 'email', 'password' ]

    def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password != confirm_password:
                        raise forms.ValidationError('Password and confirm password do not match')
            

class UserProfileForm(forms.ModelForm):

 address = forms.CharField()
 address.widget.attrs.update({'placeholder': 'Address', 'required': 'required'})
 
 profile_picture = forms.FileField(validators=[image_validator])
 profile_picture.widget.attrs.update({'class': 'btn btn-info'}),

 cover_photo = forms.FileField(validators=[image_validator])
 cover_photo.widget.attrs.update({'class': 'btn btn-info'})

 #latitude = forms.CharField()
 #latitude.widget.attrs.update({ 'readonly': 'readonly' })

 #longitude = forms.CharField()
 #longitude.widget.attrs.update({ 'readonly': 'readonly' })

 class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

def __init__(self, *args, **kwargs):
       super(UserProfileForm, self).__init__(*args, **kwargs)
       for field in self.fields:
              if field == 'latitude' or field == 'longitude':
                     self.fields[field].widget.attrs['readonly'] = 'readonly'