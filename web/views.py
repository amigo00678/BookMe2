# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

from web.models import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FilesListView(ListView):
    model = File
    template_name = 'files/files_list.html'

    def get_context_data(self, **kwargs):
        context = super(FilesListView, self).get_context_data(**kwargs)
        objects, page = self.get_objects()
        context['files'] = objects
        context['page'] = page
        context['list_url'] = reverse('files')
        return context

    def get_objects(self, filter={}, pp=10, page=1):
        objects = self.get_list(filter)
        return self.get_pages(objects, pp, page)

    def get_pages(self, objects, pp, page):
        #TODO: move to base class
        pagin = Paginator(objects, pp)
        try:
            page = pagin.page(page)
        except EmptyPage:
            page = pagin.page(pagin.num_pages)
        return page.object_list, page

    def get_list(self, filter):
        objects = self.model.objects.all()
        if 'name' in filter:
            objects = objects.filter(name__icontains=filter['name'])
        if 'created_at' in filter:
            objects = objects.filter(created_at__lte=filter['created_at'][0])
            objects = objects.filter(created_at__gte=filter['created_at'][1])
        if 'type' in filter and int(filter['type']):
            objects = objects.filter(type=filter['type'])
        if 'sort' in filter and filter['sort']:
            sort = filter['sort']
            sort_map = {
                'created': 'created_at'
            }
            sort = sort_map.get(sort, sort)
            if 'order' in filter and filter['order'] == 'desc':
                sort = '-' + sort
            objects = objects.order_by(sort)
        return objects

    def post(self, request, *args, **kwargs):
        context = {}
        objects, page = self.get_objects(request.POST, request.POST.get('pp', 10), request.POST.get('page', 1))
        context['files'] = objects
        context['page'] = page
        return JsonResponse({
            'reply': render_to_string('files/_files_list.html', context),
            'pagin': render_to_string('_pagin.html', context)
        })


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
