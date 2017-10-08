#!/usr/bin/octave-cli --persist

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

D = 20; %How many chunks do you want to break up the data into

%File location
%-------------------------------------------------------------
filename1 = 'Sept/Sept17-18.csv';
filename2 = 'Sept/Sept17_2017.csv';
filename3 = 'Sept/Sept19-21.csv';
filename4 = 'Sept/Sept19-26.csv';
filename5 = 'Sept/Sept20_2017.csv';
filename5 = 'Sept/Sept17_2017.csv';

filename6 = 'Oct/Sept29-Oct1.csv';
filename7 = 'Oct/Oct2.csv';
filename8 = 'Oct/Oct3.csv';
filename9 = 'Oct/Oct4.csv';
filename10 = 'Oct/Oct5.csv';
filename11 = 'Oct/Oct6.csv';
filename12 = 'Oct/Oct7.csv';

M = csvread(filename7);
M = [M;csvread(filename8)];
M = [M;csvread(filename9)];
M = [M;csvread(filename10)];
M = [M;csvread(filename11)];
%M = [M;csvread(filename12)];

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

%Break into smaller vectors
%-------------------------------------------------------------
normSen(length(normSen) - rem(length(normSen),D)+1:end) = [];
normCost(length(normCost) - rem(length(normCost),D)+1:end) = [];

SentArray(length(normSen) / D, D) = zeros;
CostArray(1:length(normSen) / D, D) = zeros;

len = length(normSen);

for i = 1:D
	index = i*(len/D);
	SentArray(1:end, i) = normSen((index-len/D)+1:index);
	CostArray(1:end, i) = normCost((index-len/D)+1:index);
end

for j = 1:D
	%Find time lag
	%-------------------------------------------------------------
	len = MaxShiftel;

	%Temp values
	TempCost = CostArray(1:end, j);
	TempSen = SentArray(1:end, j);

	for i = 1:len
		TempCost(1) = [];
		TempSen(end) = [];
		meanResult(i, j) = mean(TempCost - TempSen);
	end

	%Find time lag ds/dt
	%-------------------------------------------------------------
	lenDer = MaxShiftel; %Max 5hr delay


	TempCost = diff(CostArray(1:end, j));
	TempSen = diff(SentArray(1:end, j));

	for i = 1:lenDer
		TempCost(1) = [];
		TempSen(end) = [];
		meanResultdiff(i, j) = mean(abs(TempCost - TempSen));
	end
end

%Plotting
%-------------------------------------------------------------
figure(1);
plot(meanResult);
grid on
title('Mean result time shifted correlation of Cost(Normalised) & Sentiment(Normalised)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

figure(2)
plot(meanResultdiff);
grid on
title('Mean result time shifted correlation of dCost/dt(norm) and dSen/dt(norm)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

figure(3);
plot(find(meanResultdiff == min(meanResultdiff))' - (0:(D-1))*len);grid on
title('Minmum value of each fratal seperation - dCost/dt(norm) and dSen/dt(norm)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Minmum value of time shift vector per fraction', 'FontSize', FontS);

%Colapse all the results into one average vector
%Vector sum of all the columns
Av = sum(meanResultdiff');
figure(4);
plot(Av);
grid on
title('Vector sum of all fractal pieaces - Mean result time shifted correlation of dCost/dt(norm) and dSen/dt(norm)', 'FontSize', FontS);
xlabel('Time shift', 'FontSize', FontS);
ylabel('Mean value (Lower is better)', 'FontSize', FontS);

break; %Break here - look at both plots then decide what lag to use
%I don't know what the fuck I'm going to do below
for j = 1:D
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
end
