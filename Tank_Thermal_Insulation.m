clc

%% VARIABLES

L = 2.225;       % Length of tank (ft)
T1 = -225.67;   % Temp inside tank (°F) 130K
T2 = 90;     % Temp outside (°F)
Kpipe = 31.8246;  % Thermal conductivity of the tank 304L stainless steel (btu/(hr*ft*°F))
Kins = [0.0208, 0.0075, 0.0080, 0.0242, 0.0800];  % Thermal conductivity of the insulation (btu/(hr*ft*°F))

insThick = [0.08333, 0.01640, 0.019685, 0.08333, 0.16667];  % Thickness of insulation (ft)
tankInnerDiam = 0.31583;                           % Inner diameter of the tank (ft)
tankThick = 0.01750;                               % Thickness of the tank; inner to outer diameter (ft)

r1 = tankInnerDiam;   % Radius from the center of the tank to the inner wall (ft)
r2 = r1 + tankThick;  % Radius from the center of the tank to the outer wall (ft)
r3 = r2 + insThick;   % Radius from the center of the tank to the outer wall of the insulation (ft)

insPrice = [3.88, 27.5, 29.5, 7.25, 0];     % Price of thermal isulation ($/ft^2)
tankDiam = pi*r2*2;  % Diameter of the tank (ft)


%% HEAT TRANSFER EQUATION

for i = 1:5
    Q(i) = (2*pi*L*(abs(T1-T2))) / (((log(r1/r2)) / Kpipe) + ((log(r3(i)/r2)) / Kins(i)));
end

display(Q)

%% PRICE EQUATIONS

totPrice = insPrice * tankDiam  % Price of thermal insulation per foot

%% GRAPH HEAT TRANSFER VS PRICE & HEAT TRANSFER VS INSULATION THICKNESS

figure(1)  % Heat transfer vs price
plot(Q,totPrice,'o')
title('Insulation Materials: Heat Transfer vs Price')
xlabel('Heat Transfer (J/(m^2*sec))')
ylabel('Price ($/ft of pipe)')
%xlim([52,70])
%ylim([0,9])
labels = {'Polyofin', 'Cryogel Z', 'Cabot', 'Foamglas','polyisocyanurate'};
text(Q,totPrice,labels, 'VerticalAlignment','top','HorizontalAlignment','center')

figure(2)  % Heat transfer vs insulation thickness
plot(Q,insThick,'o')
title('Insulation Materials: Heat Transfer vs Insulation Thickness')
xlabel('Heat Transfer (J/(m^2*sec))')
ylabel('Insulation Thickness (ft)')
xlim([300,1400])
%labels = {'Thermalcel Polyofin', 'Cryogel Z', 'Cabot Thermal Wrap', 'Foamglas', 'polyisocyanurate'};
text(Q,insThick,labels, 'VerticalAlignment','top','HorizontalAlignment','center')