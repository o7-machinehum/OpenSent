pkg load signal;

clc; clear; close all;

FontS = 20;

BTCticker = 3;
BTCvol = 4;
BTCsen = 5;
BTCcost = 6;

LTCticker = 7;
LTCvol = 8;
LTCsen = 9;
LTCcost = 10;

%filename = 'Sept17-18.csv';
%filename = 'Sept17_2017.csv';
filename = 'Sept19-24.csv';
M = csvread(filename);

Cost = M(1:end, BTCcost);
Sen = M(1:end, BTCsen);
Vol = M(1:end, BTCvol);

titleRaw = 'Cost of Bitcoin vs. Bitcoin Sentiment';
titleDer = 'Cost of Bitcoin vs. (d/dt)Bitcoin Sentiment';

%Cost = M(1:end, LTCcost);
%Sen = M(1:end, LTCsen);

[b,a]=butter(3, 0.01);
filteredSen = filter(b,a,Sen);
filteredCost = sgolayfilt(Cost);
filteredVol = filter(b,a,Vol);

normSen = filteredSen .* (1 / max(filteredSen)); %Normalize
normVol = filteredVol .* (1 / max(filteredVol)); %Normalize
normCost = Cost .* (1 / max(Cost)); %Normalize

x = 0:length(M) - 1;
x2 = 0:length(M) - 1;

len = length(Sen) - 100; %Want to analyse half the dataset

for i = 1:len
	Cost(1) = [];
	Sen(end) = [];
	meanResult(i) = mean(Cost .*Sen);
end

ax = plotyy(x, Cost, x2, filteredSen);
title(titleRaw, 'FontSize', FontS);
ylabel(ax(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax(2), 'Crypto Sentiment', 'FontSize', FontS);
legend('Cost', 'Sentiment', 'Sentiment Volume')

break;


%Time shift
x2 = x2 + 800;

ax = plotyy(x, filteredCost, x2, [normSen normVol]);
title(titleRaw, 'FontSize', FontS);
ylabel(ax(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax(2), 'Crypto Sentiment', 'FontSize', FontS);
legend('Cost', 'Sentiment(Normalised)', 'Sentiment Volume(Normalised)')


figure();
dsdt = diff(filteredSen) ./ 10;
x2(end) = [];
ax2 = plotyy(x, Cost, x2, dsdt);
title(titleDer, 'FontSize', FontS);
ylabel(ax2(1), 'Cost (USD)', 'FontSize', FontS);
ylabel(ax2(2), 'Crypto Sentiment', 'FontSize', FontS);

%figure();
%plotyy(x, Cost, x, normVol-normSen)

