from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
# from django.contrib.auth.views import login_required


urlpatterns = [
    #url(r'^$', views.home),
    url(r'^login/', views.login_user, name = 'login'),
    url(r'^logout/', views.logout_user, name='logout'),
<<<<<<< HEAD
    url(r'^staff/$',views.home_internal_user,name = 'staff'),
    url(r'^fundtransfer/$',views.fundtransfer,name = 'fundtransfer'),
    url(r'^profile/$',views.profile,name = 'profile'),
    url(r'^user/$',views.home_external_user,name='user'),
=======
    url(r'^home_internal_user/$',views.home_internal_user,name = 'home_internal_user'),
    url(r'^fundtransfer/$',views.fundtransfer,name = 'fundtransfer'),
    url(r'^profile/$',views.profile,name = 'profile'),
    url(r'^home_external_user/$',views.home_external_user,name='home_external_user'),
>>>>>>> 2bddcab9e26953f0530b212066396df0ca4d7f65
    url(r'^$', views.index, name='index'),
]