# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage

from web.models import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ObjectsListView(ListView):
    model = File
    template_name = 'files_list.html'
    list_template = '_files_list.html'
    base_url = 'files'

    def get_context_data(self, **kwargs):
        context = super(ObjectsListView, self).get_context_data(**kwargs)
        objects, page = self.get_objects()
        context['objects'] = objects
        context['page'] = page
        context['list_url'] = reverse(self.base_url)
        return context

    def get_objects(self, filter={}, pp=10, page=1):
        objects = self.get_list(filter)
        return self.get_pages(objects, pp, page)

    def get_pages(self, objects, pp, page):
        pagin = Paginator(objects, pp)
        try:
            page = pagin.page(page)
        except EmptyPage:
            page = pagin.page(pagin.num_pages)
        return page.object_list, page

    def get_list(self, filter):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        context = {}
        objects, page = self.get_objects(
            request.POST, request.POST.get('pp', 10), request.POST.get('page', 1))
        context['objects'] = objects
        context['page'] = page
        return JsonResponse({
            'reply': render_to_string(self.list_template, context),
            'pagin': render_to_string('common/_pagin.html', context)
        })


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FilesListView(ObjectsListView):
    model = File
    template_name = 'files_list.html'
    list_template = '_files_list.html'
    base_url = 'files'

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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FoldersListView(ObjectsListView):
    model = Folder
    template_name = 'folders_list.html'
    list_template = '_folders_list.html'
    base_url = 'folders'

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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class VideoListView(ObjectsListView):
    model = Folder
    template_name = 'folders_list.html'
    list_template = '_folders_list.html'
    base_url = 'folders'

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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AudioListView(ObjectsListView):
    model = Folder
    template_name = 'folders_list.html'
    list_template = '_folders_list.html'
    base_url = 'folders'

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
