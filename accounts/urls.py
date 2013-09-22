from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
    url(r'^login/', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login/'}, name="logout"),
    url(r'^signup/$', views.SignUp.as_view(), name="signup"),
    url(r'^signup/success/$', views.signupSuccess, name="signup_success"),
    url(r'^signup/error/$', views.signupError, name="signup_error"),
    url(r'^user/password/reset/$','django.contrib.auth.views.password_reset', {'post_reset_redirect' : 'done'}, name="password_reset"),
    url(r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done', name="reset_done"),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/accounts/user/password/done/'}),
    url(r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
)