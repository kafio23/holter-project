from django.urls import path
from . import views

urlpatterns = (
    path('patient/<int:patient_id>/plot/<int:diag_id>/', views.PlotECG.as_view(), name='url_diagnosis_plot'),
    path('patient/<int:patient_id>/edit/<int:diag>/', views.diagnosis_edit, name='url_diagnosis_edit'),
    path('patient/<int:patient_id>/processing/', views.processing_parameters, name='url_processing_parameters'),
    #path('patient/(?P<patient_id>-?\d+)/processing/(?P<signal_id>-?\d+)/', views.processing_plot, name='url_processing_plot'),
    path('patient/<int:patient_id>/processing/<int:diag_id>/', views.PlotsECG.as_view(), name='url_processing_plots')
)