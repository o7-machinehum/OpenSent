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
len = length(Sen) / 2; %How much into the future we look is a matter of discussion

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

title('Mean result time shifted correlation of Cost(Normalised) & Sentiment(Normalised)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

%Find time lag ds/dt
%-------------------------------------------------------------
lenDer = length(Sen) / 4 ; %Want to analyse quarter the dataset

TempCost = diff(normCost);
TempSen = diff(normSen);

for i = 1:len
	TempCost(1) = [];
	TempSen(end) = [];
	meanResultdiff(i) = mean(abs(TempCost - TempSen));
end

figure(2)
plot(meanResultdiff);
title('Mean result time shifted correlation of dCost/dt(norm) and dSen/dt(norm)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

break; %Break here - look at both plots then decide what lag to use

%Apply Lag
%-------------------------------------------------------------
x = 0:length(Cost) - 1;
x2 = 0:length(Cost) - 1;

lag = find(meanResult == min(meanResult));
%lag = find(meanResult == min(meanResultdiff));
x2 = x2 + lag;

figure(1)
ax2 = plotyy(x, normCost, x2, normSen);
legend('Cost', 'Sentiment (timeshifted)')
