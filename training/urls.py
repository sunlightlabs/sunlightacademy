from django.conf.urls import patterns, include, url
from training.views import ModuleView, RegisterPlusView

urlpatterns = patterns('',
    url(r'^$', 'training.views.dashboard', name='dashboard'),
    url(r'^account/$', 'training.views.account', name='account'),
    url(r'^account/delete/$', 'training.views.delete_account', name='delete_account'),
    url(r'^account/error/$', 'training.views.account_error', name='account_error'),
    url(r'^account/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^account/setup/$', 'training.views.setup_account', name='setup_account'),
    url(r'^account/register/$', RegisterPlusView.as_view()),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^account/', include('social_auth.urls')),
    url(r'^category/(?P<slug>[\w\-]+)/$', 'training.views.category', name='training_category'),
    url(r'^module/(?P<slug>[\w\-]+)/$', ModuleView.as_view(), name='training_module'),
    url(r'^module/(?P<slug>[\w\-]+)/feedback/$', 'training.views.module_feedback', name='training_module_feedback'),
    url(r'^module/(?P<slug>[\w\-]+)/mark/$', 'training.views.module_mark', name='training_module_mark'),
    url(r'^tagged/(?P<slug>[\w\-]+)/$', 'training.views.tagged', name='tagged'),
    url(r'^events/$', 'training.views.training_list', name='training_list'),
    url(r'^events/(?P<slug>[\w\-]+)/$', 'training.views.training_detail', name='training_detail'),
    url(r'^registrations/$', 'training.views.registrations'),
)
