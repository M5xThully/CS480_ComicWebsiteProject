from django.http import HttpResponse
from django.shortcuts import render
from comicsite.models import Comic


def home(request):
    return render(request, 'frontpage.html')


def login(request):
    return render(request, 'loginpage.html')


def register(request):
    return render(request, 'registerpage.html')


def comic(request, pageid):

    comic = Comic.objects.filter(comicid=pageid)[0]

    context_dict = {'title': comic.comictitle,
                   'id': comic.comicid,
		    'cover': comic.comiccover,	
                    'author': comic.comicauthor,
                    'publisher': comic.comicpublisher,
                    'genre': comic.comicgenre,
                    'series': comic.comicseries,
                    'volume': comic.comicvolume,
                    'issue': comic.comicissue,
                    'rating': comic.comicrating,
                    'synopsis': comic.comicsynopsis,
                    'plot': comic.comicplot}

    # placeholder for a model which will provide the data
#   context_dict = {'title': "Poison-X",
#                   'id': '57895',
#                    'author': "Arthur Adams",
#                    'publisher': "Marvel",
#                    'genre': "Action",
#                    'series': "X-Men",
#                    'volume': "21",
#                    'issue': "21?",
#                    'rating': "4/5",
#                    'synopsis': "The X-Men fight the bad guys and probably don't die.",
#                    'plot': "The X-Men die"}

    return render(request, 'comicpage.html', context_dict)
