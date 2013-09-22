from django.conf.urls import patterns, url
from tags import views

urlpatterns = patterns('',
    url(r'^$', views.TagsView.as_view(), name='tagView'),
    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^save/$', views.SaveTag, name='saveTag'),
    url(r'^remove/$', views.RemoveTag, name='removeTag'),
)