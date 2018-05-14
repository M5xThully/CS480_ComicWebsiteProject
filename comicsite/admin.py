from django.contrib import admin
from comicsite.models import Comic
from comicsite.models import ComicUserContent
from comicsite.models import Account
from comicsite.models import AccountPosts
from comicsite.models import FavoriteComics
from comicsite.models import Post
from comicsite.models import Comment
from comicsite.models import Rating
from comicsite.models import UserProfile

admin.site.register(Comic)
admin.site.register(ComicUserContent)
admin.site.register(Account)
admin.site.register(AccountPosts)
admin.site.register(FavoriteComics)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(UserProfile)
