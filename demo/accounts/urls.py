from . import views
from django.conf.urls import url
urlpatterns = [
    url(r'^$', views.home),
    url(r'^accounts/', views.loginInput, name='loginInput'),
]
