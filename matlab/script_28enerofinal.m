%% SCRIPT FINAL TESIS 2018

clear all; close all; clc;

%% Se adquiere la SEÑAL
signal = load('9sinxy.csv');
x = signal(1501:15000,1);%signal(:,1);%(1:15000,1);
y = signal(1501:15000,2);%signal(:,2);%(1:15000,2);

% Frecuencia de Muestreo
Fs = 300; % (Hz)

%% ACONDICIONAMIENTO DE LOS VALORES X
% Entre 1000, porque asi son dados los valores
x = (x/1000)-1;
y = y/1000;

% Inicio
x_inicio1 = x(1);
x_decimal = x_inicio1 - floor(x_inicio1);
x_inicio = (x_decimal * 0.999)/0.299 + floor(x_inicio1);
% Final
x_final1  = x(end);
x_decimal_fin = x_final1 - floor(x_final1);
x_final = (x_decimal_fin*0.999)/0.299 + floor(x_final1);

% TIEMPO Total de SEÑAL 
tiempo_total = x_final-x_inicio;

% Formamos el axis x (segundos) (CON ESTO PROCESAMOS)
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


%% PROCESAMIENTO
% Por encima de 10 segundos (tiempo total)
segundos_bloque = 10;
sobra_bloque    = tiempo_total/segundos_bloque;

% contador de figures
cont_fig = 2;

% ultimo loop
last_loop = false;

% Para R-R
rr_values_all = []
rr_mean_values_all = [];
rr_mean_prom = 0

% Para saber si plotear ultima parte
ploteosiono = false;

% PROCESAMIENTO:

