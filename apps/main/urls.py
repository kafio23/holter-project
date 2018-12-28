from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='url_home'),
    # path('tutorial/', views.Plot1DView.as_view(), name='url_tutorial')
]