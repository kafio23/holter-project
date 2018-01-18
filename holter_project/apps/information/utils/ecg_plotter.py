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

    path = '/data/'
    df = pd.read_csv(settings.MEDIA_ROOT+path+file_name)

    try:
        x=df['x']
        y=df['y']
    except:
        df = pd.read_csv(settings.MEDIA_ROOT+path+file_name, sep=';')

    x=df['x']
    y=df['y']
    
    #-Agregado para aumentar tiempo 04-01-2018
    #print x
    print 'Aqui comienza AGREGADO'
    print x.__class__.__name__
    print 'x[2999]= ', x[2999]
    print 'x[3000]= ', x[3000]
    x1  = 2999+1
    for xx in range(3000,6000):
        x[xx]  = x[xx] + 10
    for xx in range(6000,9000):
        x[xx]  = x[xx] + 20
    for xx in range(9000,12000):
        x[xx]  = x[xx] + 30
    for xx in range(12000,15000):
        x[xx]  = x[xx] + 40
    for xx in range(15000,18000):
        x[xx]  = x[xx] + 50
    for xx in range(18000,21000):
        x[xx]  = x[xx] + 60
    for xx in range(21000,24000):
        x[xx]  = x[xx] + 70
    for xx in range(24000,27000):
        x[xx]  = x[xx] + 80
    for xx in range(27000,30000):
        x[xx]  = x[xx] + 90
    for xx in range(30000,33000):
        x[xx]  = x[xx] + 100
    for xx in range(33000,36000):
        x[xx]  = x[xx] + 110
    for xx in range(36000,39000):
        x[xx]  = x[xx] + 120
    for xx in range(39000,42000):
        x[xx]  = x[xx] + 130
    for xx in range(42000,45000):
        x[xx]  = x[xx] + 140
    for xx in range(45000,48000):
        x[xx]  = x[xx] + 150
    for xx in range(48000,51000):
        x[xx]  = x[xx] + 160
        
    
    
    #-----------------------------------------

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
    ecg_peaks = -ecg_data[peaks_index]
    tm_peaks = x[peaks_index]
    tm_peaks = np.array(tm_peaks)
    print 'Indices: ', peaks_index
    print 'Picos Bajos: ', ecg_peaks
    
    ## Segundos entre intervalos
    rateBPM_values = []
    rateBPM_sum    = 0
    if len(peaks_index) > 9:  #minimo 10 ciclos
        for i in range(1,len(peaks_index)):
            t_dif = tm_peaks[i]-tm_peaks[i-1]
            rateBPM_values.append(t_dif) 
        rateBPM_sum = sum(rateBPM_values)
    
    ## BPM
    rateBPM = len(tm_peaks)*1.0 / (x[x.last_valid_index()]-x[0]) * 60.0
    print 'rateBPM: ', rateBPM
    print 'Valores rateBPM: ', rateBPM_values

    ## Mean R-R Interval
    rrmean_values = []
    rr_mean       = 0
    for i in range(0,len(rateBPM_values)):
        rr_mean = 0.75 * rr_mean + 0.25 * rateBPM_values[i]
        rrmean_values.append(rr_mean)

    up_rr_mean = np.where(rateBPM_values>=(rr_mean*1.15))
    down_rr_mean = np.where(rateBPM_values<(rr_mean*0.85))
    print 'RR-MEAN: ', rr_mean
    print 'UP-rr-mean', up_rr_mean
    print 'DOWN-rr-mean', down_rr_mean

    ## Resultado
    values = {'FA': False}
    if np.any(up_rr_mean):
        values['FA'] = True
    if np.any(down_rr_mean):
        values['FA'] = True
    
    values['rr_mean'] = rr_mean
    values['up_rr_mean'] = rr_mean*1.15
    values['down_rr_mean'] = rr_mean*0.85

    values['rateBPM'] = rateBPM
    values['cycles_num'] = len(peaks_index)
    values['cycles'] = []
    cycles = []
    for i in range(0,len(peaks_index)-1):
        cycles.append('Intervalo R-R #'+str(i+1)+' - #'+str(i+2) +': '+str(rateBPM_values[i]))
        
    values['cycles'] = cycles
    print cycles
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
    return plot_div, values