if tiempo_total > segundos_bloque % Por encima de 10 segundos (tiempo total)
    
    for i = (x_inicio : segundos_bloque : x_final) % Va de 10 en 10 segs
        
        % EVITAR bloque menor a 5 segundos
        ultimate_i = i + segundos_bloque; % Prox bloque
        if (ultimate_i < x_final) && ((x_final - ultimate_i) < (segundos_bloque/2))
                  
            % Datos de BLOQUE
            indice_mayores = (i <= t);
            t_bloque_parcial = t(indice_mayores); % Para t
            y_bloque_parcial = y(indice_mayores); % Para y
            indice_menores = (t_bloque_parcial <= x_final);
            t_bloque = t_bloque_parcial(indice_menores);  % Para t
            y_bloque = y_bloque_parcial(indice_menores);  % Para y
            
            last_loop = true;
        else
            % Datos de BLOQUE
            indice_mayores = (i <= t);
            t_bloque_parcial = t(indice_mayores); % Para t
            y_bloque_parcial = y(indice_mayores); % Para y
            indice_menores = (t_bloque_parcial < (i + segundos_bloque));
            t_bloque = t_bloque_parcial(indice_menores);  % Para t
            y_bloque = y_bloque_parcial(indice_menores);  % Para y
        end
        
      
        % Filtro SALVITZKY para reducir Ruido (y_smooth)
        order_sgolay = 7;
        framelen = 21;
        % Asegurar que la cantidad de y_bloque es mayor que framelen
        if not(length(y_bloque) > framelen)
            order_sgolay = length(y_bloque)-2;
            framelen = length(y_bloque)-1;
            % Solo is es odd (impar) : order_sgolay < framelen
            if rem(framelen,2) ~= 1
                order_sgolay = order_sgolay-1;
                framelen = framelen-1;
            end
            fprintf('Se cambio el orden de Savitzky Golay\n')
        end
        y_smooth = sgolayfilt(y_bloque,order_sgolay,framelen);
        % Plot señal Suavizada
        figure(cont_fig)
        subplot(4,1,1)
        plot(t_bloque,y_smooth)
        title('Señal Suavizada')
        axis([t_bloque(1) t_bloque(end) min(y_smooth) max(y_smooth)])
        grid on
        
        
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
        grid on
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
        if not(min_peak_value >= min_peak_value_theory)
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
        
        
        % RR-VARIABILITY
        RRv_suma = 0;
        RRv_variamucho = false;
        minimo_variacion = 0.6;
        
        % RR - INTERVALOS
        rr_values    = [];
        rr_promedio  = 0;
        
        % RR-MEAN
        fuerade_rrmean = false;
        
        % MINIMO 10 picos
        if (length(y_peaks)> 9)       
            
            % Para Saber si PLOTEA (PLOT R-R Mean)
            ploteosiono = true;
            
            % RR - VARIABILITY
            for i2 = 1:(length(y_peaks)-2)
                % No deberia haber variacion (RRv = 0)
                RRv21 = (t_peaks(i2+1)-t_peaks(i2));
                RRv32 = (t_peaks(i2+2)-t_peaks(i2+1));
                RRv_suma = RRv_suma + abs(RRv32 - RRv21);
                % Intervalos RR varian mucho?
                if RRv_suma > minimo_variacion
                    RRv_variamucho = true;
                end
            end
            
            % RR - INTERVALOS (segundos)
            for i3 = 2:length(t_peaks)
                % se guarda valor intervalo RR
                pulso_ant = t_peaks(i3-1);
                pulso_act = t_peaks(i3);
                rr_values = [rr_values (pulso_act - pulso_ant)];
            end
            rr_suma = sum(rr_values);
            rr_promedio = sum(rr_values)/length(t_peaks);
            fprintf('RR valores SUMA: %.3f\n', rr_suma);
            fprintf('RR Intervalo promedio: %.3f\n', rr_promedio);
            % Asignamos al rr_values total
            rr_values_all = [rr_values_all rr_values];
            
            % MEAN R-R Interval (se toma rr_values anterior)
            rrmean_values = [];
            rr_mean       = 0;
            for i4 = 1:length(rr_values)
                rr_mean = 0.75*rr_mean+0.25*rr_values(i4);
                rrmean_values = [rrmean_values rr_mean];
            end
            % Valores R-R Limites
            up_rr_mean   = find(rr_values>=(rr_mean*1.15));
            down_rr_mean = find(rr_values<(rr_mean*0.85));
            if (length(up_rr_mean) + length(down_rr_mean)) > 1
                fuerade_rrmean = true;
            end
            % Asignamos al rr_mean valores totales
            rr_mean_values_all = [rr_mean_values_all rr_mean];
            
            % BEATS PER MIMUNTE
            rateBPM = floor(length(y_peaks)*60/(t_bloque(end)-t_bloque(1)));
            fprintf('BPM: %d\n', rateBPM);

        end
        
        
        if (fuerade_rrmean==true) || (RRv_variamucho==true)
            fprintf('Presenta FA\n', floor(rateBPM))
        else
            fprintf('No presenta FA\n')
        end

        
        % Para conteo de figuras
        cont_fig = cont_fig+1;
        
        % LOOP ULTIMO
        if last_loop
            break
        end

    end
    
    if ploteosiono == true
        %% PLOT R-R Mean
        rr_mean_prom = sum(rr_mean_values_all)/length(rr_mean_values_all);
        figure(cont_fig)
        plot(rr_values_all,'g*')
        title('R-R Total Variability')
        ylabel('R-R Intervalos segundos')
        xlabel('Numero de Bloques (10 segundos)')
        % Limite RR-Mean Promedio
        hold on
        rrmean_plot = plot([0 length(rr_values_all)],[rr_mean_prom rr_mean_prom]);
        % Limite RR-Mean Inferior
        hold on
        rrmean_plot = plot([0 length(rr_values_all)],[rr_mean_prom*0.85 rr_mean_prom*0.85],'--r');
        % Limite RR-Mean Superior
        hold on
        rrmean_plot = plot([0 length(rr_values_all)],[rr_mean_prom*1.15 rr_mean_prom*1.15],'--r');
        xlim([0, length(rr_values_all)])
        ylim([(rr_mean_prom*0.85) - 0.1, (rr_mean_prom*1.15) + 0.1])
    end
    
else
    fprinf('No se adquirio suficiente tiempo')
end