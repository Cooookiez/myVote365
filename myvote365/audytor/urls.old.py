from django.conf.urls import url
from audytor import views

app_name = 'audytor'

urlpatterns = [
    url(r'^register/?$', views.audytor_register, name='register'),
    url(r'^login/?$', views.audytor_login_register, name='login'),
    url(r'^logout/?$', views.audytor_logout, name='logout'),
    url(r'^prezentacje/?$', views.presentations, name='panel_presentations'),
    url(r'^prezentacje/nowa/?$', views.presentation_new, name='panel_presentation_new'),
    url(r'^prezentacje/edytuj/(?P<presentation_id>[a-zA-Z0-9]{4})/?$', views.presentation_edit, name='panel_presentation_edit'),
    url(r'^ustawienia/?$', views.user_settings, name='panel_user_settings'),
    url(r'^ustawienia/update/general/?$', views.user_settings_update_general, name='panel_user_settings_update_general'),
    url(r'^ustawienia/update/email/?$', views.user_settings_update_email, name='panel_user_settings_update_email'),
    url(r'^ustawienia/update/password/?$',views.user_settings_update_password, name='panel_user_settings_update_password'),
    url(r'^$', views.panel, name='panel'),
]