def signal_processing_backup(file_name):

    path = '/data/'
    df = pd.read_csv(settings.MEDIA_ROOT+path+file_name)

    try:
        x=df['x']
        y=df['y']
    except:
        df = pd.read_csv(settings.MEDIA_ROOT+path+file_name, sep=';')

    x=df['x']
    y=df['y']
    
    #-Agregado para aumentar tiempo 04-01-2018
    #print x
    print 'Aqui comienza AGREGADO'
    print x.__class__.__name__
    print 'x[2999]= ', x[2999]
    print 'x[3000]= ', x[3000]
    x1  = 2999+1
    for xx in range(3000,6000):
        x[xx]  = x[xx] + 10
    for xx in range(6000,9000):
        x[xx]  = x[xx] + 20
    for xx in range(9000,12000):
        x[xx]  = x[xx] + 30
    for xx in range(12000,15000):
        x[xx]  = x[xx] + 40
    for xx in range(15000,18000):
        x[xx]  = x[xx] + 50
    for xx in range(18000,21000):
        x[xx]  = x[xx] + 60
    for xx in range(21000,24000):
        x[xx]  = x[xx] + 70
    for xx in range(24000,27000):
        x[xx]  = x[xx] + 80
    for xx in range(27000,30000):
        x[xx]  = x[xx] + 90
    for xx in range(30000,33000):
        x[xx]  = x[xx] + 100
    for xx in range(33000,36000):
        x[xx]  = x[xx] + 110
    for xx in range(36000,39000):
        x[xx]  = x[xx] + 120
    for xx in range(39000,42000):
        x[xx]  = x[xx] + 130
    for xx in range(42000,45000):
        x[xx]  = x[xx] + 140
    for xx in range(45000,48000):
        x[xx]  = x[xx] + 150
    for xx in range(48000,51000):
        x[xx]  = x[xx] + 160
        
    
    
    #-----------------------------------------

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
    ecg_peaks = -ecg_data[peaks_index]
    tm_peaks = x[peaks_index]
    tm_peaks = np.array(tm_peaks)
    print 'Indices: ', peaks_index
    print 'Picos Bajos: ', ecg_peaks
    
    ## Segundos entre intervalos
    rateBPM_values = []
    rateBPM_sum    = 0
    if len(peaks_index) > 9:  #minimo 10 ciclos
        for i in range(1,len(peaks_index)):
            t_dif = tm_peaks[i]-tm_peaks[i-1]
            rateBPM_values.append(t_dif) 
        rateBPM_sum = sum(rateBPM_values)
    
    ## BPM
    rateBPM = len(tm_peaks)*1.0 / (x[x.last_valid_index()]-x[0]) * 60.0
    print 'rateBPM: ', rateBPM
    print 'Valores rateBPM: ', rateBPM_values

    ## Mean R-R Interval
    rrmean_values = []
    rr_mean       = 0
    for i in range(0,len(rateBPM_values)):
        rr_mean = 0.75 * rr_mean + 0.25 * rateBPM_values[i]
        rrmean_values.append(rr_mean)

    up_rr_mean = np.where(rateBPM_values>=(rr_mean*1.15))
    down_rr_mean = np.where(rateBPM_values<(rr_mean*0.85))
    print 'RR-MEAN: ', rr_mean
    print 'UP-rr-mean', up_rr_mean
    print 'DOWN-rr-mean', down_rr_mean

    ## Resultado
    values = {'FA': False}
    if np.any(up_rr_mean):
        values['FA'] = True
    if np.any(down_rr_mean):
        values['FA'] = True
    
    values['rr_mean'] = rr_mean
    values['up_rr_mean'] = rr_mean*1.15
    values['down_rr_mean'] = rr_mean*0.85

    values['rateBPM'] = rateBPM
    values['cycles_num'] = len(peaks_index)
    values['cycles'] = []
    cycles = []
    for i in range(0,len(peaks_index)-1):
        cycles.append('Intervalo R-R #'+str(i+1)+' - #'+str(i+2) +': '+str(rateBPM_values[i]))
        
    values['cycles'] = cycles
    print cycles
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
    return plot_div, values



