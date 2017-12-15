# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
#Plotly
import plotly.plotly as py
from plotly.graph_objs import *
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np
import glob
import os
import datetime


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    kwargs = {'title': 'Holter Monitor Web'}
    return render(request, 'body.html', kwargs)

def plot_graph():

    import plotly

    py = plotly.plotly(username='kafio', key='WHQcWnXsrvMrDtgDNHdT')


    y=0
    t=0
    dt=0.01
    g=9.8
    v=4
    yp=[]
    tp=[]

    while y>=0:
        v=v-g*dt
        y=y+v*dt
        t=t+dt
        yp=yp+[y]
        tp=tp+[t]



    response=py.plot(tp,yp)
    url=response['url']
    filename=response['filename']
    print(url)
    print(filename)
    return


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
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    print "Number of points: %s" % len(x_data)
    return plot_div


class Plot1DView(TemplateView):
    template_name = "plot.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = plot1d()
        return context




def plot2d():
    t = np.linspace(-1,1,2000)
    x = (t**2)+(0.5*np.random.randn(2000))
    y = (t**2)+(0.5*np.random.randn(2000))

    trace1 = go.Scatter(
        x=x, y=y, mode='markers', name='points',
        marker=dict(color='rgb(0,0,0)', size=2, opacity=0.4)
    )
    trace2 = go.Histogram2d(
        x=x, y=y, name='density',
        nbinsx=100, nbinsy=100,
        colorscale='Jet', reversescale=False, showscale=True
    )
    trace3 = go.Histogram(
        x=x, name='x density',
        marker=dict(color='blue'),
        yaxis='y2'
    )
    trace4 = go.Histogram(
        y=y, name='y density', marker=dict(color='blue'),
        xaxis='x2'
    )
    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout(
        showlegend=False,
        autosize=False,
        width=800,
        height=700,
        xaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False
        ),
        margin=dict(
            t=50
        ),
        hovermode='closest',
        bargap=0,
        xaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        ),
        yaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        )
    )

    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


class Plot2DView(TemplateView):
    template_name = "plot.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot2DView, self).get_context_data(**kwargs)
        context['plot'] = plot2d()
        return context


