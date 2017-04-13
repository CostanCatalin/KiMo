from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list/$', views.list_kids, name='list_kids'),
    url(r'^add/$', views.register_kid, name='register_kid'),
    url(r'^stats/$', views.list_stats, name='list_stats'),
    url(r'^edit/(?P<kid_id>[0-9]+)/$', views.edit_kid, name='edit_kid'),
    url(r'^view/(?P<kid_id>[0-9]+)/$', views.view_kid, name='view_kid'),
    url(r'delete/(?P<kid_id>[0-9]+)/$', views.delete_kid, name='delete_kid')
]