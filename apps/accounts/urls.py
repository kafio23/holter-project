from django.urls import path
from django.contrib import auth

urlpatterns = (
    path('logout/', auth.logout, {'next_page': '/'}, name='url_logout'),
    path('login/', auth.login, {'template_name': 'login.html'}, name='url_login'),
)
