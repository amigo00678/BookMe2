# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render

from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from web.models import *
from web.forms import *


class AdminAuthUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.type == 1:
            return HttpResponseRedirect(reverse('fe_home'))
        return super(AdminAuthUserMixin, self).dispatch(request, *args, **kwargs)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ObjectsListView(ListView):
    model = File
    template_name = 'files_list.html'
    list_template = '_files_list.html'
    pagin_template = 'common/_pagin.html'
    default_pp = 10
    base_url = 'files'

    def get_context_data(self, **kwargs):
        context = super(ObjectsListView, self).get_context_data(**kwargs)
        page = int(self.kwargs.get('page', 1))
        objects, page = self.get_objects(filter={}, pp=self.default_pp, page=page)
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
            request.POST, request.POST.get('pp', self.default_pp), request.POST.get('page', 1))
        context['objects'] = objects
        context['page'] = page
        context['list_url'] = reverse(self.base_url)
        return JsonResponse({
            'reply': render_to_string(self.list_template, context),
            'pagin': render_to_string(self.pagin_template, context)
        })

    def format_dates(self, filter, data_name):
        date_gte = datetime.strptime(filter[data_name][:10], '%m/%d/%Y')
        date_lte = datetime.strptime(filter[data_name][-10:], '%m/%d/%Y')
        return [date_gte, date_lte]


class FilesListView(AdminAuthUserMixin, ObjectsListView):
    model = File
    template_name = 'files_list.html'
    list_template = '_files_list.html'
    base_url = 'files'

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


class FilesEditView(AdminAuthUserMixin, FormView):
    form_class = FileEditForm
    success_url = reverse_lazy('files')
    template_name = 'files_edit.html'

    def get_form(self, form_class):
        try:
            instance = File.objects.get(id=self.kwargs.get('id'))
            return form_class(instance=instance, **self.get_form_kwargs())
        except File.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        messages.info(self.request, 'File updated successfully')
        return super(FilesEditView, self).form_valid(form)


class FilesAddView(AdminAuthUserMixin, FormView):
    form_class = FileEditForm
    success_url = reverse_lazy('files')
    template_name = 'files_add.html'

    def form_valid(self, form):
        form.save()
        messages.info(self.request, 'File created successfully')
        return super(FilesAddView, self).form_valid(form)


class FilesDeleteView(AdminAuthUserMixin, RedirectView):
    reverse_url = reverse_lazy('files')

    def get_redirect_url(self, *args, **kwargs):
        try:
            file = File.objects.get(id=self.kwargs.get('id'))
            fname = file.name
            file.delete()
            messages.info(self.request, "File '%s' deleted successfully" % (fname))
        except File.DoesNotExist:
            pass
        return self.reverse_url


class FoldersListView(AdminAuthUserMixin, ObjectsListView):
    model = Folder
    template_name = 'folders_list.html'
    list_template = '_folders_list.html'
    base_url = 'folders'

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


class VideoListView(AdminAuthUserMixin, ObjectsListView):
    model = Folder
    template_name = 'folders_list.html'
    list_template = '_folders_list.html'
    base_url = 'folders'

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


class AudioListView(AdminAuthUserMixin, ObjectsListView):
    model = Folder
    template_name = 'folders_list.html'
    list_template = '_folders_list.html'
    base_url = 'folders'

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


class UsersListView(AdminAuthUserMixin, ObjectsListView):
    model = User
    template_name = 'users_list.html'
    list_template = '_users_list.html'
    base_url = 'users'

    def get_list(self, filter):
        objects = self.model.objects.all()
        if 'name' in filter:
            objects = objects.filter(first_name__icontains=filter['name'])
        if 'email' in filter:
            objects = objects.filter(email__icontains=filter['email'])
        if 'created' in filter:
            dates = self.format_dates(filter, 'created')
            objects = objects.filter(created_at__gte=dates[0])
            objects = objects.filter(created_at__lte=dates[1])
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


class UsersEditView(AdminAuthUserMixin, FormView):
    form_class = FileEditForm
    success_url = reverse_lazy('files')
    template_name = 'files_edit.html'

    def get_form(self, form_class):
        try:
            instance = File.objects.get(id=self.kwargs.get('id'))
            return form_class(instance=instance, **self.get_form_kwargs())
        except File.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        messages.info(self.request, 'File updated successfully')
        return super(FilesEditView, self).form_valid(form)


class UsersDeleteView(AdminAuthUserMixin, RedirectView):
    reverse_url = reverse_lazy('files')

    def get_redirect_url(self, *args, **kwargs):
        try:
            file = File.objects.get(id=self.kwargs.get('id'))
            fname = file.name
            file.delete()
            messages.info(self.request, "File '%s' deleted successfully" % (fname))
        except File.DoesNotExist:
            pass
        return self.reverse_url
