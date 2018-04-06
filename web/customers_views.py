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
from web.views import ObjectsListView


class FEListView(ObjectsListView):
    pagin_template = 'customers/_pagin.html'
    default_pp = 12


@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomeListView(FEListView):
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
