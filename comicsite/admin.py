from django.contrib import admin
from comicsite.models import Comic
from comicsite.models import ComicUserContent
from comicsite.models import Account
from comicsite.models import AccountPosts
from comicsite.models import FavoriteComics
from comicsite.models import Following
from comicsite.models import Post

admin.site.register(Comic)
admin.site.register(ComicUserContent)
admin.site.register(Account)
admin.site.register(AccountPosts)
admin.site.register(FavoriteComics)
admin.site.register(Following)
admin.site.register(Post)