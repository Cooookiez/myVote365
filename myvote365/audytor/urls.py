from django.conf.urls import url
from audytor import views

app_name = 'auditor'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^presentacje/$', views.presentations_list, name='presentations_list'),
    url(r'^presentacja/nowa/$', views.presentations_new, name='presentation_new'),
    url(r'^presentacja/edytuj/(?P<short_id_num>[a-zA-Z0-9]{4})/$', views.presentations_edit, name='presentation_edit'),
    url(r'^ustawienia/$', views.settings, name='settings'),
    url(r'^settings/update/general/$', views.settings_update_general, name='update_general'),
    url(r'^settings/update/email/$', views.settings_update_email, name='update_email'),
    url(r'^settings/update/password/$', views.settings_update_password, name='update_password'),
    url(r'^$', views.panel, name='panel'),
]
