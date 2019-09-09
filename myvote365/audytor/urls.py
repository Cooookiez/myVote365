from django.conf.urls import url
from audytor import views

app_name = 'audytor'

urlpatterns = [
    url(r'^register/$', views.audytor_register, name='register'),
    url(r'^$', views.audytor_login_register, name='index'),
]
