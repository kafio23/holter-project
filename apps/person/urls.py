from django.urls import path
from . import views

urlpatterns = (
    path('doctors/', views.doctors_list, name='url_doctors_list'),
    path('patients/', views.patients_list, name='url_patients_list'),
    path('patient/<int:patient_id>/', views.patient_show, name='url_patient_show'),
    path('patient/<int:patient_id>/antes', views.patient_view, name='url_patient_view'),
    path('patient/<int:patient_id>/upload/', views.patient_upload, name='url_patient_upload'),
    path('patient/<int:patient_id>/signal_upload/', views.signal_upload, name='url_signal_upload'),
    path('patient/<int:patient_id>/overview/', views.patient_overview, name='url_patient_overview'),
)
