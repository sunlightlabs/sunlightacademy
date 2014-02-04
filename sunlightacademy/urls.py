from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/$', TemplateView.as_view(template_name="about.html")),
    url(r'^ti-webinar/$', TemplateView.as_view(template_name="ti-webinar.html")),
    #url(r'^webinars/$', TemplateView.as_view(template_name="calendar.html")),
    url(r'', include('sfapp.urls')),
    url(r'', include('training.urls')),
)
