from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tagging.registry import register
from tagging.fields import TagField


class users(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blockage = models.BooleanField()
    Fio = models.CharField(max_length=200)
    University = models.CharField(max_length=200)
    Faculty = models.CharField(max_length=200)
    Speciality = models.CharField(max_length=200)
    images_counter = models.IntegerField(default=0)
    style = models.BooleanField(default=True)
    language = models.BooleanField(default=True)

    def __str__(self):
        return self.user


class compendium(models.Model):

    naming = models.CharField(max_length=200)
    short = models.CharField(max_length=200)
    speciality = models.CharField(max_length=200)
    containment = models.TextField()
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TagField()
    publication_date = models.DateTimeField(blank=True, null=True)
    change_date = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField(blank=True, default=0)

    def __str__(self):
        return self.naming


class compendium_rate(models.Model):
    rate = models.IntegerField()
    compendiums = models.ForeignKey(compendium, on_delete=models.CASCADE)
    correspondent = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (str(self.correspondent)+str(self.compendiums)+str(self.rate))


class coment(models.Model):
    containment = models.TextField()
    compendiums = models.ForeignKey(compendium, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.users


class coment_rate(models.Model):
    rate = models.BooleanField()
    comentarys = models.ForeignKey(coment, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.users











