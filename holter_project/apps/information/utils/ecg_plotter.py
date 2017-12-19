# This script helps to plot ECG signals. 

import pandas as pd
from plotly import graph_objs
from plotly.offline import plot

def plot_ecg(file_name):

    df = pd.read_csv('/home/fiorella/workspace/holter_project/holter_project/media/'+file_name)
    trace1 = graph_objs.Scatter(
                        x=df['x'], y=df['y'], # Data
                        mode='lines', name='signal' # Additional options
                        )

    layout = graph_objs.Layout(title='Simple Plot from csv data',
                   plot_bgcolor='rgb(230, 230,230)')
                   
    data = [trace1]
    fig = graph_objs.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div