from django import forms
from django.forms import ModelForm
from comicsite.models import User
from comicsite.models import UserProfile
from comicsite.models import Comment


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
    #        def __init__(self, inComicid):
    #                self.comicid = inComicid

    comicid = forms.IntegerField();
    userid = forms.IntegerField()
    text = forms.CharField(max_length=128, help_text="Enter your comment: ")

    class Meta:
        model = Comment
        fields = ('text',)
