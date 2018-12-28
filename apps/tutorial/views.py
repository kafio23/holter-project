from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView
import plotly.offline as opy
import plotly.graph_objs as go
import numpy as np


def plot1d():
    x_data = np.arange(0, 120,0.1)
    trace1 = go.Scatter(
        x=x_data,
        y=np.sin(x_data)
    )

    data = [trace1]
    layout = go.Layout(
        # autosize=False,
        # width=900,
        # height=500,

        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = opy.plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


class Plot1DView(TemplateView):
    template_name = "tutorial/tutorial.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = plot1d()
        context['no_sidebar'] = True
        context['title'] = 'Tutoriales'
        return context
