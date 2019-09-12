from django.conf.urls import url
from audytor import views

app_name = 'audytor'

urlpatterns = [
    url(r'^register/$', views.audytor_register, name='register'),
    url(r'^login/$', views.audytor_login, name='login'),
    url(r'^logout/$', views.audytor_logout, name='logout'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^panel/prezentacje/$', views.presentations, name='panel_presentations'),
    url(r'^panel/ustawienia/$', views.user_settings, name='panel_user_settings'),
    url(r'^$', views.audytor_login_register, name='index'),
]
