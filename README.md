# Automated ESP32 Knife-Edge Laser Beam Profiler

## Intro

### In this optoelectronics characterization experiment, I used a differentiated knife-edge method with FWHM interpolation to find the 1/e<sup>2</sup> beam diameter. I user an ESP32, a laser diode, photoresistor, stepper motor and knife edge to collect power-position data. I later analyzed this data in Python using numpy and matplotlib. My calculated beam  1/e<sup>2</sup> value was 2.71mm.

## Setup
**Equipment**
  - ESP32 Microcontroller
  - HW-493 Laser Diode Module
  - GL5528 Photoresistor
  - 28BYJ-48 Stepper Motor with a soldered on box cutter knife-edge
  - ULN2003 Driver
  - Breadboard

**Tools**
  - C++ (ESP32 code for data collection)
  - Python (data analysis)
      - Numpy
      - Matplotlib
    
  

