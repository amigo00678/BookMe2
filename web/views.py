# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from web.models import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FilesListView(ListView):
    model = File
    template_name = 'files/files_list.html'

    def get_context_data(self, **kwargs):
        context = super(FilesListView, self).get_context_data(**kwargs)
        context['files'] = [
            {'name': 'f1', 'created_at': datetime.now(), 'type': 3},
            {'name': 'f2', 'created_at': datetime.now(), 'type': 3},
            {'name': 'f3', 'created_at': datetime.now(), 'type': 3},
        ]
        context['list_url'] = reverse('files')
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)
        context = {}
        context['files'] = [
            {'name': 'f4', 'created_at': datetime.now(), 'type': 3},
            {'name': 'f5', 'created_at': datetime.now(), 'type': 3},
            {'name': 'f6', 'created_at': datetime.now(), 'type': 3},
        ]
        return render(request, 'files/_files_list.html', context)


class FoldersListView(ListView):
    model = File
    template_name = 'files/files_list.html'

    def get_context_data(self, **kwargs):
        context = super(FoldersListView, self).get_context_data(**kwargs)
        context['files'] = [
            {'name': 'f1'},
            {'name': 'f2'},
            {'name': 'f3'},
        ]
        return context


class VideoListView(ListView):
    model = File
    template_name = 'files/files_list.html'

    def get_context_data(self, **kwargs):
        context = super(VideoListView, self).get_context_data(**kwargs)
        context['files'] = [
            {'name': 'f1'},
            {'name': 'f2'},
            {'name': 'f3'},
        ]
        return context
