from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from careers import views

urlpatterns = patterns('',
    url(r'^categorize$', login_required(views.Categorize.as_view()), name="categorize"),
    url(r'^(?P<careerCategory>[0-9A-Za-z]+)$', views.Career.as_view(), name="career")
)