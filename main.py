#Total Pressure Loss for SDR Liquid Rocket Engine Plumbing Circuit

#Sun Devil Rocketry Liquids (Plumbing)
#Created by Patrick Imper 04/01/2020 and translated from MATLAB code by Brendan Graves and Luke Spindel 06/29/2022

import math

#-----------------------------------------------------------------

#FITTINGS IN OUR PLUMBING CIRCUIT

#LOx side
o_couplings = 11; # Number of compression fitting couplings
o_90s = 2; # Number of 90 degree bends (R/D > 1)
o_teethrough = 4; # Number of tee-through fittings (does not account for tube couplings)

# Kerosene Side
k_couplings = 11; # Number of compression fitting couplings
k_90s = 2; # Number of 90 degree bends (R/D > 1)
k_teethrough = 4; # Number of tee-through fittings (does not account for tube couplings)

#-----------------------------------------------------------------

#SUM OF DIFFERENCES IN HEIGHTS AND SUM OF LENGTH OF PLUMBING

sumH_LOx = 0.0924152076; # Sum of the changes in height for LOx (meters)
suml_LOx = 1.5; # Sum in the length of plumbing for LOx (meters)
sumH_K = 0.0924152076; # Sum of the changes in height for Kerosene (meters)
suml_K = 1.5; # Sum in the length of plumbing for Kerosene (meters)

#-----------------------------------------------------------------

#CONASTANT/DETERMINED

g = 9.80665; # Gravitatinal acceleration (m/s^2)

odImp = 0.5; # Stainless tubing outer diameter (inches)
wallThicc = 0.035; # Tubing wall thickness (inches)

idImp = odImp-(2*wallThicc); # Stainless tubing inner Diameter (inches)

o_mfr = 1.0556; # Mass flow rate oxidizer (lbm/s)
k_mfr = 1.2599; # Mass flow rate kerosene + Film Cooling) (lbm/s)

kDen = 810; # Kerosene density @ 20 degrees C (kg/m^3)
oDen = 1140; # LOX density @ ~ -200 degrees C (kg/m^3)

k_mu = .192*10**(-3); # Dynamic viscosity of kerosene @ 20 degrees C (Ns/m^2 or Pa*s)
o_mu = 6.95*10**(-6); # Dynamic viscosity of LOX @ -183 degrees C (N*s/m^2 or Pa*s)

o_SG = 1.143; # LOx specific gravity (Unitless)
k_SG = 0.810; # Kerosene specific gravity (Unitless)

cv_check = 1.68; # Coefficient Volume for chosen Check Valve (Unknown?)
cv_valve = 7.5; # Coefficient Volume for chosen Main Valves (Unknown?)

orifice_drop = 30; # Designed optimal orifice pressure drop (PSI)
cc_pressure = 250; # Chamber pressure (psig)
injector_drop = 100; # Injector pressure drop (PSI)
cooling_drop = 10; # Regenetive cooling drop (PSI)

ssr = 0.002; # Stainless steel roughness (mm)

#-----------------------------------------------------------------

#BASIC CALCULATIONS/CONVERTING UNITS

idMet = idImp/39.3700787; # Stainess tubing inner diameter (meters)

o_mfrMET = o_mfr*0.45359237; # Mass flow rate oxidizer (kg/s)
k_mfrMET = k_mfr*0.45359237; # Mass flow rate fuel (kg/s)

o_vfr = o_mfrMET/oDen*15850.323141; # volumetric flow rate oxidizer (GPM)
k_vfr = k_mfrMET/kDen*15850.323141; # volumetric FLow Rate fuel (GPM)

ssrr = ssr/(idMet*1000); # Stainless Steel Relative Roughness (Roughness/Diameter) (Unitless)

A = math.pi*(idMet/2)**2; # Tubing area (meters^2)

vo = o_mfrMET/(oDen * A); # Velocity of LOX in tubing (m/s)
vk = k_mfrMET/(kDen * A); # Velocity of Kerosene in tubing (m/s)

k_Reyn = (kDen*vk*idMet)/k_mu; # Reynolds number for Kerosene (Unitless)
o_Reyn = (oDen*vo*idMet)/o_mu; # Reynolds number for LOX (Unitless)

#-----------------------------------------------------------------

#MOODY CHART CALCULATIONS(TO GET FRICTION FACTOR)

C = ssrr / 3.7;
B = 2.51/k_Reyn;
x = -1.8*math.log10((6.9/k_Reyn)+C**1.11);

for v in range(2):
  y = x+2*math.log10(C+B*x);
  y2= 1+2*(B/math.log(10))/(C+B*x);
  x = x - y/y2;


ff_k = 1/(x**2); # Friction Factor for Kerosene (Unitless)

B = 2.51/o_Reyn;
x = -1.8*math.log10((6.9/o_Reyn)+C**1.11);

for v in range(2):
  y = x+2*math.log10(C+B*x);
  y2= 1+2*(B/math.log(10))/(C+B*x);
  x = x - y/y2;

ff_o = 1/(x**2); # Friction Factor for LOX (Unitless)

#-----------------------------------------------------------------

#CALCULATING K VALUES FOR FITTING AND VALVES USING 2K METHOD

#The diameter used in this is imperial for a reason, it's required for this method

sumK_LOx = 0.04*o_couplings + ((200/o_Reyn)+0.1*(1+(1/idImp)))*o_teethrough + ((800/o_Reyn)+0.2*(1+(1/idImp)))*o_90s;

sumK_K = 0.04*k_couplings + ((200/o_Reyn)+0.1*(1+(1/idImp)))*k_teethrough + ((800/o_Reyn)+0.2*(1+(1/idImp)))*k_90s;

#-----------------------------------------------------------------

#HEAD LOSS CONSTANTS

HmajLOx_const = (ff_o*vo**2)/(2*g*idMet); # Head loss major constant LOx (Unitless)
HminLOx_const = (vo**2)/(2*g); # Head loss minor constant LOx (meters)
HmajK_const = (ff_k*vk**2)/(2*g*idMet); # Head loss constant Kerosene (Unitless)
HminK_const = (vk**2)/(2*g); # Head loss minor constant Kerosene (meters)

#-----------------------------------------------------------------

#CALCULATING PRESSURE LOSS

deltaP_Lox = o_vfr**2*o_SG*(1/cv_check**2+1/cv_valve**2)+orifice_drop+(oDen*g)/6894.76*(sumH_LOx+(HmajLOx_const*suml_LOx)+(HminLOx_const*sumK_LOx)); # Pressure loss for LOx (PSI)

deltaP_K = k_vfr**2*k_SG*(1/cv_check**2+1/cv_valve**2)+orifice_drop+cooling_drop+(kDen*g)/6894.76*(sumH_K + (HmajK_const*suml_K)+(HminK_const*sumK_K)); #Pressure loss for Kerosene (PSI)

LOxTank_press = cc_pressure+injector_drop#+ceil(deltaP_Lox);
KerTank_press = cc_pressure+injector_drop#+ceil(deltaP_K);

print("Liquid Oxygen pressure loss is " + str(math.ceil(deltaP_Lox)) + "psi");

print("Kerosene pressure loss is " + str(math.ceil(deltaP_K)) + "psi");

print("")

print("Therefore, based on a chamber pressure of " + str(cc_pressure) +"psig and an injector pressure loss of " + str(injector_drop) + "psi, the LO2 tank will need to be at " + str(LOxTank_press) + "psig and Kerosene tank at " + str(KerTank_press) + "psig." );
