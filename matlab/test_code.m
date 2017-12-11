clc; clear all;
close all;

%------ SPECIFY DATA ------------------------------------------------------
PATH= ''; % ruta donde se encuentran los archivos obtenidos de la WEB
numerosenal=111; %numero de senal a ser procesada

[x,TIME,DATAFILE]=lecturaecg(PATH,numerosenal);
y = x
yourArray = load('111m.mat');
t2 = yourArray(:,1)  % lets say it's a matrix
t3 = yourArray(1);
t4 = t3(:,1);
t5 = t3(1,:);
%x2 = yourArray(:,0)   


%------ Grafica de la señal ------------------------------------------------
figure(1); 
clf;
colordef(1,'black');
plot(TIME, x,'y');
xlim([TIME(1), TIME(end)]);
xlabel('Time / s'); ylabel('Voltage / mV');
string=['ECG signal ',DATAFILE];
title(string);
% -------------------------------------------------------------------------

figure(2); 
clf;
colordef(2,'black');
t = TIME(500:1500);
x = x(500:1500);
plot(t, x,'y');
xlim([TIME(500), TIME(1500)]);
xlabel('Time / s'); ylabel('Voltage / mV');
string=['ECG signal ',DATAFILE];
title(string);

[qrspeaks,locs] = findpeaks(x,t,'MinPeakHeight',0.3,...
    'MinPeakDistance',0.150);

figure(3)
plot(t,x)
title('R-Waves Localized by Wavelet Transform')
hold on
hwav = plot(locs,qrspeaks,'ro');
xlabel('Seconds')
%legend([hwav hexp],'Automatic','Expert','Location','NorthEast');
%total_signal = dlmread('D:\Documents\fiO!\Tesis\monitor\signals\ALL0005\F0005signal.CSV');
time = t;%total_signal(:,1);
%voltage = total_signal(:,2);
adjustedTime = time-time(1);
%plot(adjustedTime, voltage);
%figure(4)
%subplot(2,1,1),plot(adjustedTime, x); % plot(time,x);  %Senal Obtenida
%subplot(2,1,2), plot(conv(fir1(100,0.2), x)); %plot(conv(fir1(100,0.04), x)); %Senal Filtrada

%% Fourier
%y = fft(x);
%figure(5)
%plot(abs(y))

%% Ritmo Cardiaco (Promedio de 3)
indices_r = [];
for i = 1:length(locs)
    indices_r = [indices_r, find(t == locs(i)) ];
end

%Promedio de 3
tiempo_prom = locs(3)-locs(1);
num_ciclos  = length(locs);
bpm  = (num_ciclos * 60)/tiempo_prom;
freq = (num_ciclos * 1)/tiempo_prom;

fprintf('Numero de latidos por minuto: %f bpm\n', bpm)
fprintf('%f Hz \n', freq)

if (bpm > 100)
    fprintf('Presenta Arritmia\n')
else
    fprintf('Ritmo cardiaco Normal\n')
end

%% SENAL COMPLETA
t_final  = TIME(end);
t_inicio = TIME(1);
intervalo = 10; %segundos
index_cont = length(TIME)/intervalo;
index = 1+18000;
sub_time   = [];
figure_cont = 5;

for i = t_inicio : intervalo : 10%t_inicio : intervalo : t_final
    
    sub_time = TIME((index-index_cont):index);
    sub_y    = y((index-index_cont):index);
    
    [peaks,times] = findpeaks(sub_y,sub_time,'MinPeakHeight',0.3,...
    'MinPeakDistance',0.150);
  
    figure(figure_cont)
    %smoothECG = sgolayfilt(sub_y,7,21);
    [p,s,mu] = polyfit((1:numel(sub_y))',sub_y,6);
    f_y = polyval(p,(1:numel(sub_y))',[],mu);
    ECG_data = sub_y - f_y;        % Detrend data
    [peaks_ECG,times_ECG] = findpeaks(ECG_data,sub_time,'MinPeakHeight',0.45,...
    'MinPeakDistance',0.150);

    subplot(2,1,1); plot(sub_time,sub_y);
    xlim([sub_time(1), sub_time(end)]);
    subplot(2,1,2); plot(sub_time, ECG_data);
    xlim([sub_time(1), sub_time(end)]);
    hold on
    hwav = plot(times_ECG,peaks_ECG,'ro');
    legend([hwav],'Peaks');
    
    all_bpm = [];
    step1   = 2;
    for ii = 1 : step1 : (length(peaks_ECG)-2)
        tiempo_prom = times_ECG(ii+2)-times_ECG(ii);
        bpm  = ((step1+1) * 60)/tiempo_prom;
        all_bpm = [all_bpm bpm];
    end
    num_ciclos = length(peaks_ECG);
    bpm_prom = sum(all_bpm)/length(all_bpm)
    fprintf('La Figura(%i): \n', figure_cont)
    fprintf('Hay %f ciclos cardiacos\n', num_ciclos)
    fprintf('El Ritmo Cardiaco es(%f) bpm: \n', bpm_prom)
    
    index = index + index_cont;
    figure_cont = figure_cont + 1;
end
        
        