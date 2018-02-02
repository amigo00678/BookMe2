# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
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

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class File(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Folder')
    type = models.IntegerField(choices=FILE_TYPE_E, default=1)


class Folder(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('Folder', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

