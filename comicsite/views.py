from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from comicsite.models import Comic
from comicsite.models import Account
from comicsite.models import Comment
from comicsite.models import UserProfile
from comicsite.models import User
from comicsite.forms import CommentForm, LoginForm
from comicsite.forms import UserForm
from comicsite.forms import UserProfileForm
from django.urls import reverse
import logging
from comicsite.search import run_query
from django.contrib import messages


def base(request):
    return render(request, 'base.html')


def home(request):    
    
    comic = Comic.objects.filter(pk__in=[1,2,13,4,15,6,7,18]).values()

    user.id = request.user.id

    return render(request, 'frontpage.html', {'comic':comic})


def loginpage(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        userx = form.login(request)
        if userx:
            login(request, userx)
            return redirect("/loggedin")
    else:
        form = LoginForm()
    return render(request, 'loginpage.html', {'login_form': form })


def loggedin(request):
    return render(request, 'loggedin.html')


def registered(request):
    return render(request, 'registered.html')


def register(request):
    isregistered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.profpic = request.FILES['profpic']

            profile.save()

            isregistered = True

            return redirect('/registered')

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'registerpage.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def user(request):
    return render(request, 'user.html')


def comic(request, pageid):
    # the comment form
    commentform = CommentForm()

    # picking the comic whose id is equal to the pageid
    comic = Comic.objects.filter(comicid=pageid)[0]

    # getting the top five most recent comments for the comic
    comments = Comment.objects.filter(comicid=pageid).order_by('-date')[:5]

    # going through each comic and constructing a dictionary to be used in the template
    comment_list = []
    for com in comments:
        user_object = User.objects.filter(id=com.userid)[0]

        # adding a dictionary the list to be used in the template
        comment_list.append({
            'user': user_object.username,
            'date': com.date,
            'comment_text': com.text
        })

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
                    'commentform': commentform,
                    'comments': comment_list}

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

#return render(request, 'user.html')
def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'search.html', {'result_list': result_list})
