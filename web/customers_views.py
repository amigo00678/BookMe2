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
from django.http import HttpResponseRedirect

from web.models import *
from web.forms import *
from web.views import ObjectsListView


class CustomerAuthUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('fe_home'))
        return super(CustomerAuthUserMixin, self).dispatch(request, *args, **kwargs)


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
    default_pp = 6
    base_url = reverse_lazy('fe_home')

    ratings = { 4: '9+', 3: '8+', 2: '7+', 1: '6+', 0: 'No rating' }

    def get_additional_context(self):
        return { 
            'features': Feature.objects.all(),
            'room_features': RoomFeature.objects.all(),
            'ratings': sorted(self.ratings.iteritems(), reverse=True)
        }

    def get_list(self, filter):
        objects = self.model.objects.all()

        fids = []
        rfids = []
        rates = []

        for key, value in filter.iteritems():
            if key.startswith('feature_'):
                fids.append(int(value))
            elif key.startswith('room_feature_'):
                rfids.append(int(value))
            elif key.startswith('rate_'):
                rates.append(int(value))

        if fids:
            objects = objects.filter(features__in=fids).distinct()
        if rfids:
            objects = objects.filter(room__features__id__in=rfids).distinct()
        if rates:
            rate = min(rates)
            objects = objects.annotate(Avg('review__rate'))
            objects = objects.filter(review__rate__avg__gte=rate)

        if 'sort' in filter and filter['sort']:
            sort = filter['sort']
            sort_map = {
            }
            sort = sort_map.get(sort, sort)
            if 'order' in filter and filter['order'] == 'desc':
                sort = '-' + sort
            objects = objects.order_by(sort)
        else:
            objects = objects.order_by('id')

        return objects


class HomeReviewsListView(FEListView):
    model = Review
    template_name = 'customers/reviews_list.html'
    list_template = 'customers/_reviews_list.html'
    base_url = 'fe_reviews'
    default_pp = 4

    def dispatch(self, *args, **kwargs):
        self.base_url = reverse(self.base_url, kwargs={'id': self.kwargs.get('id')})
        return super(HomeReviewsListView, self).dispatch(*args, **kwargs)

    def get_additional_context(self):
        context = {}
        try:
            file = File.objects.get(id=self.kwargs.get('id'))
            context['file'] = file
        except File.DoesNotExist:
            pass
        return context

    def get_list(self, filter):
        objects = self.model.objects.filter(item__id=int(self.kwargs.get('id'))).order_by('-id')
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


class HomeReviewAddView(CustomerAuthUserMixin, FormView):
    form_class = FEReviewEditForm
    success_url = 'fe_file'
    template_name = 'customers/review_add.html'

    def dispatch(self, *args, **kwargs):
        self.success_url = reverse(self.success_url, kwargs={'id': self.kwargs.get('id')})
        return super(HomeReviewAddView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeReviewAddView, self).get_context_data(**kwargs)
        try:
            file = File.objects.get(id=self.kwargs.get('id'))
            context['file'] = file
        except File.DoesNotExist:
            pass
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)

        try:
            file = File.objects.get(id=self.kwargs.get('id'))
            instance.item = file
        except File.DoesNotExist:
            pass

        instance.user = self.request.user
        instance.save()

        return super(HomeReviewAddView, self).form_valid(form)


class FileDetailView(DetailView):
    model = File
    template_name = 'customers/file_view.html'
    pk_url_kwarg = 'id'


class HomeFilesListView(FEListView):
    model = File
    base_url = reverse_lazy('fe_files')

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[0][0])


class HomeAudioListView(FEListView):
    model = File
    base_url = reverse_lazy('fe_audio')

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[1][0])


class HomeVideoListView(FEListView):
    model = File
    base_url = reverse_lazy('fe_video')

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[2][0])


class HomeBinaryListView(FEListView):
    model = File
    base_url = reverse_lazy('fe_bin')

    def get_list(self, filter):
        return self.model.objects.filter(type=FILE_TYPE_E[3][0])
