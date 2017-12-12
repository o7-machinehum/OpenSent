#!/usr/bin/octave-cli --persist

%Todo
%-------------------------------------------------------------
% 1. Implement Filename into plot titles
%-------------------------------------------------------------
pkg load signal;

clc; clear;

FontS = 20;

%File location
%-------------------------------------------------------------
%filename = 'Sept/Sept17-18.csv';
%filename = 'Sept/Sept17_2017.csv';
%filename = 'Sept/Sept19-21.csv';
%filename = 'Sept/Sept19-26.csv';
%filename = 'Sept/Sept20_2017.csv';
%filename = 'Sept/Sept17_2017.csv';

%filename = 'Oct/Sept29-Oct1.csv';
%filename = 'Oct/Oct9.csv';
filename = 'Dec/Dec01.csv';


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

ETHticker = 11;
ETHvol = 12;
ETHsen = 13;
ETHcost = 14;

Cost = M(1:end, BTCcost);
Sen = M(1:end, BTCsen);
Vol = M(1:end, BTCvol);

%Cost = M(1:end, LTCcost);
%Sen = M(1:end, LTCsen);

titleRaw = 'Cost of Bitcoin vs. Bitcoin Sentiment';
titleDer = 'Cost of Bitcoin vs. (d/dt)Bitcoin Sentiment';

x = 0:length(M) - 1;
x2 = 0:length(M) - 1;

%Filtering
%-------------------------------------------------------------
windowSize = 50; 
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
x(1:windowSize) = [];
x2(1:windowSize) = [];

%Normalise
%-------------------------------------------------------------
normSen = filteredSen .* (1 / max(filteredSen)); %Normalize
normVol = filteredVol .* (1 / max(filteredVol)); %Normalize
normCost = Cost .* (1 / max(Cost)); %Normalize

%Initial Plotting (Raw)
%-------------------------------------------------------------
figure(1)
ax = plotyy(x, filteredCost, x2, filteredSen);
title(titleRaw, 'FontSize', FontS);
ylabel(ax(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax(2), 'Crypto Sentiment', 'FontSize', FontS);
legend('Cost', 'Sentiment')

%Initial Plotting (Diff)
%-------------------------------------------------------------
figure(2)
x3 = x;
x3(end) = [];
ax = plotyy(x3, diff(filteredCost), x3, diff(filteredSen));
title(titleDer, 'FontSize', FontS);
ylabel(ax(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax(2), 'Crypto Sentiment', 'FontSize', FontS);
legend('Cost', 'Sentiment')
