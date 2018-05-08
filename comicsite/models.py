# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.forms import ModelForm


class Comic(models.Model):
    comicid = models.IntegerField(db_column='comicID', primary_key=True)  # Field name made lowercase.
    comictitle = models.CharField(db_column='comicTitle', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comicplot = models.TextField(db_column='comicPlot', blank=True, null=True)  # Field name made lowercase.
    comicpublisher = models.CharField(db_column='comicPublisher', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comicseries = models.CharField(db_column='comicSeries', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comicvolume = models.IntegerField(db_column='comicVolume', blank=True, null=True)  # Field name made lowercase.
    comicissue = models.IntegerField(db_column='comicIssue', blank=True, null=True)  # Field name made lowercase.
    comicgenre = models.CharField(db_column='comicGenre', max_length=45, blank=True, null=True)  # Field name made lowercase.
    comicauthor = models.CharField(db_column='comicAuthor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    comicsynopsis = models.TextField(db_column='comicSynopsis', blank=True, null=True)  # Field name made lowercase.
    comicrating = models.IntegerField(db_column='comicRating', blank=True, null=True)  # Field name made lowercase.
    comiccover = models.CharField(db_column='comicCover', max_length=20, blank=True, null=True)

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
    accountid = models.AutoField(db_column='accountID', primary_key=True)  #Field name made lowercase.
    accountfirstname = models.TextField(db_column='accountFirstName', blank=True, null=True)  # Field name made lowercase.
    accountlastname = models.TextField(db_column='accountLastName', blank=True, null=True)  # Field name made lowercase.
    accountemail = models.TextField(db_column='accountEmail')  #Field name made lowercase.
    accountusername = models.TextField(db_column='accountUserName')  # Field name made lowercase.
    accountpassword = models.TextField(db_column='accountPassword')  # Field name made lowercase.
    accountcity = models.TextField(db_column='accountCity', blank=True, null=True)  # Field name made lowercase.
    followingid = models.ForeignKey('Following', models.DO_NOTHING, db_column='followingID', blank=True, null=True)  # Field name made lowercase.
    accountpicture = models.TextField(db_column='accountPicture', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account'

class AccountPosts(models.Model):
    account_accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column= 'account_accountID')  # Field name made lowercase.
    post_postid = models.ForeignKey('Post', models.DO_NOTHING, db_column='post_postID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'account_posts'
class FavoriteComics(models.Model):
    account_accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='account_accountID')  # Field name made lowercase.
    comic_comicid = models.ForeignKey(Comic, models.DO_NOTHING, db_column='comic _comicID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'favorite_comics'

class Following(models.Model):
    followingid = models.IntegerField(db_column='followingID', primary_key=True)# Field name made lowercase.
    accountid = models.ForeignKey(Account, models.DO_NOTHING, db_column='accountID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'following'

class Post(models.Model):
    postid = models.IntegerField(db_column='postID', primary_key=True)  # Field name made lowercase.
    postcontent = models.TextField(db_column='postContent', blank=True, null=True)  # Field name made lowercase.
    postdate = models.DateField(db_column='postDate', blank=True, null=True)  #Field name made lowercase.
    postrating = models.IntegerField(db_column='postRating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'post'
