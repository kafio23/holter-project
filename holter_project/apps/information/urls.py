from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^patient/(?P<patient_id>-?\d+)/plot/(?P<diag_id>-?\d+)/$', views.PlotECG.as_view(), name='url_diagnosis_plot'),
)