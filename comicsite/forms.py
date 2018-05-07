
from django import forms
from comicsite.models import Account

class AccountForm(forms.ModelForm):
	accountfirstname = form.CharField(label='First Name')
	accountlastname = form.CharField(label='Last Name')
	accountemail
	accountusername
	accountpassword
	accountcity
