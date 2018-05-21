from django import forms
from django.forms import ModelForm
from comicsite.models import Account
from comicsite.models import User
from comicsite.models import UserProfile
from comicsite.models import Comment
import logging


class AccountForm(ModelForm):
    accountfirstname = forms.CharField(required=False)
    accountlastname = forms.CharField(required=False)
    accountemail = forms.EmailInput()
    accountusername = forms.CharField()
    accountpassword = forms.CharField()
    accountcity = forms.CharField(required=False)

    class Meta:
        model = Account
        fields = ['accountfirstname', 'accountlastname', 'accountemail', 'accountusername', 'accountpassword',
                  'accountcity']
        labels = {
            'accountfirstname': ('First Name'),
            'accountlastname': ('Last Name'),
            'accountemail': ('Email'),
            'accountusername': ('Username'),
            'accountpassword': ('Password'),
            'accountcity': ('City'),
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['accountfirstname'].label = "First Name"
        self.fields['accountlastname'].label = "Last Name"
        self.fields['accountemail'].label = "Email"
        self.fields['accountusername'].label = "Username"
        self.fields['accountpassword'].label = "Password"
        self.fields['accountcity'].label = "City"
        self.fields['accountfirstname'].widget.attrs.update({'class': "form-control"})
        self.fields['accountlastname'].widget.attrs.update({'class': "form-control"})
        self.fields['accountemail'].widget.attrs.update({'class': "form-control"})
        self.fields['accountusername'].widget.attrs.update({'class': "form-control"})
        self.fields['accountpassword'].widget.attrs.update({'class': "form-control"})
        self.fields['accountcity'].widget.attrs.update({'class': "form-control"})

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'username'
        }
    ))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'first name'
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'last name'
        }
    ))

    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'email'
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': "form-control",
            'placeholder': 'password'
        }
    ))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    
    usercity = forms.CharField(required=False)
    profpic = forms.ImageField(required=False)

    usercity = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': "form-control",
            'placeholder': 'city'
        }
    ))

    class Meta:
        model = UserProfile
        fields = ('usercity', 'profpic')


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.comicid = kwargs.pop('comicid')
        super(CommentForm, self).__init__(*args, **kwargs)

#    def __setpageid__(self, in_pageid):
#        self.comicid = in_pageid

    comicid = forms.IntegerField();
    userid = forms.IntegerField()
    text = forms.CharField(max_length=128, help_text="Enter your comment: ")

#    logger = logging.getLogger('django')
#    logger.debug("comicid:" + str(comicid))

    class Meta:
        model = Comment
        fields = ('text', 'userid', 'comicid')
