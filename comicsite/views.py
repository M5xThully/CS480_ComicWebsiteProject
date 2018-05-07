from django.http import HttpResponse
from django.shortcuts import render
from comicsite.models import Comic
from comicsite.models import Account


def home(request):
    return render(request, 'frontpage.html')


def login(request):
    return render(request, 'loginpage.html')


def register(request):
    return render(request, 'registerpage.html')

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
                    'plot': comic.comicplot}

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

def add_account(request):
    form = AccountForm()

    if request.methond = 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=TRUE)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'registerpage.html', {'form': form})
