from django.conf.urls import url
from django.contrib import auth

urlpatterns = (
    url(r'^logout/$', auth.logout, {'next_page': '/'}, name='url_logout'),
    url(r'^login/$', auth.login, {'template_name': 'login.html'}, name='url_login'),
)
