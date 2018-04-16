# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string
import os
from datetime import datetime

from django.db import models
from django.db.models import Avg

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from web.constants import *


class AuthManager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        user = self.model(email=self.normalize_email(email), first_name=first_name,
            last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        return self.create_user(email, password, first_name, last_name, is_admin=True, **extra_fields)


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    objects = AuthManager()

    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=USER_TYPE_E, default=2)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def public_name(self):
        return "%s" % (self.first_name)


class File(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Folder', null=True, blank=True)
    type = models.IntegerField(choices=FILE_TYPE_E, default=1)

    top_content = models.TextField(null=True, blank=True)
    middle_content = models.TextField(null=True, blank=True)
    bottom_content = models.TextField(null=True, blank=True)

    top_slider = models.ForeignKey('ImageSlider', null=True, blank=True, related_name='top_slider')
    bottom_slider = models.ForeignKey('ImageSlider', null=True, blank=True, related_name='bottom_slider')

    features = models.ManyToManyField('Feature')

    @property
    def latest_reviews(self):
        return self.review_set.all()[:3]

    @property
    def rate(self):
        return Review.objects.filter(item=self).aggregate(Avg('rate')).get('rate__avg')

    @property
    def reviews_count(self):
        return Review.objects.filter(item=self).count()


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField(default=0)
    user = models.ForeignKey('User')
    item = models.ForeignKey('File')
    pros = models.TextField(null=True, blank=True)
    cons = models.TextField(null=True, blank=True)


def feature_upload_path(instance, filename):
    rnd_part = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    path = 'uploads/features/feature_{0}{1}'.format(rnd_part, filename[-4:])

    try:
        os.makedirs(path)
    except Exception as e:
        pass
    return path


class Feature(models.Model):
    name = models.CharField(max_length=200)
    value = models.BooleanField(default=True)
    key = models.CharField(max_length=10)
    image = models.FileField(null=True, blank=True, upload_to=feature_upload_path)

    def __unicode__(self):
        return "%s" % (self.name)


class ImageSlider(models.Model):
    images = models.ManyToManyField('SliderImage', blank=True)


def image_upload_path(instance, filename):
    now = datetime.now()
    rnd_part = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

    path = 'uploads/{0}/{1}/{2}/img_{3}{4}'.format(
        now.year, now.month, now.day, rnd_part, filename[-4:])

    try:
        os.makedirs(path)
    except Exception as e:
        pass

    return path


class SliderImage(models.Model):
    image = models.FileField(upload_to=image_upload_path)


class Folder(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('Folder', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

