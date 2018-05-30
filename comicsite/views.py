from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date

from comicsite.models import Comic
from comicsite.models import Account
from comicsite.models import Comment
from comicsite.models import Post
from comicsite.models import User, Rating
from comicsite.forms import CommentForm, LoginForm, RatingForm, PostForm
from comicsite.forms import UserForm
from comicsite.forms import UserProfileForm
from itertools import chain
# from comicsite.search import run_query
import logging
import re
import operator


def base(request):
    return render(request, 'base.html')


def home(request):
    comic = Comic.objects.filter(pk__in=[11, 2, 23, 4, 15, 6, 7, 18]).values()
    user.id = request.user.id

    post_list = Post.objects.all().order_by('-date')[:5]

    all_lists = list(chain(post_list, comic))
    
    for comic in comic:
        print(comic)
    return render(request, 'frontpage.html', {'all_lists': all_lists})

def postlist(request):
    post_list = Post.objects.all().values()
    return render(request, 'postlist.html', {'post_list': post_list})


def broke(request):
    post_listforbroke = Post.objects.all().values()
    return render(request, 'broke.html', {'post_listforbroke': post_listforbroke})


def loginpage(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        userx = form.login(request)
        if userx:
            login(request, userx)
            return redirect("/loggedin")
    else:
        form = LoginForm()
    return render(request, 'loginpage.html', {'login_form': form})


def loggedin(request):
    return render(request, 'loggedin.html')


def loggedout(request):
    logout(request)
    return render(request, 'loggedout.html')


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
                profile.userprofile.profpic = request.FILES['picture']

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


def createpost(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        print("Is valid?")
        if post_form.is_valid():
            print("Valid.")
            post = post_form.save(commit=False)
            post.user = User.objects.get(username=request.user.username)
            print("Got User")
            if 'picture' in request.FILES:
                post.image = request.FILES['picture']

            post.save()
            print("Redirecting.")
            return redirect("/postcreated")
    else:
        print("Failing.")
        post_form = PostForm()

    return render(request, 'createpost.html', {'post_form': post_form})


def postcreated(request):
    return render(request, 'postcreated.html')


def user(request, username):
    user = User.objects.get(username=username)
    return render(request, 'user.html', {'user': user})


def myprofile(request):
    return render(request, 'myprofile.html')


def post(request, pageid):
    post_obj = Post.objects.filter(postid=pageid)[0]
    context_dict = {
        'title': post_obj.title,
        'text': post_obj.text,
        'image': post_obj.image,
        'date': post_obj.date,
        'id': post_obj.postid,
        'user': post_obj.user
    }
    return render(request, 'postpage.html', context_dict)


def update_comic_rating(incomicid):
    # getting the comic object to be updated
    comic = Comic.objects.filter(comicid=incomicid)[0]

    # getting the ratings associated with the comic
    ratings = Rating.objects.filter(comicid=incomicid)

    counter = 0
    avg_rating = 0
    for rat in ratings:
        avg_rating += rat.rating
        counter += 1

    avg_rating /= counter

    comic.comicrating = avg_rating

    comic.save()


def comic(request, pageid):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.comicid = pageid
            comment.userid = request.user.id
            comment.save()
            return redirect(request.path)

        if rating_form.is_valid():
            rating = rating_form.save(commit=False)

            # deleting an previous ratings by this user about this comic (there should only be max one)
            ratings = Rating.objects.filter(userid=request.user.id, comicid=pageid)
            if ratings:
                for rat in ratings:
                    rat.delete()

            rating.comicid = pageid
            rating.userid = request.user.id
            rating.save()
            update_comic_rating(pageid)
            return redirect(request.path)

    # the comment form
    comment_form = CommentForm()

    # picking the comic whose id is equal to the pageid
    comic_obj = Comic.objects.filter(comicid=pageid)[0]

    # getting the top five most recent comments for the comic
    comments = Comment.objects.filter(comicid=pageid).order_by('-date')[:5]

    # going through each comic and constructing a dictionary to be used in the template
    comment_list = []
    for com in comments:
        user_object = User.objects.filter(id=com.userid)[0]

        link_str = "/user/" + user_object.username

        # adding a dictionary the list to be used in the template
        comment_list.append({
            'link': link_str,
            'user': user_object.username,
            'date': com.date,
            'comment_text': com.text
        })

    context_dict = {'title': comic_obj.comictitle,
                    'id': comic_obj.comicid,
                    'author': comic_obj.comicauthor,
                    'publisher': comic_obj.comicpublisher,
                    'genre': comic_obj.comicgenre,
                    'series': comic_obj.comicseries,
                    'volume': comic_obj.comicvolume,
                    'issue': comic_obj.comicissue,
                    'rating': comic_obj.comicrating,
                    'ratingform': RatingForm(),
                    'synopsis': comic_obj.comicsynopsis,
                    'plot': comic_obj.comicplot,
                    'cover': comic_obj.comiccover,
                    'commentform': comment_form,
                    'comments': comment_list}

    # getting the rating made by this user for the comic, if it exists
    rating_list = Rating.objects.filter(comicid=pageid, userid=request.user.id)
    if rating_list:
        user_rating = rating_list[0].rating
        context_dict['user_rating'] = user_rating

    return render(request, 'comicpage.html', context_dict)


def comiclist(request, sortby=None):
    comic_list = Comic.objects.all().values()

    if sortby is not None:
        comic_list = Comic.objects.filter(comictitle__startswith=sortby)

    return render(request, 'comiclist.html', {'comic_list': comic_list})


def account(request, userid):
    account_obj = Account.objects.filter(accountid=userid)[0]

    context_dict = {'id': account_obj.accountid,
                    'firstname': account_obj.accountfirstname,
                    'lastname': account_obj.accountlastname,
                    'email': account_obj.accountemail,
                    'username': account_obj.accountusername,
                    'password': account_obj.accountpassword,
                    'city': account_obj.accountcity,
                    'followid': account_obj.followingid,
                    'picture': account_obj.picture}

    return render(request, 'user.html', context_dict)


def broke(request):
    return render(request, 'broke.html')
'''
    def search(request):
        result_list = []
        if 'q' in request.GET and request.GET['q']:
            q=request.GET['q']
            comic_list = Comic.objects.filter(comic_list__icontains =q)
        return render(request, 'searchpage.html', {'comic_list':result_list})

    else:
        return HttpResponse('Please submit a search term.')

>>>>>>> d3abdd607d85156354b9d19a0c4e8b6ce15fecd2

def search(request):
    result_list = []
    result_list.append("a")
    result_list.append("b")
    #if 'q' in request.GET and request.GET['q']:
       # q=request.GET['q']
       # comic_list = Comic.objects.filter(comictitle__icontains =q)
    return render(request, 'searchpage.html', {'result_list':result_list})
'''
