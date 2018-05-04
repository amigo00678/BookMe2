from django.conf.urls import url

from web.views import *
from web.user_views import *
from web.customers_views import *


urlpatterns = [

    # customer fronted views
    url(r'^$', HomeListView.as_view(), name='fe_home'),

    url(r'^customer-file/(?P<id>\d+)/$', FileDetailView.as_view(), name='fe_file'),
    url(r'^customer-files/$', HomeFilesListView.as_view(), name='fe_files'),
    url(r'^customer-audio/$', HomeAudioListView.as_view(), name='fe_audio'),
    url(r'^customer-video/$', HomeVideoListView.as_view(), name='fe_video'),
    url(r'^customer-bin/$', HomeBinaryListView.as_view(), name='fe_bin'),

    url(r'^customer-reviews/(?P<id>\d+)/$', HomeReviewsListView.as_view(), name='fe_reviews'),
    url(r'^customer-reviews-add/(?P<id>\d+)/$', HomeReviewAddView.as_view(), name='fe_review_add'),

    url(r'^customer-login/$', HomeLoginView.as_view(), name='fe_login'),
    url(r'^customer-logout/$', HomeLogoutView.as_view(), name='fe_logout'),

    # admin views
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # features
    url(r'^features/$', FeaturesListView.as_view(), name='features'),
    url(r'^features/add/$', FeatureAddView.as_view(), name='features_add'),
    url(r'^features/edit/(?P<id>\d+)/$', FeatureEditView.as_view(), name='features_edit'),
    url(r'^features/delete/(?P<id>\d+)$', FeatureDeleteView.as_view(), name='features_delete'),

    # orders
    url(r'^orders/$', OrdersListView.as_view(), name='orders'),
    url(r'^orders/add/$', OrdersAddView.as_view(), name='orders_add'),
    url(r'^orders/edit/(?P<id>\d+)/$', OrdersEditView.as_view(), name='orders_edit'),
    url(r'^orders/delete/(?P<id>\d+)$', OrdersDeleteView.as_view(), name='orders_delete'),

    # room features
    url(r'^room-features/$', RoomFeaturesListView.as_view(), name='room_features'),
    url(r'^room-features/add/$', RoomFeatureAddView.as_view(), name='room_features_add'),
    url(r'^room-features/edit/(?P<id>\d+)/$', RoomFeatureEditView.as_view(), name='room_features_edit'),
    url(r'^room-features/delete/(?P<id>\d+)$', RoomFeatureDeleteView.as_view(), name='room_features_delete'),

    # rooms
    url(r'^rooms/(?P<p_id>\d+)/$', RoomsListView.as_view(), name='rooms'),
    url(r'^rooms/(?P<p_id>\d+)/add/$', RoomAddView.as_view(), name='rooms_add'),
    url(r'^rooms/(?P<p_id>\d+)/edit/(?P<id>\d+)/$', RoomEditView.as_view(), name='rooms_edit'),
    url(r'^rooms/(?P<p_id>\d+)/delete/(?P<id>\d+)$', RoomDeleteView.as_view(), name='rooms_delete'),

    # reviews
    url(r'^reviews/$', ReviewsListView.as_view(), name='reviews'),
    url(r'^reviews/add/$', ReviewAddView.as_view(), name='reviews_add'),
    url(r'^reviews/edit/(?P<id>\d+)/$', ReviewEditView.as_view(), name='reviews_edit'),
    url(r'^reviews/delete/(?P<id>\d+)$', ReviewDeleteView.as_view(), name='reviews_delete'),

    # files
    url(r'^files/$', FilesListView.as_view(), name='files'),
    url(r'^files/add/$', FilesAddView.as_view(), name='files_add'),
    url(r'^files/edit/(?P<id>\d+)/$', FilesEditView.as_view(), name='files_edit'),
    url(r'^files/delete/(?P<id>\d+)$', FilesDeleteView.as_view(), name='files_delete'),

    # users
    url(r'^users/$', UsersListView.as_view(), name='users'),
    url(r'^users/edit/(?P<id>\d+)/$', UsersEditView.as_view(), name='users_edit'),
    url(r'^users/add/$', UsersAddView.as_view(), name='users_add'),
    url(r'^users/delete/(?P<id>\d+)$', UsersDeleteView.as_view(), name='users_delete'),

    url(r'^folders/$', FoldersListView.as_view(), name='folders'),
    url(r'^video/$', VideoListView.as_view(), name='video'),

]
