from django.conf.urls import url
from . import views

urlpatterns = [
    #Routes to render templates
    url(r'^$', views.index),
    url(r'books/add$', views.addbook),
    url(r'books/(?P<number>[0-9]+)$', views.loadbook),
    url(r'users/(?P<number>[0-9]+)$', views.loaduser),

    #Routes to process and redirect
    url(r'processregistration$', views.registration),
    url(r'logout$', views.logout),
    url(r'login$', views.login),
    url(r'processaddbook$', views.processaddbook),
    url(r'processaddreview$', views.processaddreview)
] 