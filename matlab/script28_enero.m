%% SCRIPT FINAL TESIS 2018

clear all; close all; clc;

%% Se adquiere la SEÑAL
signal = load('nuevo4sinxy.csv');
x = signal(1:10000,1);
y = signal(1:10000,2);

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
% En milisegundos
taquicardia_mili = 600;   %Menor que 600 milisegundos
bradicardia_mili = 1000;  %Mayor que 1000 milisegundos

%% CONVERSION BITS
num_bits = 12;
max_volt = 3.3;
y = (max_volt * y)/(2^num_bits);

%% ACONDICIONAMIENTO DE LOS VALORES X
% Obtencion de decimales
x_decimales = x - floor(x);
% Para valor inicial    (x_inicio)
x_indexiniciales     = (x==x_inicio);
x_valoresiniciales   = x(x_indexiniciales);
x_decimalesiniciales = x_decimales(x_indexiniciales);
% Cuento cuantos numeros de decimales
cantidad_decimalesmin=0;
contador1 = 1;
while (floor(x*10^cantidad_decimalesmin)~=x*10^cantidad_decimalesmin)
    cantidad_decimalesmin = cantidad_decimalesmin + 1;
end
% Seleccion de x_inicio
if length(x_valoresiniciales) == 2
    x_inicio = floor(x_valoresiniciales(1)) + (x_decimalesiniciales(1)/100);
    if cantidad_decimalesmin > 1
        x_inicio = floor(x_valoresiniciales(1)) + (x_decimalesiniciales(1)/10);
    end
elseif  length(x_valoresiniciales) == 3
    x_inicio = floor(x_valoresiniciales(1)) + (x_decimalesiniciales(1)/100);
else
    x_inicio = floor(x_valoresiniciales(1)) + (x_decimalesiniciales(1)/100);
    if cantidad_decimalesmin > 1
        x_inicio = floor(x_valoresiniciales(1)) + (x_decimalesiniciales(1)/10);
    end
end
% Para valor final (x_final)
x_indexfinales     = (x==x_final);
x_valoresfinales   = x(x_indexfinales);
x_decimalesfinales = x_decimales(x_indexfinales);
% Cuento cuantos numeros de decimales
cantidad_decimalesmax=0;
contador2 = 1;
while (floor(x_valoresfinales(contador2)*10^cantidad_decimalesmax)~=x_valoresfinales(contador2)*10^cantidad_decimalesmax)
    cantidad_decimalesmax = cantidad_decimalesmax + 1;
end
% Seleccion de x_final
if length(x_valoresfinales)      == 2
    x_final = floor(x_valoresfinales(2)) + (x_decimalesfinales(2)/10);
    if cantidad_decimalesmax > 1 
        x_final = floor(x_valoresfinales(2)) + (x_decimalesfinales(2));
    end
elseif  length(x_valoresfinales) == 3
    x_final = floor(x_valoresfinales(3)) + (x_decimalesfinales(3));
else
    x_final = floor(x_valoresfinales(1)) + (x_decimalesfinales(1)/100);
    if cantidad_decimalesmax > 1
        x_final = floor(x_valoresfinales(1)) + (x_decimalesfinales(1)/10);
    end
end

% Entrego el verdadero TIEMPO (segundos)
t = linspace(x_inicio,x_final,(length(y)));


%% PROCESAMIENTO
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
        subplot(4,1,1)
        plot(t_bloque,y_smooth)
        title('Señal Suavizada')
        
        % DETREND (Quitar tendencia de la señal) (y_detrend)
        [p,s,mu] = polyfit((1:numel(y_smooth))',y_smooth,6);
        f_y = polyval(p,(1:numel(y_smooth))',[],mu);
        y_detrend = y_smooth - f_y;
        % Plot señal Detrend (Origen en CERO)
        figure(cont_fig)
        subplot(4,1,2)
        plot(t_bloque,y_detrend)
        title('Señal Detrend (CERO)')
        axis([t_bloque(1) t_bloque(end) min(y_detrend) 1])
        
        % VARIANZA                  (y_var)
        y_var = y_detrend.*y_detrend*10;
        % Plot de la señal con varianza
        figure(cont_fig)
        subplot(4,1,3)
        plot(t_bloque, y_var)
        title('Señal x Señal')
        axis([t_bloque(1) t_bloque(end) min(y_var) 1])
        y_normal = y_var;
        
        % NORMALIZAR             (y_normal)
        %y_normal = y_detrend/max(y_detrend);
        % Plot señal Normalizada
        %figure(cont_fig)
        %subplot(4,1,3)
        %plot(t_bloque, y_normal)
        %hold on
        %plot(t_bloque,y_var)
        %title('Señal Normalizada')
        %axis([t_bloque(1) t_bloque(end) min(y_normal) 1])
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        
        % DETECCION PICOS
        y_max = max(y_normal);
        % umbral minimo del pico de la señal
        min_peak_value = y_max*0.4;
        % umbral minimo de pico (TEORICO)
        min_peak_value_theory = 0.2;  
        % Los picos deben ser si o si mayores a 0.29
        if min_peak_value >= min_peak_value_theory
            fprintf('El pico maximo es mayor a %.3f\n', min_peak_value_theory)
        else
            fprintf('El pico maximo es menor a %.3f\n', min_peak_value_theory)
            min_peak_value = min_peak_value_theory;
        end
        % Picos: valores
        [y_peaks,t_peaks] = findpeaks(y_normal,t_bloque,'MinPeakHeight',min_peak_value,...
            'MinPeakDistance',0.3); % primer valor probado 0.150
        %Plot de picos
        figure(cont_fig);
        subplot(4,1,4);plot(t_bloque,y_normal)
        hold on
        hwav = plot(t_peaks,y_peaks,'ro');
        legend([hwav],'Picos');
        axis([t_bloque(1) t_bloque(end) min(y_normal) 1])
        fprintf('Numero de Picos: %d\n', length(y_peaks));
        
        %RR-Variability
        RRv_parcial = 0;
        RRv = 0;
        rateBPN_values = [];
        rateBPN_times  = [];
        rateBPN_sum    = 0 ;
        if (length(y_peaks)> 9)       %minimo 10
            for i2 = 1:(length(y_peaks)-2)
                RRv_parcial = RRv_parcial + abs((t_peaks(i2+2)-t_peaks(i2+1))-(t_peaks(i2+1)-t_peaks(i2)));
            end
            RRv = RRv_parcial/length(y_peaks);
            fprintf('RRv_parcial: %.3f\n', RRv_parcial);
            fprintf('RRv_promedio: %.3f\n', RRv);

            %Secs entre intervalos ?? REVISAR
            for i4 = 2:length(t_peaks)
                rateBPN_values = [rateBPN_values t_peaks(i4)-t_peaks(i4-1)];
            end
            rateBPN_sum = sum(rateBPN_values);
            fprintf('RRv_promedio: %.3f\n', rateBPN_sum);
        end

        % Para conteo de figuras
        cont_fig = cont_fig+1;
        

    end
  
else
    haha='(:'
end
    