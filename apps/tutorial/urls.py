from django.urls import path
from . import views

urlpatterns = [
    path('', views.Plot1DView.as_view(), name='url_tutorial')
]