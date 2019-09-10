from django.conf.urls import url
from audytor import views

app_name = 'audytor'

urlpatterns = [
    url(r'^register/$', views.audytor_register, name='register'),
    url(r'^login/$', views.audytor_login, name='login'),
    url(r'^logout/$', views.audytor_logout, name='logout'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^$', views.audytor_login_register, name='index'),
]
