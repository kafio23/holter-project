%% SCRIPT FINAL TESIS 2018

clear all; close all; clc;

%% Se adquiere la SEÑAL
signal = load('nuevo4sinxy.csv');
x = signal(1:7000,1);
y = signal(1:7000,2);

% Frecuencia de Muestreo
Fs = 300; % (Hz)

% señal comienza en 1. Le restamos.
x = x-1;
x_inicio = x(1);
x_final  = x(end);
tiempo_total = [x_final-x_inicio];

% Formamos el axis x (segundos)
t = linspace(x_inicio,x_final,(length(y)));

% Ploteo toda la TODA señal
figure(1)
plot(t,y)
title('Señal Completa Cruda')

%% Datos:
% BPM (Latidos por MINUTO (60 segundos))
taquicardia = 100;      % Mayor que
bradicardia = 60;       % Menor que 0.8683
% Separacion de PICOS ( 1 Hz - 1.667 Hz (2 Hz))
taquicardia_seg = 60/taquicardia;  %Menor que 0.6 segs
bradicardia_seg = 60/bradicardia;  %Mayor que 1.0 segs

%% PROCESAMIENTO

% Conversion de BITS
num_bits = 12;
max_volt = 3.3;
y = (max_volt * y)/(2^num_bits);

% Por encima de 10 segundos (tiempo total)
segundos_bloque = 10;
sobra_bloque    = tiempo_total/segundos_bloque;

% contador de figures
cont_fig = 2;

if tiempo_total > segundos_bloque % Por encima de 10 segundos (tiempo total)
    
    for i = (x_inicio : segundos_bloque : x_final) % Va de 10 en 10 segs
        
        % Datos de BLOQUE
        indice_mayores = (i <= t);
        t_bloque_parcial = t(indice_mayores); % Para t
        y_bloque_parcial = y(indice_mayores); % Para y
        indice_menores = (t_bloque_parcial < (i + segundos_bloque));
        t_bloque = t_bloque_parcial(indice_menores);  % Para t
        y_bloque = y_bloque_parcial(indice_menores);  % Para y
        
        % Filtro SALVITZKY para reducir Ruido (y_smooth)
        y_smooth = sgolayfilt(y_bloque,7,21);
        % Plot señal Suavizada
        figure(cont_fig)
        subplot(3,1,1)
        plot(t_bloque,y_smooth)
        title('Señal Suavizada')
        
        % DETREND (Quitar tendencia de la señal) (y_detrend)
        [p,s,mu] = polyfit((1:numel(y_smooth))',y_smooth,6);
        f_y = polyval(p,(1:numel(y_smooth))',[],mu);
        y_detrend = y_smooth - f_y;
        % Plot señal Detrend (Origen en CERO)
        figure(cont_fig)
        subplot(3,1,2)
        plot(t_bloque,y_detrend)
        title('Señal Detrend (CERO)')
        
        % NORMALIZAR             (y_normal)
        y_normal = y_detrend/max(y_detrend);
        % Plot señal Normalizada
        figure(cont_fig)
        subplot(3,1,3)
        plot(t_bloque,y_normal)
        title('Señal Normalizada')
        
        % Para conteo de figuras
        cont_fig = cont_fig+1;
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        
        % DETECCION PICOS
        y_max = max(y_normal);
        % umbral minimo del pico
        min_peak_value = y_max*0.6;
        % Picos: valores
        [y_peaks,t_peaks] = findpeaks(y_normal,t_bloque,'MinPeakHeight',min_peak_value,...
            'MinPeakDistance',0.150);

    end
  
else
    haha='(:'
end