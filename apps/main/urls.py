from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='url_home'),
    url(r'^plot/$', views.plot_graph, name='url_plot_graph'),
    url(r'^plot1d/$', views.Plot1DView.as_view(), name='plot1d'),
    url(r'^plot2d/$', views.Plot2DView.as_view(), name='plot2d'),
    url(r'^plotecg/$', views.PlotECG.as_view(), name='plot_ecg'),
]
