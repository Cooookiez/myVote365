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
    url(r'^panel/ustawienia/update/general$', views.user_settings_update_general, name='panel_user_settings_update_general'),
    url(r'^panel/ustawienia/update/email$', views.user_settings_update_email, name='panel_user_settings_update_email'),
    url(r'^panel/ustawienia/update/password$',views.user_settings_update_password, name='panel_user_settings_update_password'),
    url(r'^$', views.audytor_login_register, name='index'),
]
