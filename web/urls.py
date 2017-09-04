from django.conf.urls import url

from web.views import *


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^files/', FilesListView.as_view(), name='files'),
    url(r'^files-list/', FilesListView.as_view(), name='files_list'),
    url(r'^folders/', FoldersListView.as_view(), name='folders'),
    url(r'^video/', VideoListView.as_view(), name='video'),
]