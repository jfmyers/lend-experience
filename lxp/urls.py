from django.conf.urls import patterns, include, url

from django.contrib import admin
from userProfile import views
from siteInfo import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('contributions.urls', namespace="feed")),
    url(r'^contributions/', include('contributions.urls', namespace="contributions")),
    url(r'^about/', views.AboutView.as_view(), name='about'),
    url(r'^accounts/', include('accounts.urls',namespace="accounts")),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^career/', include('careers.urls',namespace="careers")),
    url(r'^community/', views.CommunityView.as_view(), name='community'),
    url(r'^contact/', views.ContactView.as_view(), name='contact'),
    url(r'^legal/', views.LegalView.as_view(), name='legal'),
    url(r'^tags/', include('tags.urls',namespace="tags")),
    url(r'^story/', include('userProfile.urls',namespace="myUserProfile")),
    url(r'^search/', include('search.urls',namespace="search")),
    
    #url(r'^info/', include('about.urls',namespace="siteInfo")),
    
    
    url(r'^(?P<tag>[0-9A-Za-z]+)-(?P<pk>[0-9]+)/', include('tags.urls',namespace="tagDetail")),
    url(r'^(?P<handle>[0-9A-Za-z]+)_(?P<pk>[0-9]+)/', include('userProfile.urls',namespace="userProfile")),
    
)
