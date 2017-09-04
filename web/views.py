# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.views.generic import ListView, TemplateView

from web.models import *


class FilesListView(ListView):
    model = File
    template_name = 'files/files_list.html'

    def get_context_data(self, **kwargs):
        context = super(FilesListView, self).get_context_data(**kwargs)
        context['files'] = [
            {'name': 'f1'},
            {'name': 'f2'},
            {'name': 'f3'},
        ]
        return context


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
