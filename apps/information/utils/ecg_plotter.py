# This script helps to plot ECG signals. 

import pandas as pd
from plotly import graph_objs
from plotly import tools
from plotly.offline import plot
from django.conf import settings

from scipy import signal
from scipy.signal import find_peaks_cwt
from numpy import polyfit
import numpy as np
import math

from .detect_peaks import detect_peaks

def frange(x, y, jump):
    '''
        Crea una lista de numeros para la division
        de la senal por ploques de jump segundos
    '''
    while x < y:
        yield x
        x += jump


def signal_processing(file_name, divide_plots=False):

    print('***************************************************')
    print('---------------------------------------------------')

    ## ---------------- Datos de Eventos PLOTS ---------------
    tiempos_plots = []
    bpm_plots     = []
    x_plots       = []
    y_plots       = []
    rrmean_values_plots = []
    rr_variability_plots = []
    rrmean_plots       = []
    rr_variabilitysum_plots = []

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
    rateBPM = 60

    ## ---------- ACONDICIONAMIENTO DE LOS VALORES X ----------
    # Entre 1000, porque asi son dados los valores
    x = np.array(x)
    y = np.array(y)
    # Para empezar en el segundo 5
    try:
        x = x[1500:10000]
        y = y[1500:10000]
    except:
        pass
    x = (x/1000.0)-1          # Para empezar desde 0 segundos
    y = y/1000.0
    
    # Inicio de muestra (segundos)
    x_inicio1 = x[0]
    x_decimal = x_inicio1-math.floor(x_inicio1)
    x_inicio = (x_decimal * 0.999) / 0.299  + math.floor(x_inicio1)   
    # Final de muestra (segundos)
    x_final1 = x[-1]
    x_decimal_fin = x_final1 - math.floor(x_final1)
    x_final = (x_decimal_fin * 0.999) / 0.299 + math.floor(x_final1)   
    
    # TIEMPO Total de la SENAL
    tiempo_total = x_final - x_inicio

    # Formamos el axis x (segundos) (CON ESTO PROCESAMOS)
    t = np.linspace(x_inicio, x_final, y.size, endpoint=True)
    # El Y para PLOT     (y_final)
    y_final = []

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
    segundos_bloque = 15.0
    sobra_bloque    = tiempo_total/segundos_bloque
    bloques         = list(frange(x_inicio, x_final, segundos_bloque))

    # contador de figuras
    cont_fig = 2

    # ultimo loop
    last_loop = False

    # Para R-R
    rr_values_all      = []
    rr_values_all_plot = []
    rr_mean_values_all = []
    rrmean_values = []
    rr_mean_prom       = 0
    rr_up_mean_values_all = []
    rr_down_mean_values_all = []
    RRv_all = []
    RRv_all_plot=[]
    rr_mean       = 0
    RRv_suma_all = []

    # Para saber si plotear ultima parte
    ploteosiono = False

    y_peaks=[]
    t_peaks = []
    picos_todos = []
    
    ## Resultado
    values = {'FA': False, 'ARRITMIA': False, 'ARRITMIA_GENERAL': False}
    values['suficiente_tiempo'] = True

    # PROCESAMIENTO:
    if tiempo_total > segundos_bloque:    # Por encima de  10 segundos (tiempo total)
        for i in bloques:
            # EVITAR bloque menor a 5 segundos
            ultimate_i = i + segundos_bloque     # Proximo bloque
            if (ultimate_i < x_final) and ((x_final-ultimate_i) < (segundos_bloque/2)):

                # Datos de BLOQUE
                indice_mayores = (i <= t)                       
                t_bloque_parcial = t[indice_mayores]            # Para t
                y_bloque_parcial = y[indice_mayores]            # Para y
                indice_menores = (t_bloque_parcial <= x_final)
                t_bloque = t_bloque_parcial[indice_menores]     # Para t
                y_bloque = y_bloque_parcial[indice_menores]     # Para y
                

                last_loop = True
            else:
                # Datos de BLOQUE
                indice_mayores = (i <= t)
                t_bloque_parcial = t[indice_mayores]            # Para t
                y_bloque_parcial = y[indice_mayores]            # Para y
                indice_menores = (t_bloque_parcial <= (i + segundos_bloque))
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
            
            y_smooth = signal.savgol_filter(y_bloque, framelen, order_sgolay)
            

            # DETREND (Quitar la tendecia de la senal)   (y_detrend)
            p = polyfit((np.arange(len(y_smooth))),y_smooth,6)
            f_y = np.polyval(p,(np.arange(len(y_smooth))))
            y_detrend = y_smooth - f_y


            # MULTIPLICACION por si misma
            y_var = y_detrend * y_detrend
            y_var = y_var * 100              # 10 (valor a milivoltios)
            y_normal = y_var


            # DETECCION de PICOS
            y_max = max(y_normal)

            # umbral minimo del pico de la senal
            min_peak_value = y_max*0.4
            
            # umbral minimo de pico (TEORICO)
            min_peak_value_theory = 0.2
            # Los picos deben ser si o si mayores a 0.29
            if not(min_peak_value >= min_peak_value_theory):
                print('El pico minimio es menor a '+str(min_peak_value_theory))
                min_peak_value = min_peak_value_theory
            # Picos: valores
            index_peaks = detect_peaks(y_normal, mph=min_peak_value, mpd=0.3, show=True)    # primer valor probado 0.150
            
            if index_peaks == []:
                break     
            t_peaks = t_bloque[index_peaks]           
            y_peaks = y_normal[index_peaks]

            #Colocar todos los picos:
            for peak in y_peaks:
                picos_todos.append(peak)
            
            # RR-VARIABILITY
            RRv_suma = 0
            RRv_variamucho = False
            minimo_variacion = 0.6    ##CAMBIAR? por el momento bien 0.6 1.5
            porcentaje_prematuridad = 0.78

            # RR - INTERVALOS
            rr_values    = []
            rr_promedio  = 0
            RRv_suma_porcentaje = []
            # RR-MEAN
            fuerade_rrmean = False

            # MINIMO 10 picos
            if (len(y_peaks)> 9):
                # RR - VARIABILITY
                for i2 in range(len(y_peaks)-2):
                    # No deberia haber variacion (RRv = 0)
                    RRv21 = (t_peaks[i2+1]-t_peaks[i2])
                    RRv32 = (t_peaks[i2+2]-t_peaks[i2+1])
                    RRv_suma = RRv_suma + abs(RRv32 - RRv21)
                    RRv_suma_all.append(abs(RRv32 - RRv21))   #Plots

                    # Porcentaje
                    if (1-(abs(RRv21-RRv32)/(RRv21))):
                        RRv_suma_porcentaje.append(abs(RRv32 - RRv21))

                if RRv_suma > minimo_variacion:
                    RRv_variamucho = True
                             

                # RR - INTERVALOS (segundos)
                for i3 in range(1,len(t_peaks)):
                    # se guarda valor intervalo RR
                    pulso_ant = t_peaks[i3-1]
                    pulso_act = t_peaks[i3]
                    rr_values.append(pulso_act - pulso_ant)
                
                #  de RRv para plot!!
                RRv_hahas = [RRv_suma]*len(rr_values)  ## REVISAR DESCOMENTAR
                #RRv_hahas = RRv_suma_sola*len(rr_values) 
                for RRv_haha in RRv_hahas:
                    RRv_all.append(RRv_haha)
                
                
                rr_suma = sum(rr_values)
                rr_promedio = sum(rr_values)/len(t_peaks)
                
                # Asignamos al rr_values total
                for rr_val in rr_values:                ## REVISAR!!
                    rr_values_all.append(rr_val)
                
                # MEAN R-R Interval (se toma rr_values anterior)
                rr_mean       = 0
                for i4 in range(0,len(rr_values)):
                    rr_mean = 0.75*rr_mean+0.25*rr_values[i4]
                rrmean_values = [rr_mean]*len(rr_values)
                # Asignamos al rr_mean valores totales
                for rrmean_value in rrmean_values:
                    rr_mean_values_all.append(rrmean_value)

                # Valores R-R Limites
                up_rr_true = []  # Los valores mayores a 
                up_mean_rrvalues = [i21 for i21 in rr_values if i21 >= (rr_mean*1.35)]  #2.5+0.5##ESSTO QUEDA
                
                down_rr_true = []  # Los valores mayores a 
                down_mean_rrvalues = [i22 for i22 in rr_values if i22 <= (rr_mean*0.85)]  #0.1-0.5

                
                if (len(up_mean_rrvalues) + len(down_mean_rrvalues)) > 1:
                    fuerade_rrmean = True
                elif up_mean_rrvalues or down_mean_rrvalues:
                    fuerade_rrmean = True


                # BEATS PER MIMUNTE
                rateBPM = len(y_peaks)*60.0/(t_bloque[-1]-t_bloque[0])
                #print('BPM: '+ str(rateBPM))

            # ---------------- FIBRILACION AURICULAR ----------------
            if (fuerade_rrmean==True) and (RRv_variamucho==True):
                values['FA'] = True
                tiempos_plots.append([t_bloque[0],t_bloque[-1]])
                x_plots.append(t_bloque)
                y_plots.append(y_smooth)
                rrmean_values_plots.append(rrmean_values)
                rr_variability_plots.append(rr_values)
                rr_variabilitysum_plots.append(RRv_suma_all)
                rrmean_plots.append(rr_mean)
                bpm_plots.append(rateBPM)
                values['ARRITMIA_GENERAL'] = True
            elif (fuerade_rrmean==True):
                values['ARRITMIA_GENERAL'] = True
            else:
                values['FA'] = False
                values['ARRITMIA'] = False

            # Para conteo de figuras
            cont_fig = cont_fig+1
            
            # Para formar el Y FINAL
            for y_i in y_detrend:
                y_final.append(y_i)

            # LOOP ULTIMO
            if last_loop:
                break
    

    else:
        values['suficiente_tiempo'] = False
        print('No se adquirio suficiente tiempo')


    values['rr_mean'] = rr_mean
    values['up_rr_mean'] = rr_mean*1.15
    values['down_rr_mean'] = rr_mean*0.85

    values['rateBPM'] = rateBPM
    values['cycles_num'] = len(picos_todos)
    values['cycles'] = []
    cycles = []
    values['tiempos_plots'] = tiempos_plots

    for i in range(0,len(y_peaks)-1):
        cycles.append('Intervalo R-R #'+str(i+1)+' - #'+str(i+2) +': '+str(rateBPM))
        
    values['cycles'] = cycles

    #--------------------------------------------------

    trace1 = graph_objs.Scatter(
                        x=t, y=y_final, 
                        mode='lines', name='signal'
                        )

    layout = graph_objs.Layout(title='ECG ('+file_name+')',
                   plot_bgcolor='rgb(230, 230,230)')
    

    ## ----------------- R-R MEAN Interval Plot --------------
    x_values_mean = range(0, len(rr_values_all))
    
    ups_mean = []
    for rr_up_mean in rr_mean_values_all:
        ups_mean.append(rr_up_mean*1.35) #2.5+0.5
    x_values_mean1 = range(0, len(ups_mean))

    downs_mean = []
    for down_up_mean in rr_mean_values_all:
        downs_mean.append(down_up_mean*0.85) #0.1-0.5
    x_values_mean2 = range(0, len(downs_mean))
    
    
    trace2 = graph_objs.Scatter(
        x=x_values_mean,
        y=rr_values_all,
        mode='markers',
        name='Intervalos MEAN R-R'
    )
    trace3 = graph_objs.Scatter(
        x=x_values_mean1,
        y=ups_mean,
        name='Limite MEAN R-R'
    )
    
    trace4 = graph_objs.Scatter(
        x=x_values_mean2,
        y=downs_mean,
        name='Limite MEAN R-R'
    )
    # -----------------------------------------------------

    # ----------------R-R Interval Plot--------------------
    x_values = range(0, len(rr_values_all))
    x_RRv_suma_all = range(0, len(RRv_suma_all))
    #rr_values_prom = sum(rr_values_all)/len(rr_values_all)
    
    rr_up = [1.1]*len(x_values)#[15]*len(x_values)
    rr_down = [0]*len(x_values)#[0]*len(x_values)

    trace5 = graph_objs.Scatter(
        x=x_values,
        y=RRv_suma_all,#RRv_all,
        mode='markers',
        name='Intervalos R-R'
    )
    trace6 = graph_objs.Scatter(
        x=[0, len(x_values)],
        y=rr_up,#[sum(RRv_all)/len(RRv_all)*1.15, sum(RRv_all)/len(RRv_all)*1.15],#y=rr_up_mean_values_all,
        name='Limite R-R'
    )
    trace7 = graph_objs.Scatter(
        x=[0, len(x_values)],
        y=rr_down,#[sum(RRv_all)/len(RRv_all)*0.85, sum(RRv_all)/len(RRv_all)*0.85],#y=[rr_mean_prom*0.85, rr_mean_prom*0.85],
        name='Limite R-R'
    )
                   
    data = [trace1, trace2, trace3, trace4, trace5]
    fig = tools.make_subplots(rows=3, cols=1, subplot_titles=('ECG', 'R-R Variabilidad'))
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 1)
    fig.append_trace(trace5, 3, 1)
    fig.append_trace(trace6, 3, 1)
    fig.append_trace(trace7, 3, 1)
    fig['layout']['xaxis1'].update(title='Segundos', range=[5, 15])
    fig['layout']['yaxis1'].update(title='Milivoltios')
    fig['layout']['plot_bgcolor']='rgb(230, 230,230)'
    fig['layout']['xaxis2'].update(title='Bloques')#, range=[0, len(x_values)] )
    fig['layout']['yaxis2'].update(title='R-R Intervalos')
    fig['layout']['xaxis3'].update(title='Bloques')#, range=[0, len(x_values)+5])
    
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    # Si no se requiere plots, enviar 2 variables
    if divide_plots==False:
        return plot_div, values

    # --------------- Plots de Eventos -----------------
    event_plots = []            #Plots de eventos
    plot_cont   = 0
    
    if len(tiempos_plots) > 0:
        for tiempos_plot in tiempos_plots:
            event_trace = graph_objs.Scatter(
                            x=x_plots[plot_cont],
                            y=y_plots[plot_cont],
                            mode='lines',
                            name = 'Evento Arritmico'
                        )

            x_rr_plots = range(0, len(rr_variability_plots))
            event_trace2 = graph_objs.Scatter(
                            x=x_rr_plots[plot_cont],
                            y=rr_variability_plots[plot_cont],
                            mode='markers',
                            name='Variabilidad R-R'
                        )

            rrmean_up_plots = []
            rrmean_up_plots.append(rrmean_plots[plot_cont]*1.35)
            rrmean_up_plots = rrmean_up_plots*len(rr_variability_plots[plot_cont])
            
            event_trace3 = graph_objs.Scatter(
                            x=[0, len(rrmean_up_plots)],
                            y=rrmean_up_plots,
                            name='Limite MEAN R-R'
                        )
            rrmean_down_plots = []
            rrmean_down_plots.append(rrmean_plots[plot_cont]*0.85)
            rrmean_down_plots = rrmean_down_plots*len(rr_variability_plots[plot_cont])
            
            event_trace4 = graph_objs.Scatter(
                            x=[0, len(rrmean_down_plots)],
                            y=rrmean_down_plots,
                            name='Limite MEAN R-R'
                        )

            #---------------------------------------------------------
            x_rrv_plots = range(0, len(rr_variabilitysum_plots[plot_cont]))
            rr_up_plots = [0.8]*len(x_rrv_plots)
            event_trace5 = graph_objs.Scatter(
                            x=x_rrv_plots[plot_cont],
                            y=rr_variabilitysum_plots[plot_cont],
                            mode='markers',
                            name='Suma de Variabilidad R-R'
                        )
            event_trace6 = graph_objs.Scatter(
                            x=[0, len(rr_up_plots)],
                            y=rr_up_plots,#[sum(RRv_all)/len(RRv_all)*1.15, sum(RRv_all)/len(RRv_all)*1.15],#y=rr_up_mean_values_all,
                            name='Limite R-R (propio)'
                        )

            subplot_titles = ('Evento: del segundo '+ str(int(tiempos_plot[0]))+' - al segundo '+str(int(tiempos_plot[1])), 
                                'R-R Variabilidad')
            event_fig = tools.make_subplots(rows=3, cols=1, subplot_titles=subplot_titles)
            event_fig.append_trace(event_trace, 1, 1)
            event_fig.append_trace(event_trace2, 2, 1)
            event_fig.append_trace(event_trace3, 2, 1)
            event_fig.append_trace(event_trace4, 2, 1)
            event_fig.append_trace(event_trace5, 3, 1)
            event_fig.append_trace(event_trace6, 3, 1)
            event_fig['layout']['xaxis1'].update(title='Segundos')
            event_plot = plot(event_fig, output_type='div', include_plotlyjs=False)
            event_plots.append(event_plot)
            plot_cont += 1
    # --------------------------------------------------
    return plot_div, values, event_plots