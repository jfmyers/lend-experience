from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django import forms

class UserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Make the following required fields when a new user signs up.
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    
    class Meta:
        model = User
        fields = ('email','password','first_name','last_name')