%Todo
%-------------------------------------------------------------
% 1. Implement Filename into plot titles
%-------------------------------------------------------------
pkg load signal;

clc; clear;

FontS = 20;

%File location
%-------------------------------------------------------------
filename = 'Sept/Sept19-25.csv';
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

figure(2)
x3 = x;
x3(end) = [];
ax = plotyy(x3, diff(filteredCost), x3, diff(filteredSen));
title(titleRaw, 'FontSize', FontS);
ylabel(ax(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax(2), 'Crypto Sentiment', 'FontSize', FontS);
legend('Cost', 'Sentiment')

%break;

%Find time lag
%-------------------------------------------------------------
len = length(Sen) / 4 ; %Want to analyse quarter the dataset

TempCost = Cost;
TempSen = filteredSen;

for i = 1:len
	TempCost(1) = [];
	TempSen(end) = [];
	meanResult(i) = mean(TempCost - TempSen);
end

figure(3)
plot(meanResult);

title('Mean result time shifted correlation of Cost & Sentiment', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

%Find time lag ds/dt
%-------------------------------------------------------------
lenDer = length(Sen) / 4 ; %Want to analyse quarter the dataset

TempCost = diff(filteredCost);
TempSen = diff(filteredSen);

for i = 1:len
	TempCost(1) = [];
	TempSen(end) = [];
	meanResultdiff(i) = mean(abs(TempCost - TempSen));
end

figure(4)
plot(meanResultdiff);
title('Mean result time shifted correlation of dCost/dt and dSen/dt', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);


%Apply Lag
%-------------------------------------------------------------
lag = find(meanResult == min(meanResult));
x2 = x2 + lag;

break;

figure(4)
ax2 = plotyy(x, filteredCost, x2, filteredSen);
legend('Cost', 'Sentiment (timeshifted)')

break;

figure(5)
ax = plotyy(x, filteredCost, x2, [normSen normVol]);
title(titleRaw, 'FontSize', FontS);
ylabel(ax(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax(2), 'Crypto Sentiment', 'FontSize', FontS);
legend('Cost', 'Sentiment(Normalised)', 'Sentiment Volume(Normalised)')

figure(6);
dsdt = diff(filteredSen) ./ 10;
x2(end) = [];
ax2 = plotyy(x, filteredCost, x2, dsdt);
title(titleDer, 'FontSize', FontS);
ylabel(ax2(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax2(2), 'Crypto Sentiment', 'FontSize', FontS);

%figure();
%plotyy(x, Cost, x, normVol-normSen)
break;
