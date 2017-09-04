# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from web.constants import *

from django.db import models


class File(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('Folder')
    type = models.IntegerField(choices=FileType.choices(), default=FileType.TXT)


class Folder(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('Folder', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

