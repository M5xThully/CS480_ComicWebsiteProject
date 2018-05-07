
from django import forms
from comicsite.models import Account

class AccountForm(forms.ModelForm):
	class Meta:
		model = Account
		fields = ['accountfirstname', 'accountlastname', 'accountemail', 'accountusername', 'accountpassword', 'accountcity']
