# This script helps to plot ECG signals. 

import pandas as pd
from plotly import graph_objs
from plotly.offline import plot
from django.conf import settings

from scipy import signal
from scipy.signal import find_peaks_cwt
from numpy import polyfit
import numpy as np
import math

from detect_peaks import detect_peaks

def frange(x, y, jump):
    '''
        Crea una lista de numeros para la division
        de la senal por ploques de jump segundos
    '''
    while x < y:
        yield x
        x += jump


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
    peaks_index = detect_peaks(ecg_data, mph=0.6, mpd=0.150, show=True)#detect_peaks(-ecg_data, mph=0.6, mpd=0.150, show=True)
    ecg_peaks = ecg_data[peaks_index]#-ecg_data[peaks_index]
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
    peaks_index = detect_peaks(-ecg_data, mph=0.4, mpd=0.150, show=True)
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
def signal_processing_backupULTIMO(file_name):

    path = '/data/'
    df = pd.read_csv(settings.MEDIA_ROOT+path+file_name)

    try:
        x=df['X']
        y=df['Y']
    except:
        df = pd.read_csv(settings.MEDIA_ROOT+path+file_name, sep=';')

    x=df['X']
    y=df['Y']
    
    #-Agregado para aumentar tiempo 04-01-2018
    #print x
    """print 'Aqui comienza AGREGADO'
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
    """
    #-----------Agregado el 18 de enero 2018----------
    x           = np.array(x)
    y           = np.array(y)
    
    x           = x-1             # Para que comience en 0 (cero) segundos

    x_inicial   = x[0]    # Inicio de muestra (segundos)
    x_final     = x[-1]     # Fin de muestra (segundos)
    
    total_tiempo = x_final-x_inicial 
    fs           = 300.0
    sec_sample   = 1.0/fs

    tiempo_muestra = []
    multi          = 0

    for yy in  y:
        tiempo_muestra.append(sec_sample*multi)
        multi += 1
    x = np.array(tiempo_muestra)
    #--------------------------------------------------

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
    peaks_index = detect_peaks(ecg_data, mph=0.6, mpd=0.150, show=True)
    ecg_peaks = ecg_data[peaks_index]
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
    rateBPM = len(tm_peaks)*1.0 / (x[-1]-x[0]) * 60.0
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



