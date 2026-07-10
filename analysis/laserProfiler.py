import numpy as np
import matplotlib.pyplot as plt
import math
import util

ARM_LENGTH = 5.1
STEPS_PER_ROTATION = 2048

# values from terminal (check /firmware/Esp32DataCollection.cpp)
steps = np.array([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145])
# PRECONDITION: a value of 0 must be present in raw_ADC
raw_ADC = np.array([3354,3374,3363,3356,3358,3363,3367,3361,3366,3365,3357,3355,3361,3357,3363,3361,3358,3358,3359,3361,3361,3358,3358,3358,3358,3356,3361,3357,3359,3358,3366,3359,3355,3356,3357,3354,3357,3358,3341,3334,3312,3295,3248,3191,3121,3030,2882,2735,2589,2416,2145,1806,1477,1200,801,466,64,0,5,336,681,1059,1381,1698,2079,2355,2545,2701,2861,3004,3102,3179,3234,3281,3307,3329,3339,3355,3359,3355,3357,3365,3348,3361,3363,3357,3357,3354,3358,3362,3363,3357,3363,3363,3357,3358,3357,3358,3354,3358,3359,3359,3357,3349,3346,3355,3355,3355,3355,3360,3356,3357,3357,3358,3350,3356,3348,3359,3359,3357,3351,3344,3351,3351,3357,3357,3359,3347,3359,3355,3350,3354,3346,3353,3355,3351,3361,3353])

# update the length of the arrays, starting at step 40 and stop at the first ADC value of 0. this keeps our data relevant to the laser profile and irrelevant data at the beginning and end of the arrays
start_idx = np.where(steps >= 40)[0][0]
zero_position = np.where(raw_ADC[start_idx:] == 0)[0][0]

zero_index = start_idx + zero_position

steps = steps[start_idx:zero_index + 1]
raw_ADC = raw_ADC[start_idx:zero_index + 1]

# make the first step start from 0
steps -= 40

print(steps)

# replace steps with a distance array
# calculate distance per step in centimeters by dividing path circumference by number of steps
distancePerStep = (2 * math.pi * ARM_LENGTH) / (STEPS_PER_ROTATION)
print("Distance per step (cm): ", distancePerStep)

# create distances array converting steps to linear distances
distances = steps * distancePerStep
print("Distances (cm): ", distances)

# NOTE: for a derivation of this equation, check README.md
# convert ADC to relative power using the empirical power-law model of a photoresistor
# note that fixed resistor is 10K Ohms, and the GL5528 photoresistor has a gamma value of 0.7, and the ADC is 12-bit (0-4095)
relative_power = (1/(10**4 * (4095/raw_ADC - 1)))**(1/0.7)

# update zero_index
zero_index = np.where(raw_ADC == 0)[0][0]

# for the zero value, we can use the same formula but with a raw_ADC value of 1 (to avoid division by zero)
# an ADC value of 1 is very close to 0, so the relative power will be sufficiently small
relative_power[zero_index] = (1/(10**4 * (4095/1 - 1)))**(1/0.7)
print("Relative power: ", relative_power)

intensity = -np.gradient(relative_power, distances)
print("Intensity: ", intensity)

smoothed_intensity = util.moving_average_5_with_edges(intensity)

# make intensity values range from 0 to 1 to have a relative intensity profile
smoothed_intensity = (smoothed_intensity/np.max(smoothed_intensity))

plt.plot(distances, smoothed_intensity)
plt.xlabel("Distance (cm)")
plt.ylabel("Smoothed Intensity (normalized)")
plt.title("Laser Profile")
plt.show()


# INTERPOLATION for FWHM: find the two distances where intensity is half of the max
target = 0.5
crossings = util.interpolate_crossings(distances, smoothed_intensity, target)

print("Estimated distances for intensity 0.5:", crossings)

# using the two half-maximum points, we can calculate the full width at half maximum (FWHM)
fwhm = crossings[1] - crossings[0]
print("Full width at half maximum (FWHM): ", fwhm)

# fwhm-derived beam diameter (core center of the beam)
fwhm_beam_diameter = fwhm * 1.699
print("FWHM-derived diameter at 1/e^2(cm): ", fwhm_beam_diameter)

# INTERPOLATION for 1/e^2: find the two distances where intensity is 13.5% of the max
target = 0.135
crossings_1e2 = util.interpolate_crossings(distances, smoothed_intensity, target)

print("Estimated distances for intensity 0.135:", crossings_1e2)

# using the two 1/e^2 points, we can calculate the full width at 1/e^2
fwhm_1e2 = crossings_1e2[1] - crossings_1e2[0]
print("Full width at 1/e^2: ", fwhm_1e2)

print("1/e^2 graphically-derived diameter at 1/e^2(cm): ", fwhm_1e2)

# Final estimated beam_diameter at 1/e^2
final_beam_diameter = (fwhm_beam_diameter + fwhm_1e2) / 2
print("Final beam diameter (cm): ", final_beam_diameter)
