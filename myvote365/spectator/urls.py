from django.conf.urls import url
from spectator import views

app_name = 'spectator'

urlpatterns = [
    url(r'^(?P<short_id_num>[a-zA-Z0-9]{4})/$', views.index, name='index'),
]
