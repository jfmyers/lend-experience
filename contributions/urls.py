from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from contributions import views

urlpatterns = patterns('',
    url(r'^$', views.MultiContributionView.as_view(), name="post_list"),
    url(r'^(?P<title>[0-9A-Za-z]+)-(?P<pk>\d+)/$', views.SingleContributionView.as_view(), name='detail'),
    url(r'^add/$', login_required(views.AddContributionView.as_view()), name='post'),
    url(r'^edit/(?P<title>[0-9A-Za-z]+)-(?P<pk>\d+)/$', login_required(views.EditContributionView.as_view()), name='edit'),
    url(r'^save_new/$', login_required(views.SaveNewPostForm.as_view()), name='saveNewPost'),
    url(r'^save_existing/$', login_required(views.SaveExistingPostForm.as_view()), name='saveExistingPost'),
    url(r'^comment/save/$', login_required(views.CommentPost), name='comment_save'),
    url(r'^comment/remove/$', login_required(views.CommentRemove), name='comment_remove'),
)