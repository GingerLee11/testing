from django.urls import path, re_path

from . import views

urlpatterns = [
    path('new', views.new_list, name='new-list'),
    re_path(r'^(\d+)/$', views.view_list, name='view-list'),
]
