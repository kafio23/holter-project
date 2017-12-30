from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^doctors/$', views.doctors_list, name='url_doctors_list'),
    url(r'^patients/$', views.patients_list, name='url_patients_list'),
    url(r'^patient/(?P<patient_id>-?\d+)/$', views.patient_view, name='url_patient_view'),
    url(r'^patient/(?P<patient_id>-?\d+)/upload/$', views.patient_upload, name='url_patient_upload'),
    url(r'^patient/(?P<patient_id>-?\d+)/signal_upload/$', views.signal_upload, name='url_signal_upload'),
    url(r'^patient/(?P<patient_id>-?\d+)/overview/$', views.patient_overview, name='url_patient_overview'),
)