# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.views.generic import ListView

from web.models import *


class FilesListView(ListView):
    model = File
    template_name = 'files/list.html'

    def get_context_data(self, **kwargs):
        context = super(FilesListView, self).get_context_data(**kwargs)
        context['files'] = [
            {'name': 'f1'},
            {'name': 'f2'},
            {'name': 'f3'},
        ]
        return context
