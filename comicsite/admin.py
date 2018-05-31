from django.contrib import admin
from comicsite.models import Comic
from comicsite.models import Post
from comicsite.models import Comment
from comicsite.models import Rating
from comicsite.models import UserProfile

admin.site.register(Comic)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(UserProfile)
