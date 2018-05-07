
m django.forms import ModelForm
from comicsite.models import Account

class AccountForm(ModelForm):
	accountfirstname = form.CharField(label='First Name')
	accountlastname = form.CharField(label='Last Name')
	accountemail = form.CharField(label='Email')
	accountusername = form.CharField(label='Username')
	accountpassword = form.CharField(label='Password', widget=forms.HiddenInput())
	accountcity = form.CharField(label='City')

	class Meta:
		model = Account
		fields = ['accountfirstname', 'accountlastname', 'accountemail', 'accountusername', 'accountpassword', 'accountcity']
