from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('mobvisuals.views',
    (r'^$', 'Login'),
    (r'^index/$', 'index'),
    (r'^py_dot_chart.png$','py_dot_chart'),
    (r'^visuals/$', 'visuals'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

