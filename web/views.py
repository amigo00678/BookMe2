# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.template import loader, Context
from django.http import JsonResponse

from web.models import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FilesListView(ListView):
    model = File
    template_name = 'files/files_list.html'

    def get_context_data(self, **kwargs):
        context = super(FilesListView, self).get_context_data(**kwargs)
        context['files'] = self.get_list({})
        context['list_url'] = reverse('files')
        return context

    def get_list(self, filter):
        objects = self.model.objects.all()
        if 'name' in filter:
            objects = objects.filter(name__icontains=filter['name'])
        if 'created_at' in filter:
            objects = objects.filter(created_at__lte=filter['created_at'][0])
            objects = objects.filter(created_at__gte=filter['created_at'][1])
        if 'type' in filter:
            objects = objects.filter(type=filter['type'])
        return objects

    def post(self, request, *args, **kwargs):
        context = {}
        context['files'] = self.get_list(request.POST)

        tpl = loader.get_template('files/_files_list.html')
        return JsonResponse({'reply': tpl.render(context)})


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