#----------------------------------------------------------
# ESTE ES EL SCRIPT CON LA NUEVA CONF
#-----------PROCESSING PLOT-------------
def signal_processing(file_name):

    ## ---------------- Se adquiere la senal -----------------
    path = '/data/'
    df = pd.read_csv(settings.MEDIA_ROOT+path+file_name)

    try:
        x=df['X']
        y=df['Y']
    except:
        df = pd.read_csv(settings.MEDIA_ROOT+path+file_name, sep=';')

    x=df['X']
    y=df['Y']
    
    # Frecuencia de Muestro
    Fs = 300

    ## ---------- ACONDICIONAMIENTO DE LOS VALORES X ----------
    # Entre 1000, porque asi son dados los valores
    x = np.array(x)
    y = np.array(y)
    # Para empezar en el segundo 5
    x = x[1500:-1]
    y = y[1500:-1]
    x = (x/1000.0)-1          # Para empezar desde 0 segundos
    y = y/1000.0

    # Inicio de muestra (segundos)
    x_inicio1 = x[0]
    x_decimal = x_inicio1-math.floor(x_inicio1)
    x_inicio = (x_decimal * 0.999) / 0.299  + math.floor(x_inicio1)    ## PREGUNTAR
    # Final de muestra (segundos)
    x_final1 = x[-1]
    x_decimal_fin = x_final1 - math.floor(x_final1)
    x_final = (x_decimal_fin * 0.999) / 0.299 + math.floor(x_final1)   ## PREGUNTAR
    
    # TIEMPO Total de la SENAL
    tiempo_total = x_final - x_inicio

    # Formamos el axis x (segundos) (CON ESTO PROCESAMOS)
    t = np.linspace(x_inicio, x_final, y.size, endpoint=True)

    ## -------------------- Datos ---------------------
    # BPM (Latidos por MINUTO (60 segundos))
    taquicardia = 100.0                   # Mayor que
    bradicardia = 60.0                    # Menor que
    # Separacion de PICOS (1 Hz - 1.667 Hz (2 Hz))
    taquicardia_seg = 60/taquicardia    # Menor que 0.6 segundos
    bradicardia_seg = 60/bradicardia    # Mayor que 1.0 segundos
    # En milisegundos
    taquicardia_mili  = 600.0             # Menor que 600 milisegundos
    bradicardia_mili  = 1000.0            # Mayor que 1000 milisegundos

    ## ------------- CONVERSION DE BITS ---------------  
    num_bits = 12.0
    max_volt = 3.3
    y = (max_volt * y)/(2^int(num_bits))
    #--------------------------------------------------

    ## --------------- PROCESAMIENTO -----------------
    # Por encima de 10 segundos (tiempo total)
    segundos_bloque = 10.0
    sobra_bloque    = tiempo_total/segundos_bloque
    bloques         = list(frange(x_inicio, x_final, segundos_bloque))

    # contador de figuras
    cont_fig = 2

    # ultimo loop
    last_loop = False

    # Para R-R
    rr_values_all      = []
    rr_mean_values_all = []
    rr_mean_prom       = 0

    # Para saber si plotear ultima parte
    ploteosiono = False

    # PROCESAMIENTO:
    if tiempo_total > segundos_bloque:    # Por encima de  10 segundos (tiempo total)
        for i in bloques:
            # EVITAR bloque menor a 5 segundos
            ultimate_i = i + segundos_bloque     # Proximo bloque
            if (ultimate_i < x_final) and ((x_final-ultimate_i) < (segundos_bloque/2)):

                # Datos de BLOQUE
                indice_mayores = (i <= t)                       # Para t
                t_bloque_parcial = t[indice_mayores]            # Para y
                indice_menores = (t_bloque_parcial <= x_final)
                t_bloque = t_bloque_parcial[indice_menores]     # Para t
                y_bloque = y_bloque_parcial[indice_menores]     # Para y

                last_loop = True
            else:
                # Datos de BLOQUE
                indice_mayores = (i <= t)
                t_bloque_parcial = t[indice_mayores]            # Para t
                y_bloque_parcial = y[indice_mayores]            # Para y
                indice_menores = (t_bloque_parcial < (i + segundos_bloque))
                t_bloque = t_bloque_parcial[indice_menores]     # Para t
                y_bloque = y_bloque_parcial[indice_menores]     # Para y

             
            # Filtro SALVITZKY para reducir ruido (y_smooth)
            order_sgolay = 7
            framelen = 21
            # Asegurar que la cantidad de y_bloque es mayor que framelen
            if not(len(y_bloque) > framelen):
                order_sgolay = len(y_bloque)-2
                framelen = len(y_bloque)-1
                # Solo is es odd (impar) : order_sgolay < framelen
                if (framelen%2) != 1:
                    order_sgolay = order_sgolay-1;
                    framelen = framelen-1
                print('Se cambio el orden de Savitzky Golay\n')
            
            print '?????'
            print y_bloque.size
            print order_sgolay
            print framelen
            y_smooth = signal.savgol_filter(y_bloque, framelen, order_sgolay)
            

            # DETREND (Quitar la tendecia de la senal)   (y_detrend)
            p = polyfit((np.arange(len(y))),y,6)
            f_y = np.polyval(p,(np.arange(len(y))))
            y_detrend = y_smooth - f_y


            # MULTIPLICACION por si misma
            y_var = y_detrend * y_detrend
            y_var = y_var * 10              # 10 (valor a milisegundos)
            y_normal = y_var

            # NORMALIZAR             (y_normal)
            #y_normal = y_detrend/max(y_detrend)

            # DETECCION de PICOS
            y_max = max(y_normal)
            # umbral minimo del pico de la senal
            min_peak_value = y_max*0.4
            # umbral minimo de pico (TEORICO)
            min_peak_value_theory = 0.2


    else:
        print('No se adquirio suficiente tiempo')
    
    ##################################################
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
    peaks_index = detect_peaks(ecg_data, mph=0.6, mpd=0.150, show=True)
    ecg_peaks = ecg_data[peaks_index]
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
    rateBPM = len(tm_peaks)*1.0 / (x[-1]-x[0]) * 60.0
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