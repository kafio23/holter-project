from django.urls import path
from . import views

urlpatterns = (
    path('doctors/', views.doctors_list, name='url_doctors_list'),
    path('patients/', views.patients_list, name='url_patients_list'),
    path('patient/(?P<patient_id>-?\d+)/$', views.patient_view, name='url_patient_view'),
    path('patient/(?P<patient_id>-?\d+)/upload/$', views.patient_upload, name='url_patient_upload'),
    path('patient/(?P<patient_id>-?\d+)/signal_upload/$', views.signal_upload, name='url_signal_upload'),
    path('patient/(?P<patient_id>-?\d+)/overview/$', views.patient_overview, name='url_patient_overview'),
)