
from django import forms
from . import models

class AccountForm(forms.ModelForm):
	class Meta:
		model = models.Account
		fields = ['accountfirstname', 'accountlastname', 'accountemail', 'accountusername', 'accountpassword', 'accountcity']
