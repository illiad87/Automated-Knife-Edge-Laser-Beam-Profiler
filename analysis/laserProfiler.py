import numpy as np
import matplotlib.pyplot as plt
import math
import util

ARM_LENGTH = 5.1
STEPS_PER_ROTATION = 2048

data = np.genfromtxt("photoresistorData.csv", delimiter=",", names=True)

# values from terminal (check /firmware/Esp32DataCollection.cpp)
steps = data["step"]
# PRECONDITION: a value of 0 must be present in raw_ADC
raw_ADC = data["adc_val"]

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
