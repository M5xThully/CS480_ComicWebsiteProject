from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from comicsite.models import Comic
from comicsite.models import Account
from comicsite.forms import AccountForm

def home(request):
    return render(request, 'frontpage.html')


def login(request):
    return render(request, 'loginpage.html')


def registered(request):
    return render(request, 'registered.html')


def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_entry = form.save()
            return redirect('/home')
    else:
        form = AccountForm()

    return render(request, 'registerpage.html', {'form':form})

def user(request):
    return render(request, 'user.html')


def comic(request, pageid):

    comic = Comic.objects.filter(comicid=pageid)[0]

    context_dict = {'title': comic.comictitle,
                    'id': comic.comicid,
                    'author': comic.comicauthor,
                    'publisher': comic.comicpublisher,
                    'genre': comic.comicgenre,
                    'series': comic.comicseries,
                    'volume': comic.comicvolume,
                    'issue': comic.comicissue,
                    'rating': comic.comicrating,
                    'synopsis': comic.comicsynopsis,
                    'plot': comic.comicplot,
		    'cover': comic.comiccover}
    return render(request, 'comicpage.html', context_dict)


def account(request, userid):

    account = Account.objects.filter(accountid=userid)[0]

    context_dict = {'id': account.accountid,
                    'firstname': account.accountfirstname,
                    'lastname': account.accountlastname,
                    'email': account.accountemail,
                    'username': account.accountusername,
                    'password': account.accountpassword,
                    'city': account.accountcity,
                    'followid': account.followingid,
                    'picture': account.accountpicture}

    return render(request, 'user.html', context_dict)
#    return render(request, 'user.html')

