from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), #Main route to load index.html
    url(r'sucess$', views.sucess), #Route to load the sucess.html page
    url(r'processregistration$', views.registration), #post route for registration
    url(r'logout$', views.logout), #route to logout
    url(r'login$', views.login) #post route for login
] 