from django.conf.urls import patterns, url
from search import views

urlpatterns = patterns('',
    url(r'^$', views.SearchAllView.as_view(), name='searchAll'),
)