from django.conf.urls import url

from web.views import *


urlpatterns = [
    url(r'^$', FilesListView.as_view(), name='files'),
]
