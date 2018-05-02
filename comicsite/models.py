# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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

    class Meta:
        managed = False
        db_table = 'comic'
