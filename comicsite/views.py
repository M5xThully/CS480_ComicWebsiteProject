from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views.generic import TemplateView

from comicsite.models import Comic
from comicsite.models import Comment
from comicsite.models import Post
from comicsite.models import User, Follow, Rating
from comicsite.models import FavoriteComics
from comicsite.forms import CommentForm, LoginForm, PostForm
from comicsite.forms import UserForm
from comicsite.forms import RatingForm
from comicsite.forms import UserProfileForm
from comicsite.forms import FavComicForm
from comicsite.forms import FollowForm

from itertools import chain
import logging
import re
import operator


def base(request):
    return render(request, 'base.html')


def home(request):
    user.id = request.user.id
    
    comic = Comic.objects.filter(pk__in=[102, 104, 21, 24, 18]).values()
    recent_comic = Comic.objects.all().order_by('-comicid')[:5]
    post_list = Post.objects.all().order_by('-date')[:5]

    context_dict = { 'comic':comic,
                     'post_list':post_list,
                     'recent_comic':recent_comic}

    return render(request, 'frontpage.html', context_dict)


def post(request, pageid):
    post_obj = Post.objects.filter(postid=pageid)[0]
    context_dict = {
        'title': post_obj.title,
        'text': post_obj.text,
        'image': post_obj.image,
        'date': post_obj.date,
        'id': post_obj.postid,
        'user': post_obj.user.username
    }
    return render(request, 'postpage.html', context_dict)


def postlist(request):
    post_list = Post.objects.all().values()
    return render(request, 'postlist.html', {'post_list': post_list})


def newsfeed(request):
    post_list = Post.objects.all().order_by('-date')[:5]
    return render(request, 'newsfeed.html', {'post_list': post_list})


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
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

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
        post_form = PostForm(request.POST, request.FILES)
        print("Is valid?")
        if post_form.is_valid():
            print("Valid.")
            post = post_form.save(commit=False)
            post.user = User.objects.get(username=request.user.username)
            print("Got User")
            post.save()

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
    if request.method == 'POST':
        follow_form = FollowForm(request.POST)

        if follow_form.is_valid():
            following = follow_form.save(commit=False)

            followed = Follow.objects.filter(user=request.user, following=username)

            if followed:
                followed.delete()
            else:
                following.user = request.user
                following.following = username
                following.save()
            return redirect(request.path)

    follow_form = FollowForm()
    
    user_profile = User.objects.get(username=username)
    fav_list = FavoriteComics.objects.filter(userid=user_profile).values('comicid')
    fav_comic_list = Comic.objects.filter(comicid__in=fav_list)
    follow_list = Follow.objects.filter(user=user_profile) 
    is_followed = None

    if request.user.is_active:
        followed = Follow.objects.filter(user=request.user)
        is_followed = followed.filter(following=user_profile)

    context_dict = {'username': user_profile.username,
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'email': user_profile.email,
                    'profpic' : user_profile.userprofile.profpic,
                    'fav_list': fav_comic_list,
                    'follow_list': follow_list,
                    'follow_form': follow_form,
                    'is_followed': is_followed}

    return render(request, 'user.html', context_dict)


def myprofile(request):
    fav_list = FavoriteComics.objects.filter(userid = request.user).values('comicid')
    fav_comic_list = Comic.objects.filter(comicid__in=fav_list)
    follow_list = Follow.objects.filter(user = request.user)

    # timeline
    user_posts = Post.objects.filter(user = request.user)
    following_ids = Follow.objects.filter(user = request.user).values('following')
    following = User.objects.filter(username__in = following_ids)
    following_posts = Post.objects.filter(user__in = following)
    following_comment = Comment.objects.filter(userid__in = following) 
    combined_posts = user_posts | following_posts
    timeline_posts = combined_posts.distinct().order_by('-date')[:10]

    context_dict={'fav_list':fav_comic_list,
                  'follow_list':follow_list,
                  'timeline_posts':timeline_posts} 

    return render(request, 'myprofile.html', context_dict)


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
        fav_comic_form = FavComicForm(request.POST)
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

        if fav_comic_form.is_valid():
            fav_comic = fav_comic_form.save(commit=False)

            is_fav = FavoriteComics.objects.filter(userid=request.user, comicid=pageid)

            if is_fav:
                is_fav.delete()
            else:
                fav_comic.userid = request.user
                fav_comic.comicid = pageid
                fav_comic.save()

            return redirect(request.path)

    fav_comic_form = FavComicForm()
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
                    'comments': comment_list,
                    'fav_comic_form': fav_comic_form}

    # getting the rating made by this user for the comic, if it exists
    rating_list = Rating.objects.filter(comicid=pageid, userid=request.user.id)
    if rating_list:
        user_rating = rating_list[0].rating
        context_dict['user_rating'] = user_rating

    if request.user.is_active:
        fav_comic = FavoriteComics.objects.filter(userid=request.user)
        is_fav = fav_comic.filter(comicid=pageid)
        context_dict['is_fav'] = is_fav

    return render(request, 'comicpage.html', context_dict)


def comiclist(request, sortby=None):
    comic_list = Comic.objects.all().values()

    if sortby is not None:
        comic_list = Comic.objects.filter(comictitle__startswith=sortby)

    return render(request, 'comiclist.html', {'comic_list': comic_list})


def broke(request):
    return render(request, 'broke.html')


def searchpage(request):
    q = request.GET['q']
    result_listComicTitle = []
    result_listAuthor = []
    result_listUser = []
    if (q != ""):
        result_listComicTitle = Comic.objects.filter(comictitle__icontains=q)
        result_listAuthor = Comic.objects.filter(comicauthor__icontains=q)
        result_listUser = User.objects.filter(username__icontains=q)
    return render(request, 'searchpage.html',
                  {'result_listComicTitle': result_listComicTitle, 'result_listAuthor': result_listAuthor,
                   'result_listUser': result_listUser})
