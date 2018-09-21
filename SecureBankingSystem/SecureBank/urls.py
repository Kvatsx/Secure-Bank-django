from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
# from django.contrib.auth.views import login_required


urlpatterns = [
    url(r'^$', views.home),
    # url(r'^login/$', login, {'template_name': 'SecureBank/login.html'})
]