from . import views
from django.conf.urls import url

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name='index')
]
