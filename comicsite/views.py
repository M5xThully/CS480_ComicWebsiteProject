from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from comicsite.models import Comic
from comicsite.models import Account
from comicsite.forms import CommentForm

def home(request):
    return render(request, 'frontpage.html')


def login(request):
    return render(request, 'loginpage.html')


def registered(request):
    return render(request, 'registered.html')

'''
def register(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            new_entry = form.save()
            return redirect('/registered')
    else:
        form = AccountForm()

    return render(request, 'registerpage.html', {'form':form})
'''
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            profile.save()
            registered = True
            
            return redirect('/registered')
            
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registerpage.html', {'form':UserForm}, {'form':UserProfileForm})



def user(request):
    return render(request, 'user.html')


def comic(request, pageid):

    # the comment form
    commentform = CommentForm()

    # picking the comic whose id is equal to the pageid
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
                    'cover': comic.comiccover,
                    'rating': comic.comicrating,
                    'commentform': commentform}

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

