#!/usr/bin/octave-cli --persist

%Todo
%-------------------------------------------------------------
% 1. Implement Filename into plot titles
%-------------------------------------------------------------
pkg load signal;

clc; clear;

%Parameters
%-------------------------------------------------------------
FontS = 20;
ShiftMethod = 'diff'; %Differential shift method
%ShiftMethod = 'mag'; %Magnitude shift method
%ShiftMethod = 'man'; %Manual shift method
grid on

MaxShifthr = 5;
MaxShiftel = MaxShifthr*60*2;

MinShifthr = 1; %Lets ignore a possible time lag less than 1hr
MinShiftel = MinShifthr*60*2;

%File location
%-------------------------------------------------------------
%filename = 'Sept/Sept17-18.csv';
%filename = 'Sept/Sept17_2017.csv';
%filename = 'Sept/Sept19-21.csv';
%filename = 'Sept/Sept19-26.csv';
%filename = 'Sept/Sept20_2017.csv';
%filename = 'Sept/Sept17_2017.csv';

%filename = 'Oct/Sept29-Oct1.csv';
%filename = 'Oct/Oct2.csv';
%filename = 'Oct/Oct3.csv';
%filename = 'Oct/Oct4.csv';
%filename = 'Oct/Oct5.csv';
%filename = 'Oct/Oct6.csv';
%filename = 'Oct/Oct7.csv';
%filename = 'Oct/Oct9.csv';
%filename = 'Oct/Oct10.csv';
%filename = 'Oct/Oct11.csv';
filename = 'Oct/Oct12.csv';

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
%x(1:windowSize) = [];
%x2(1:windowSize) = [];

%Normalise
%-------------------------------------------------------------
normSen = filteredSen - min(filteredSen); %Normalize
normSen = normSen.*(1/max(normSen));
normCost = filteredCost - min(filteredCost); %Normalize
normCost = normCost.*(1/max(normCost));

%Find time lag
%-------------------------------------------------------------
len = MaxShiftel;

%Temp values
TempCost = normCost;
TempSen = normSen;

for i = 1:len
	TempCost(1) = [];
	TempSen(end) = [];
	meanResult(i) = mean(TempCost - TempSen);
end

figure(1)
plot(meanResult);
grid on

title('Mean result time shifted correlation of Cost(Normalised) & Sentiment(Normalised)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

%Find time lag ds/dt
%-------------------------------------------------------------
lenDer = MaxShiftel; %Max 5hr delay


TempCost = diff(normCost);
TempSen = diff(normSen);

for i = 1:lenDer
	TempCost(1) = [];
	TempSen(end) = [];
	meanResultdiff(i) = mean(abs(TempCost - TempSen));
end

figure(2)
plot(meanResultdiff);
grid on
title('Mean result time shifted correlation of dCost/dt(norm) and dSen/dt(norm)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

%break; %Break here - look at both plots then decide what lag to use

%Apply Lag
%-------------------------------------------------------------
x = 0:length(Cost) - 1;
x2 = 0:length(Cost) - 1;

if strcmp(ShiftMethod, 'man')
	lag = 400; %Manual lag
	tit = strcat('Manual lag of:', num2str(lag*30/3600), 'hrs');
elseif strcmp(ShiftMethod, 'mag')
	lag = find(meanResult == min(meanResult(MinShiftel:end)));
	tit = strcat('Magnutude numarical method used lag of:', num2str(lag*30/3600), 'hrs');
else
	lag = find(meanResultdiff == min(meanResultdiff(MinShiftel:end)));
	tit = strcat('Numarical derivative method used lag of:', num2str(lag*30/3600), 'hrs');
end

tit = strcat(tit, filename);

x2 = x2 + lag;

figure(1)
ax2 = plotyy(x, filteredCost - mean(filteredCost), x2, filteredSen - mean(filteredSen));
grid on
legend('Cost', 'Sentiment (timeshifted)');
title(tit, 'FontSize', FontS);
xlabel('Time', 'FontSize', FontS);
ylabel(ax2(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax2(2), 'Crypto Sentiment', 'FontSize', FontS);

%Taking derive remove element
x(end) = [];
x2(end) = [];

tit = strcat('diff',tit);
figure(2)
ax2 = plotyy(x, diff(filteredCost), x2, diff(filteredSen));
grid on
legend('dCost/dt', 'dSentiment/dt (timeshifted)');
title(tit, 'FontSize', FontS);
xlabel('Time', 'FontSize', FontS);
ylabel(ax2(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax2(2), 'Crypto Sentiment', 'FontSize', FontS);
