from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
# from django.contrib.auth.views import login_required


urlpatterns = [
<<<<<<< HEAD
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', login, {'template_name': 'SecureBank/login.html'}),
    url(r'^login/', views.loginView, name='loginView'),
=======
    #url(r'^$', views.home),
    url(r'^login/', views.login_user, name = 'login'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^home_internal_user/$',views.home_internal_user,name = 'home_internal_user'),
    url(r'^home_external_user/$',views.home_external_user,name='home_external_user'),
    url(r'^$', views.index, name='index'),
>>>>>>> master
]