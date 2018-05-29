# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class Comic(models.Model):
    comicid = models.AutoField(db_column='comicID', primary_key=True)  # Field name made lowercase.
    comictitle = models.CharField(db_column='comicTitle', max_length=50, blank=True,
                                  null=True)  # Field name made lowercase.
    comicplot = models.TextField(db_column='comicPlot', blank=True, null=True)  # Field name made lowercase.
    comicpublisher = models.CharField(db_column='comicPublisher', max_length=50, blank=True,
                                      null=True)  # Field name made lowercase.
    comicseries = models.CharField(db_column='comicSeries', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    comicvolume = models.IntegerField(db_column='comicVolume', blank=True, null=True)  # Field name made lowercase.
    comicissue = models.IntegerField(db_column='comicIssue', blank=True, null=True)  # Field name made lowercase.
    comicgenre = models.CharField(db_column='comicGenre', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    comicauthor = models.CharField(db_column='comicAuthor', max_length=100, blank=True,
                                   null=True)  # Field name made lowercase.
    comicsynopsis = models.TextField(db_column='comicSynopsis', blank=True, null=True)  # Field name made lowercase.
    comicrating = models.IntegerField(db_column='comicRating', blank=True, null=True)  # Field name made lowercase.
    comiccover = models.CharField(db_column='comicCover', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comic'


class ComicUserContent(models.Model):
    comic_comicid = models.ForeignKey(Comic, models.DO_NOTHING, db_column='comic_comicID')  # Field name made lowercase.
    post_postid = models.ForeignKey('Post', models.DO_NOTHING, db_column='post_postID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comic_user_content'


class Account(models.Model):
    accountid = models.AutoField(db_column='accountID', primary_key=True)  # Field name made lowercase.
    accountfirstname = models.TextField(db_column='accountFirstName', blank=True,
                                        null=True)  # Field name made lowercase.
    accountlastname = models.TextField(db_column='accountLastName', blank=True, null=True)  # Field name made lowercase.
    accountemail = models.EmailField(db_column='accountEmail')  # Field name made lowercase.
    accountusername = models.TextField(db_column='accountUserName')  # Field name made lowercase.
    accountpassword = models.TextField(db_column='accountPassword')  # Field name made lowercase.
    accountcity = models.TextField(db_column='accountCity', blank=True, null=True)  # Field name made lowercase.
    accountpicture = models.ImageField(db_column='accountPicture', upload_to='accounts', blank=True,
                                       null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'


class AccountPosts(models.Model):
    account_accountid = models.ForeignKey(Account, models.DO_NOTHING,
                                          db_column='account_accountID')  # Field name made lowercase.
    post_postid = models.ForeignKey('Post', models.DO_NOTHING, db_column='post_postID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account_posts'


class FavoriteComics(models.Model):
    account_accountid = models.ForeignKey(Account, models.DO_NOTHING,
                                          db_column='account_accountID')  # Field name made lowercase.
    comic_comicid = models.ForeignKey(Comic, models.DO_NOTHING,
                                      db_column='comic _comicID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'favorite_comics'


# class Post(models.Model):
#     postid = models.AutoField(db_column='postID', primary_key=True)  # Field name made lowercase.
#     postcontent = models.TextField(db_column='postContent', blank=True, null=True)  # Field name made lowercase.
#     postdate = models.DateField(db_column='postDate', blank=True, null=True)  # Field name made lowercase.
#     postrating = models.IntegerField(db_column='postRating', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'post'


class Comment(models.Model):
    # a integer field which uniquely identifies the comment
    commentid = models.AutoField(primary_key=True)
    # the id of the user who made this comment
    userid = models.IntegerField(null=False)
    # the id of the comic on which this comment was made
    comicid = models.IntegerField(null=False)
    # the actual comment itself
    text = models.TextField(blank=False)
    # the date of the comment
    date = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        managed = False
        db_table = 'comments'


class Rating(models.Model):
    # a integer field which uniquely identifies the rating
    ratingid = models.AutoField(primary_key=True)
    # the actual rating, from 1 to 5
    rating = models.IntegerField(null=False, blank=False)
    # the id of the user who made this rating
    userid = models.IntegerField(null=False)
    # the id of the comic being rated     
    comicid = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'ratings'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    # additional attributes
    userid = models.AutoField(primary_key=True)
    usercity = models.TextField(blank=True, null=True)
    profpic = models.ImageField(upload_to='profile_images', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_profile'


class Post(models.Model):
    # id of the post
    postid = models.AutoField(primary_key=True)
    # title of each post
    title = models.TextField(blank=False)
    # text body of the post
    text = models.TextField(blank=False)
    # image a user can upload with the post
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    # the user posting the post
    username = models.ForeignKey(User, on_delete=CASCADE)
    # date of the post
    date = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        managed = False
        db_table = 'posts'
