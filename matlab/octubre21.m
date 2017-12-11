%% Prueba RDMAT con 1 min de senal
clear all; close all; clc;
[tm,signal,Fs,siginfo]=rdmat('08405m');
%04015m 08455m 08434m (error) 08405m (error) 08378m
sig_1 = signal(:,1);
sig_2 = signal(:,1); %%%%2

%% CSV file
%signal = load('ecg_mcv.csv');
%tm = signal(:,1)
%sig_1 = signal(:,2);
%sig_2 = signal(:,2);

%% Plot Senal
figure(1)
plot(tm,signal)
figure(2)
plot(tm, sig_1)
title('Derivada II')
figure(3)
smoothsig_2 = sgolayfilt(sig_2,7,21);
subplot(2,1,1); plot(tm,sig_2,'r')
title('Original Signal')
subplot(2,1,2); plot(tm,smoothsig_2,'r')
title('Smooth Signal')


%% Dividir la senal en bloques de 10 seg.
intervalo_seg = 10;       % bloques de n segundos
t_final = tm(end);
length_sig    = length(tm);
%intervalo_val = length_sig/intervalo_seg;
time1 = 0;
time2 = time1 + intervalo_seg;   %10
figure_cont = 4;
times_index = [];
for i1 = 1 : intervalo_seg : 60% (t_final+intervalo_seg) %60 aqui!
        
    %Hasta el numero
    tm1  = find(tm<time2);
    tm1  = tm(tm1);
    %Desde el numero
    tm1  = find(tm1>=time1);
    tm11 = tm(tm1);
    sig1 = smoothsig_2(tm1);
    
    %Detrend
    [p,s,mu] = polyfit((1:numel(sig1))',sig1,6);
    f_y = polyval(p,(1:numel(sig1))',[],mu);
    ECG_data = sig1 - f_y;                        % Detrend data
    
    %Picos bajos
    [peaks_ECG,times_ECG] = findpeaks(-ECG_data,tm11,'MinPeakHeight',0.9,...
    'MinPeakDistance',0.150);

    %Picos Altos
    [up_peaks,up_times] = findpeaks(ECG_data,tm11,'MinPeakHeight',0.9,...
    'MinPeakDistance',0.150);
    
    %RR-Variability
    RRv_parcial = 0;
    RRv = 0;
    rateBPN_values = [];
    rateBPN_times  = [];
    rateBPN_sum    = 0 ;
    if (length(peaks_ECG)> 9)       %minimo 10
        for i2 = 1:(length(peaks_ECG)-2)
            RRv_parcial = RRv_parcial + abs((times_ECG(i2+2)-times_ECG(i2+1))-(times_ECG(i2+1)-times_ECG(i2)));
        end
        RRv = RRv_parcial/length(peaks_ECG);
        
        %Secs entre intervalos
        for i4 = 2:length(times_ECG)
            rateBPN_values = [rateBPN_values times_ECG(i4)-times_ECG(i4-1)];
            %rateBPN_times  = [rateBPN_times (times_ECG(i4)+(times_ECG(i4)-times_ECG(i4-1))/2)];
        end
        rateBPN_sum = sum(rateBPN_values);
        %rateBPM = (rateBPN * 60) /(times_ECG(end)-times_ECG(1))
    end
    
    %BPM
    rateBPM = length(times_ECG)/(tm11(end)-tm11(1))*60;
    
    %Mean R-R Interval
    rrmean_values = [];
    rr_mean       = 0;
    for i5 = 1:length(rateBPN_values)
        rr_mean = 0.75*rr_mean+0.25*rateBPN_values(i5);
        rrmean_values = [rrmean_values rr_mean];
    end
    up_rr_mean   = find(rateBPN_values>=(rr_mean*1.15));
    down_rr_mean = find(rateBPN_values<(rr_mean*0.85));
    
    %Picos reales
    times_index = [];
    for i3 = 1:length(times_ECG)
        times_index = [times_index find(tm11==times_ECG(i3))];
    end
    
    %FFT
    Y = fft(ECG_data);
    freqHz = (0:1:length(abs(Y))-1)*Fs/length(Y);
    
    %Plot
    figure(figure_cont);
    subplot(4,1,1);plot(tm11,sig1)
    hold on
    hwav = plot(tm11(times_index),sig1(times_index),'ro');
    legend([hwav],'Peaks');
    
    subplot(4,1,2);plot(tm11,ECG_data)
    hold on
    hwav = plot(times_ECG,-peaks_ECG,'ro');
    legend([hwav],'Peaks');
    hold on
    hwav_up = plot(up_times,up_peaks,'go');
    legend([hwav_up],'Peaks');
    
    subplot(4,1,3);plot(rateBPN_values,'g*')
    title('R-R Intervals (sec)')
    hold on
    rrmean_plot = plot([0 length(rateBPN_values)],[rr_mean rr_mean]);
    xlim([0, length(rateBPN_values)])
    if rr_mean > 1
        ylim([0,1.5])
    else
        ylim([0,1])
    end
    hold on
    rrmean_plot = plot([0 length(rateBPN_values)],[rr_mean*0.85 rr_mean*0.85],'--r');
    hold on
    rrmean_plot = plot([0 length(rateBPN_values)],[rr_mean*1.15 rr_mean*1.15],'--r');
    
    subplot(4,1,4);plot(freqHz,(abs(Y)/length(Y)));
    xlim([0, 35])
    
    %Print
    fprintf('Ritmo cardiaco de Bloque #%i: %f\n', (figure_cont), RRv)
    fprintf('Numero de Picos: %i\n', length(times_ECG))
    fprintf('BPM: %i', floor(rateBPM))
    if (rateBPM > 100) || (length(up_rr_mean)>=1)||(length(down_rr_mean)>=1)
        fprintf(' ----> Arritmia FA\n', floor(rateBPM))
    else
        fprintf('\n')
    end
    %Actualizar valores
    time1 = time2;
    time2 = time2 + intervalo_seg;
    figure_cont = figure_cont+1;
end