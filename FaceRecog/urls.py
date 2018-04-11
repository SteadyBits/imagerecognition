from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from FaceRecog import views
from FaceRecog.forms import CustomerForm

urlpatterns = [

    url(r'^dashboard/$', views.home, name='dashboard'),
    url(r'^image/class/$', views.upload_and_predict, name='upload'),

]