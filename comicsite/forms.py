
m django.forms import ModelForm
from comicsite.models import Account

<<<<<<< HEAD
class AccountForm(forms.ModelForm):
	accountfirstname = form.CharField(label='First Name')
	accountlastname = form.CharField(label='Last Name')
	accountemail
	accountusername
	accountpassword
	accountcity
=======
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
>>>>>>> 4db3e1b271eb31b666886c2e93adc6f1a37f2bcd
