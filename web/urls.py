from django.conf.urls import url

from web.views import *
from web.user_views import *
from web.customers_views import *


urlpatterns = [

    # customer fronted views
    url(r'^$', HomeListView.as_view(), name='fe_home'),
    url(r'^file/(?P<id>\d+)/$', FileDetailView.as_view(), name='fe_file'),

    # admin views
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^files/$', FilesListView.as_view(), name='files'),
    url(r'^files/add/$', FilesAddView.as_view(), name='files_add'),
    url(r'^files/edit/(?P<id>\d+)/$', FilesEditView.as_view(), name='files_edit'),
    url(r'^files/delete/(?P<id>\d+)$', FilesDeleteView.as_view(), name='files_delete'),

    url(r'^users/$', UsersListView.as_view(), name='users'),
    url(r'^users/edit/(?P<id>\d+)/$', UsersEditView.as_view(), name='users_edit'),
    url(r'^users/delete/(?P<id>\d+)$', UsersDeleteView.as_view(), name='users_delete'),

    url(r'^folders/$', FoldersListView.as_view(), name='folders'),
    url(r'^video/$', VideoListView.as_view(), name='video'),

]
