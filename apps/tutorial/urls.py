from django.urls import path
from . import views

urlpatterns = [
    path('', views.Plot1DView.as_view(), name='url_tutorial'),
    path('manual/', views.web_manual, name='url_tutorial_manual')
]