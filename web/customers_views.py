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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FEListView(ObjectsListView):
    pagin_template = 'customers/_pagin.html'
    template_name = 'customers/files_list.html'
    list_template = 'customers/_files_list.html'
    default_pp = 8


@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomeListView(FEListView):
    model = File
    template_name = 'customers/files_list.html'
    list_template = 'customers/_files_list.html'
    base_url = 'fe_home'
    default_pp = 12

    def get_list(self, filter):
        return self.model.objects.all()


class FileDetailView(DetailView):
    model = File
    template_name = 'customers/file_view.html'
    pk_url_kwarg = 'id'


class HomeFilesListView(FEListView):
    model = File
    base_url = 'fe_files'

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[0][0])


class HomeAudioListView(FEListView):
    model = File
    base_url = 'fe_audio'

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[1][0])


class HomeVideoListView(FEListView):
    model = File
    base_url = 'fe_video'

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[2][0])


class HomeBinaryListView(FEListView):
    model = File
    base_url = 'fe_bin'

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[3][0])
