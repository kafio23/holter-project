from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^doctors/$', views.doctors_list, name='url_doctors_list'),
    url(r'^patients/$', views.patients_list, name='url_patients_list'),
)