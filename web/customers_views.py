# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin

from web.models import *
from web.forms import *


@method_decorator(ensure_csrf_cookie, name='dispatch')
class MainListView(ListView):
    model = File
    template_name = 'customers/files_list.html'
    list_template = 'customers/_files_list.html'
    base_url = 'fe_home'

    def get_context_data(self, **kwargs):
        context = super(MainListView, self).get_context_data(**kwargs)
        page = int(self.kwargs.get('page', 1))
        objects, page = self.get_objects(filter={}, pp=12, page=page)
        context['objects'] = objects
        context['page'] = page
        context['list_url'] = reverse(self.base_url)
        return context

    def get_objects(self, filter={}, pp=12, page=1):
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
            request.POST, request.POST.get('pp', 12), request.POST.get('page', 1))
        context['objects'] = objects
        context['page'] = page
        context['list_url'] = reverse(self.base_url)
        return JsonResponse({
            'reply': render_to_string(self.list_template, context),
            'pagin': render_to_string('customers/_pagin.html', context)
        })

    def format_dates(self, filter, data_name):
        date_gte = datetime.strptime(filter[data_name][:10], '%m/%d/%Y')
        date_lte = datetime.strptime(filter[data_name][-10:], '%m/%d/%Y')
        return [date_gte, date_lte]


@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomeListView(MainListView):
    model = File
    template_name = 'customers/files_list.html'
    list_template = 'customers/_files_list.html'
    base_url = 'fe_home'

    def get_list(self, filter):
        objects = self.model.objects.all()
        if 'name' in filter:
            objects = objects.filter(name__icontains=filter['name'])
        if 'created' in filter:
            dates = self.format_dates(filter, 'created')
            objects = objects.filter(created_at__gte=dates[0])
            objects = objects.filter(created_at__lte=dates[1])
        if 'type' in filter and int(filter['type']):
            objects = objects.filter(type=filter['type'])
        if 'sort' in filter and filter['sort']:
            sort = filter['sort']
            sort_map = {
                'created': 'created'
            }
            sort = sort_map.get(sort, sort)
            if 'order' in filter and filter['order'] == 'desc':
                sort = '-' + sort
            objects = objects.order_by(sort)
        return objects


class FileDetailView(DetailView):
    model = File
    template_name = 'customers/file_view.html'
    pk_url_kwarg = 'id'
