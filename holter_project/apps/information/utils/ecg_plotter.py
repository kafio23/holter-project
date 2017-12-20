# This script helps to plot ECG signals. 

import pandas as pd
from plotly import graph_objs
from plotly.offline import plot
from django.conf import settings

from scipy import signal
from scipy.signal import find_peaks_cwt
from numpy import polyfit
import numpy as np

from detect_peaks import detect_peaks

def plot_ecg(file_name):

    df = pd.read_csv(settings.MEDIA_ROOT+'/'+file_name)
    x=df['x']
    y=df['y']

    #---------------- Processing Signal----------------
    ## Filtro Pasa-Bajas
    y=signal.savgol_filter(y,21,7)

    ## Detrend
    p = polyfit((np.arange(len(y))),y,6)
    f_y = np.polyval(p,(np.arange(len(y))))
    ecg_data = y - f_y
    y = ecg_data

    ## Normalizar
    ecg_data = ecg_data/max(abs(ecg_data))
    y = ecg_data

    ## Picos Bajos
    peaks_index = detect_peaks(-ecg_data, mph=0.6, mpd=0.150, show=True)
    ecg_peaks = ecg_data[peaks_index]
    tm_peaks = x[peaks_index]
    print 'Picos Bajos: ', ecg_peaks
    
    ## Segundos entre intervalos
    rateBPM_values = []
    rateBPM_sum    = 0
    if len(peaks_index) > 9:  #minimo 10 ciclos
        for i in range(1,len(peaks_index)):
            t_dif = x[i]-x[i-1]
            rateBPM_values.append(t_dif) 
        rateBPM_sum = sum(rateBPM_values)
    
    ## BPM
    rateBPM = len(peaks_index) / (x[(len(x)-1)]-x[0]) * 60
    print 'rateBPM: ', rateBPM

    ## Mean R-R Interval
    #--------------------------------------------------

    trace1 = graph_objs.Scatter(
                        x=x, y=y, # Data
                        mode='lines', name='signal' # Additional options
                        )

    layout = graph_objs.Layout(title='ECG ('+file_name+')',
                   plot_bgcolor='rgb(230, 230,230)')
                   
    data = [trace1]
    fig = graph_objs.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div