# -*- coding: utf-8 -*-

from django.core.validators import validate_email
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import AuthenticationForm

from web.models import *


class AuthForm(AuthenticationForm):

    def clean(self):
        cd = super(AuthForm, self).clean()
        email = cd.get('username', None)
        if email:
            validate_email(email)


class FileEditForm(ModelForm):
    class Meta:
        model = File
        fields = ['name', 'type', 'content']

        widgets = {
            'content': Textarea(attrs={'class': 'tinymce'}),
        }
