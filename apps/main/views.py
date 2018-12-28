from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponseRedirect(reverse('url_home'))


def home(request):
    kwargs = {'title': 'Holter Monitor Web'}
    kwargs['no_sidebar'] = True
    kwargs['title']      = '¡Bienvenido!'
    kwargs['suptitle']   = ''
    return render(request, 'main/body.html', kwargs)

# def tutorial(request):
#     kwargs = {}
#     kwargs['no_sidebar'] = True
#     kwargs['title']      = 'Tutorial'
#     return render(request, 'main/tutorial.html', kwargs)

import plotly.offline as opy
import plotly.graph_objs as go
import numpy as np

class Graph(TemplateView):
    template_name = 'main/tutorial.html'
    kwargs = {}
    kwargs['no_sidebar'] = True

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        # x = [-2,0,4,6,7]
        # y = [q**2-q+3 for q in x]
        # trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': "10"},
        #                     mode="lines",  name='1st Trace')

        # data=go.Data([trace1])
        # layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        # figure=go.Figure(data=data,layout=layout)
        # div = opy.plot(figure, auto_open=False, output_type='div')
        # import plotly.plotly as py
        # import plotly.graph_objs as go

        # Create random data with numpy
        

        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        trace = go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )

        data = [trace]

        # Plot and embed in ipython notebook!
        # div = opy.plot(data, filename='basic-scatter')
        div = opy.plot(data, filename='basic-line')

        # or plot with: plot_url = py.plot(data, filename='basic-line')

        context['plot'] = div

        return context, kwargs

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
    template_name = "main/tutorial.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = plot1d()
        context['no_sidebar'] = True
        return context

def about_us(request):
    kwargs = {}
    kwargs['no_sidebar'] = True
    # kwargs['title']      = '¡Bienvenido!'
    # kwargs['suptitle']   = ''
    render(request, "about_us.html", kwargs)