from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
# from django.contrib.auth.views import login_required


urlpatterns = [
    #url(r'^$', views.home),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
    # url(r'^staff/', views.home_internal_user, name='staff'),
    url(r'^fundtransfer/$', views.fundtransfer, name='fundtransfer'),
    url(r'^fundcredit/$', views.fundcredit, name='fundcredit'),
    url(r'^funddebit/$', views.funddebit, name='funddebit'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^user/$', views.home_external_user, name='user'),
    # url(r'^manager/$', views.home_internal_user, name='manager'),
    url(r'^authorize_transaction/$', views.authorize_transaction, name='authorize_transaction'),
    url(r'^$', views.index, name='index'),

    url(r'^transaction_confirmation/(?P<transaction_id>[0-9]+)/$', views.transaction_confirmation,
        name='transaction_confirmation')
]