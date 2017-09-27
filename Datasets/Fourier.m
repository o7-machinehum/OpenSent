%Todo
%-------------------------------------------------------------
% 1. Implement Filename into plot titles
%-------------------------------------------------------------
pkg load signal;

clc; clear;

FontS = 20;

%File location
%-------------------------------------------------------------
filename = 'Sept/Sept19-26.csv';
M = csvread(filename);

%Defining placements
%-------------------------------------------------------------
BTCticker = 3;
BTCvol = 4;
BTCsen = 5;
BTCcost = 6;

LTCticker = 7;
LTCvol = 8;
LTCsen = 9;
LTCcost = 10;

Cost = M(1:end, BTCcost);
Sen = M(1:end, BTCsen);
Vol = M(1:end, BTCvol);

%Cost = M(1:end, LTCcost);
%Sen = M(1:end, LTCsen);

titleRaw = 'Cost of Bitcoin vs. Bitcoin Sentiment';
titleDer = 'Cost of Bitcoin vs. (d/dt)Bitcoin Sentiment';

%Filtering
%-------------------------------------------------------------
windowSize = 150; 
bb = (1/windowSize)*ones(1,windowSize);
aa = 1;

[b,a]=butter(3, 0.01);
filteredSen = filter(b,a,Sen);
filteredCost = filter(bb,aa,Cost);
filteredVol = filter(b,a,Vol);

%For some reason the average filter fucks up the first little bit
Cost(1:windowSize) = [];
filteredSen(1:windowSize) = [];
filteredCost(1:windowSize) = [];
filteredVol(1:windowSize) = [];

%Normalise
%-------------------------------------------------------------
normSen = filteredSen - min(filteredSen); %Normalize
normSen = normSen.*(1/max(normSen));
normCost = filteredCost - min(filteredCost); %Normalize
normCost = normCost.*(1/max(normCost));

%Move signal into fourier space
%-------------------------------------------------------------
T = 30; % Sampling period       
Fs = 1/T; % Sampling frequency                    
L = length(filteredCost); % Length of signal
t = (0:L-1)*T; % Time vector

fftCost = fft(filteredCost);
fftSen = fft(filteredSen);

fftCost(1:1000) = [];
fftSen(1:10) = [];

P2cost = abs(fftCost/L);
P1cost = P2cost(1:L/2+1);
P1cost(2:end-1) = 2*P1cost(2:end-1);

P2sen = abs(fftSen/L);
P1sen = P2sen(1:L/2+1);
P1sen(2:end-1) = 2*P1sen(2:end-1);

f = Fs*(0:(L/2))/L;
plot(f,P1cost, f, P1sen);

break;

plot(t, filteredCost);
title('Mean result time shifted correlation of Cost(Normalised) & Sentiment(Normalised)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);
