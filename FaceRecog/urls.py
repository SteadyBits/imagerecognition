from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from FaceRecog import views
from FaceRecog.forms import FileUploadedForm

urlpatterns = [

    url(r'^dashboard/$', views.home, name='dashboard'),
    url(r'^image/class/$', views.file_upload, name='upload'),
    url(r'^image/class/api/$', views.file_upload_api, name='upload_api'),

]