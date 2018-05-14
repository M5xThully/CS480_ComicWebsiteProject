from django import forms
from django.forms import ModelForm
from comicsite.models import Account
from django.contrib.auth.models import User
from comicsite.models import UserProfile
from comicsite.models import Comment

class AccountForm(ModelForm):

        accountfirstname = forms.CharField(required=False)
        accountlastname = forms.CharField(required=False)
        accountemail = forms.EmailInput()
        accountusername = forms.CharField()
        accountpassword = forms.CharField()
        accountcity = forms.CharField(required=False)

        class Meta:
                model = Account
                fields = ['accountfirstname', 'accountlastname', 'accountemail', 'accountusername', 'accountpassword', 'accountcity']
                labels = {
                        'accountfirstname':('First Name'),
                        'accountlastname':('Last Name'),
                        'accountemail':('Email'),
                        'accountusername':('Username'),
                        'accountpassword':('Password'),
                        'accountcity':('City'),
                }

        def __init__(self, *args, **kwargs):
                super(AccountForm, self).__init__(*args, **kwargs)
                self.fields['accountfirstname'].label = "First Name"
                self.fields['accountlastname'].label = "Last Name"
                self.fields['accountemail'].label = "Email"
                self.fields['accountusername'].label = "Username"
                self.fields['accountpassword'].label = "Password"
                self.fields['accountcity'].label = "City"
                self.fields['accountfirstname'].widget.attrs.update({'class' : "form-control"})
                self.fields['accountlastname'].widget.attrs.update({'class' : "form-control"})
                self.fields['accountemail'].widget.attrs.update({'class' : "form-control"})
                self.fields['accountusername'].widget.attrs.update({'class' : "form-control"})
                self.fields['accountpassword'].widget.attrs.update({'class' : "form-control"})
                self.fields['accountcity'].widget.attrs.update({'class' : "form-control"})
                
                
                
class UserForm(forms.ModelForm):
            password = forms.CharField(widget=forms.PasswordInput())

            class Meta:
                model = User
                fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
            class Meta:
                model = UserProfile
                fields = ('userid', 'usercity', 'followingid', 'profpic')


class CommentForm(forms.ModelForm):
#        def __init__(self, inComicid):
#                self.comicid = inComicid

        comicid = forms.IntegerField();
        userid = forms.IntegerField()
        text = forms.CharField(max_length=128, help_text="Enter your comment: ")

        class Meta:
                model = Comment
                fields = ('text',)

