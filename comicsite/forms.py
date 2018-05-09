from django import forms
from django.forms import ModelForm
from comicsite.models import Account

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
