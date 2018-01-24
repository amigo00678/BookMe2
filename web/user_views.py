# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import FormView, RedirectView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect

from web.forms import *


class LoginView(FormView):
    template_name = 'common/login.html'
    form_class = AuthForm

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.data.get('username'),
            password=form.data.get('password'))
        if user:
            login(self.request, user)
            return HttpResponseRedirect('files')
        else:
            return HttpResponseRedirect('login')


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)
