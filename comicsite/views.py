from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from comicsite.models import Comic, Post
from comicsite.models import Account
from comicsite.models import Comment
from comicsite.models import User
from comicsite.forms import CommentForm, LoginForm#, PostForm
from comicsite.forms import UserForm
from comicsite.forms import UserProfileForm
#from comicsite.search import run_query
import logging
import re
import operator


def base(request):
    return render(request, 'base.html')


def home(request):
    comic = Comic.objects.filter(pk__in=[11, 2, 23, 4, 15, 6, 7, 18]).values()
    user.id = request.user.id

    return render(request, 'frontpage.html', {'comic': comic})


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
                profile.userprofile.profpic = request.FILES['profpic']

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


def user(request, username):
    user = User.objects.get(username=username)
    return render(request, 'user.html', {'user': user})


def myprofile(request):
    return render(request, 'myprofile.html')


def createpost(request):
    #PASS USERID TO CREATE POST!
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save()
            post.save()
    else:
        post_form = PostForm()

    return render(request, 'createpost.html', {'post_form': post_form})


def post(request, pageid):
    post_obj = Post.objects.filter(postid = pageid)[0]
    context_dict = {
        'title': post_obj.title,
        'text': post_obj.text,
        'image': post_obj.image,
        'date': post_obj.date,
        'id': post_obj.postid,
        'user': post_obj.userid
    }
    return render(request, 'post.html', context_dict)


def comic(request, pageid):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            logger = logging.getLogger('django')
            logger.debug("userid:" + str(comment.userid) + " comicid:" + str(comment.comicid))
            comment.comicid = pageid
            comment.userid = request.user.id
            comment.save()
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

        link_str = "/" + user_object.username
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
                    'synopsis': comic_obj.comicsynopsis,
                    'plot': comic_obj.comicplot,
                    'cover': comic_obj.comiccover,
                    'commentform': comment_form,
                    'comments': comment_list}

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

def article(request):
    return render(request,'articlepage.html')

'''
def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        print(query)
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'searchpage.html', {'result_list': result_list})

class BasicSearchListView(BasicListView):
    paginate_by = 10

    def get_queryset(self):
        result = super(BasicSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Comic(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Comic(content__icontains=q) for q in query_list))
            )

        return result
'''