#-----------PROCESSING PLOT-------------
def signal_processing(file_name):

    path = '/data/'
    df = pd.read_csv(settings.MEDIA_ROOT+path+file_name)

    try:
        x=df['x']
        y=df['y']
    except:
        df = pd.read_csv(settings.MEDIA_ROOT+path+file_name, sep=';')

    x=df['x']
    y=df['y']
    
    #-Agregado para aumentar tiempo 04-01-2018
    #print x
    print 'Aqui comienza AGREGADO'
    print x.__class__.__name__
    print 'x[2999]= ', x[2999]
    print 'x[3000]= ', x[3000]
    x1  = 2999+1
    for xx in range(3000,6000):
        x[xx]  = x[xx] + 10
    for xx in range(6000,9000):
        x[xx]  = x[xx] + 20
    for xx in range(9000,12000):
        x[xx]  = x[xx] + 30
    for xx in range(12000,15000):
        x[xx]  = x[xx] + 40
    for xx in range(15000,18000):
        x[xx]  = x[xx] + 50
    for xx in range(18000,21000):
        x[xx]  = x[xx] + 60
    for xx in range(21000,24000):
        x[xx]  = x[xx] + 70
    for xx in range(24000,27000):
        x[xx]  = x[xx] + 80
    for xx in range(27000,30000):
        x[xx]  = x[xx] + 90
    for xx in range(30000,33000):
        x[xx]  = x[xx] + 100
    for xx in range(33000,36000):
        x[xx]  = x[xx] + 110
    for xx in range(36000,39000):
        x[xx]  = x[xx] + 120
    for xx in range(39000,42000):
        x[xx]  = x[xx] + 130
    for xx in range(42000,45000):
        x[xx]  = x[xx] + 140
    for xx in range(45000,48000):
        x[xx]  = x[xx] + 150
    for xx in range(48000,51000):
        x[xx]  = x[xx] + 160
        
    
    
    #-----------------------------------------

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
    ecg_peaks = -ecg_data[peaks_index]
    tm_peaks = x[peaks_index]
    tm_peaks = np.array(tm_peaks)
    print 'Indices: ', peaks_index
    print 'Picos Bajos: ', ecg_peaks
    
    ## Segundos entre intervalos
    rateBPM_values = []
    rateBPM_sum    = 0
    if len(peaks_index) > 9:  #minimo 10 ciclos
        for i in range(1,len(peaks_index)):
            t_dif = tm_peaks[i]-tm_peaks[i-1]
            rateBPM_values.append(t_dif) 
        rateBPM_sum = sum(rateBPM_values)
    
    ## BPM
    rateBPM = len(tm_peaks)*1.0 / (x[x.last_valid_index()]-x[0]) * 60.0
    print 'rateBPM: ', rateBPM
    print 'Valores rateBPM: ', rateBPM_values

    ## Mean R-R Interval
    rrmean_values = []
    rr_mean       = 0
    for i in range(0,len(rateBPM_values)):
        rr_mean = 0.75 * rr_mean + 0.25 * rateBPM_values[i]
        rrmean_values.append(rr_mean)

    up_rr_mean = np.where(rateBPM_values>=(rr_mean*1.15))
    down_rr_mean = np.where(rateBPM_values<(rr_mean*0.85))
    print 'RR-MEAN: ', rr_mean
    print 'UP-rr-mean', up_rr_mean
    print 'DOWN-rr-mean', down_rr_mean

    ## Resultado
    values = {'FA': False}
    if np.any(up_rr_mean):
        values['FA'] = True
    if np.any(down_rr_mean):
        values['FA'] = True
    
    values['rr_mean'] = rr_mean
    values['up_rr_mean'] = rr_mean*1.15
    values['down_rr_mean'] = rr_mean*0.85

    values['rateBPM'] = rateBPM
    values['cycles_num'] = len(peaks_index)
    values['cycles'] = []
    cycles = []
    for i in range(0,len(peaks_index)-1):
        cycles.append('Intervalo R-R #'+str(i+1)+' - #'+str(i+2) +': '+str(rateBPM_values[i]))
        
    values['cycles'] = cycles
    print cycles
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
    return plot_div, values