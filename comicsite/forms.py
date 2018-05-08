from django.forms import ModelForm
from comicsite.models import Account

class AccountForm(ModelForm):
	
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
