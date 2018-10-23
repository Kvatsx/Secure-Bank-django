from django.conf.urls import url
from . import views
from SecureBank import internal_user_view, external_user_view
from django.contrib.auth.views import login
# from django.contrib.auth.views import login_required


urlpatterns = [
    #url(r'^$', views.home),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
    url(r'^staff/$',internal_user_view.home_internal_user, name='staff'),
    url(r'^fundtransfer/$',views.fundtransfer, name='fundtransfer'),
    url(r'^profile/$',views.profile, name='profile'),
    url(r'^user/$', external_user_view.home_external_user, name='user'),
    url(r'^$', views.index, name='index'),
]