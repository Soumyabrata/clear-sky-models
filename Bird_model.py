from math import * # enables use of pi, trig functions, and more.
#from __future__ import division # ensures no rounding errors from division involving integers

import numpy as np
#import math
import datetime


phi = 1.3429943
longitude = 103.6810899

#tz = -5
tz = 8
P_mb = 970
Ozone_cm = 0.3
H20_cm = 1.5
AOD500nm = 0.193
AOD380nm = 0.298
Taua = 0.15
Ba = 0.85
albedo = 0.2


G_sc = 1367 # W/m^2
std_mer = longitude-longitude%15+15 # This Standard Meridian calculation is only a guide!! 
# Please double check this value for your location!


# DAY OF YEAR
#n = 5

# HOUR OF DAY
#hr = 11



def etr(n):
	return G_sc*(1.00011+0.034221*cos(2*pi*(n-1)/365)+0.00128*sin(2*pi*(n-1)/365)+0.000719*cos(2*(2*pi*(n-1)/365))+
		0.000077*sin(2*(2*pi*(n-1)/365)))




def dec(Dangle):
	return (0.006918-0.399912*cos(Dangle)+0.070257*sin(Dangle)-0.006758*cos(2*Dangle)+0.000907*sin(2*Dangle)-0.002697*cos(3*Dangle)
		+0.00148*sin(3*Dangle))*(180/pi)


def eqtime(Dangle):
	return (0.0000075+0.001868*cos(Dangle)-0.032077*sin(Dangle)-0.014615*cos(2*Dangle)-0.040849*sin(2*Dangle))*229.18


def omega(hr, eqt):
	return 15*(hr-12.5) + longitude - tz*15 + eqt/4	


def zen(dec, hr_ang):
	return acos(cos(dec/(180/pi))*cos(phi/(180/pi))*cos(hr_ang/(180/pi))+sin(dec/(180/pi))*sin(phi/(180/pi)))*(180/pi)

def airmass(zen):
	if zen < 89:
		return 1/(cos(zen/(180/pi))+0.15/(93.885-zen)**1.25)
	else:
		return 0

def T_rayleigh(airmass):
	if airmass > 0:
		return exp(-0.0903*(P_mb*airmass/1013)**0.84*(1+P_mb*airmass/1013-(P_mb*airmass/1013)**1.01))
	else:
		return 0

def T_ozone(airmass):
	if airmass > 0:
		return 1-0.1611*(Ozone_cm*airmass)*(1+139.48*(Ozone_cm*airmass))**-0.3034-0.002715*(Ozone_cm*airmass)/(1+0.044*(Ozone_cm*airmass)+0.0003*(Ozone_cm*airmass)**2)
	else:
		return 0


def T_gasses(airmass):
	if airmass > 0:
		return exp(-0.0127*(airmass*P_mb/1013)**0.26)
	else:
		return 0		


def T_water(airmass):
	if airmass > 0:
		return 1-2.4959*airmass*H20_cm/((1+79.034*H20_cm*airmass)**0.6828+6.385*H20_cm*airmass)
	else:
		return 0

def T_aerosol(airmass):
	if airmass > 0:
		return exp(-(Taua**0.873)*(1+Taua-Taua**0.7088)*airmass**0.9108)
	else:
		return 0		

def taa(airmass, taerosol):
	if airmass > 0:
		return 1-0.1*(1-airmass+airmass**1.06)*(1-taerosol)
	else:
		return 0		

def rs(airmass, taerosol, taa):
	if airmass > 0:
		return 0.0685+(1-Ba)*(1-taerosol/taa)
	else:
		return 0

def Id(airmass, etr, taerosol, twater, tgases, tozone, trayleigh):
	if airmass > 0:
		return 0.9662*etr*taerosol*twater*tgases*tozone*trayleigh
	else:
		return 0		


def idnh(zen, Id):
	if zen < 90:
		return Id*cos(zen/(180/pi))
	else:
		return 0		

def ias(airmass, etr, zen, tozone, tgases, twater, taa, trayleigh, taerosol):
	if airmass > 0:
		return etr*cos(zen/(180/pi))*0.79*tozone*tgases*twater*taa*(0.5*(1-trayleigh)+Ba*(1-(taerosol/taa)))/(1-airmass+(airmass)**1.02)
	else:
		return 0		


def gh(airmass, idnh, ias, rs):
	if airmass > 0:
		return (idnh+ias)/(1-albedo*rs)
	else:
		return 0		


def dectime(doy, hr):
	return doy+(hr-0.5)/24






def Bird_model(n,hr):

	#print (n,hr)

	etr1 = etr(n)
	Dangle = 2*pi*(n-1)/365
	dec1 = dec(Dangle)
	eqt = eqtime(Dangle)
	hr_ang = omega(hr, eqt)
	zenang = zen(dec1, hr_ang)
	airmass1 = airmass(zenang)
	trayleigh = T_rayleigh(airmass1)
	tozone = T_ozone(airmass1)
	tgases = T_gasses(airmass1)
	twater = T_water(airmass1)
	taerosol = T_aerosol(airmass1)
	taa1 = taa(airmass1, taerosol)
	rs1 = rs(airmass1, taerosol, taa1)
	Id1 = Id(airmass1, etr1, taerosol, twater, tgases, tozone, trayleigh)
	idnh1 = idnh(zenang, Id1)
	ias1 = ias(airmass1, etr1, zenang, tozone, tgases, twater, taa1, trayleigh, taerosol)
	gh1 = gh(airmass1, idnh1, ias1, rs1)

	#print(gh1)
	return (gh1)

	