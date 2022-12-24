clc

%% VARIABLES

L = 1;       % Length of pipe (ft)
T1 = -370;   % Temp inside pipe (°F)
T2 = 80;     % Temp outside (°F)
Kpipe = 28;  % Thermal conductivity of the pipe 316 stainless steel (btu/(hr*ft*°F))
Kins = [0.0208, 0.0075, 0.008, 0.0242];  % Thermal conductivity of the insulation (btu/(hr*ft*°F))

insThick = [0.08333, 0.01640, 0.019685, 0.08333];  % Thickness of insulation (ft)
pipeInnerDiam = 0.04167;                           % Inner diameter of the pipe (ft)
pipeThick = 0.00291;                               % Thickness of the pipe; inner to outer diameter (ft)

r1 = pipeInnerDiam;   % Radius from the center of the pipe to the inner wall (ft)
r2 = r1 + pipeThick;  % Radius from the center of the pipe to the outer wall (ft)
r3 = r2 + insThick;   % Radius from the center of the pipe to the outer wall of the insulation (ft)

insPrice = [3.88, 27.5, 29.5, 7.25];     % Price of thermal isulation ($/ft^2)
pipeDiam = pi*r2*2;  % Diameter of the pipe (ft)

%% HEAT TRANSFER EQUATION

for i = 1:4
    Q(i) = (2*pi*L*(abs(T1-T2))) / (((log(r1/r2)) / Kpipe) + ((log(r3(i)/r2)) / Kins(i)));
end

display(Q)

%% PRICE EQUATIONS

totPrice = insPrice * pipeDiam  % Price of thermal insulation per foot

%% GRAPH HEAT TRANSFER VS PRICE & HEAT TRANSFER VS INSULATION THICKNESS

figure(1)  % Heat transfer vs price
plot(Q,totPrice,'o')
title('Insulation Materials: Heat Transfer vs Price')
xlabel('Heat Transfer (J/(m^2*sec))')
ylabel('Price ($/ft of pipe)')
xlim([52,70])
ylim([0,9])
labels = {'Thermalcel Polyofin', 'Cryogel Z', 'Cabot Thermal Wrap', 'Foamglas'};
text(Q,totPrice,labels, 'VerticalAlignment','top','HorizontalAlignment','center')

figure(2)  % Heat transfer vs insulation thickness
plot(Q,insThick,'o')
title('Insulation Materials: Heat Transfer vs Insulation Thickness')
xlabel('Heat Transfer (J/(m^2*sec))')
ylabel('Insulation Thickness (ft)')
xlim([52,70])
%labels = {'Thermalcel Polyofin', 'Cryogel Z', 'Cabot Thermal Wrap', 'Foamglas'};
text(Q,insThick,labels, 'VerticalAlignment','top','HorizontalAlignment','center')