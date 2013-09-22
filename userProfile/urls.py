from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from userProfile import views

urlpatterns = patterns('',
    url(r'^$', views.Story.as_view(), name="story"),
    url(r'^edit/$', login_required(views.EditStory.as_view()), name="edit"),
    url(r'^edit/save/$', login_required(views.Update.as_view()), name="saveEdit"),
    url(r'^edit/image/$', login_required(views.ImageUpload.as_view()), name="uploadImage"),
    url(r'^view/$', login_required(views.Story.as_view()), name="mystory"),
)