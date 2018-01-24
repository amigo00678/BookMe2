# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import FormView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect

from web.forms import *


class LoginView(FormView):
    template_name = 'common/login.html'
    form_class = AuthForm

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect('files')

    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super(LoginView, self).post(request, *args, **kwargs)
