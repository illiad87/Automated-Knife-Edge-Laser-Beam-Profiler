# Automated ESP32 Knife-Edge Laser Beam Profiler

## Intro

### In this optoelectronics characterization experiment, I used a differentiated knife-edge method with FWHM interpolation to find the 1/e<sup>2</sup> beam diameter. I user an ESP32, a laser diode, photoresistor, stepper motor and knife edge to collect power-distance data. I later analyzed this data in Python using Numpy and Matplotlib. My calculated beam  1/e<sup>2</sup> value was 2.71mm.

## Setup
**Equipment**
  - ESP32 Microcontroller
  - HW-493 Laser Diode Module
  - GL5528 Photoresistor
  - 28BYJ-48 Stepper Motor with a soldered-on box cutter knife-edge
  - ULN2003 Driver
  - Breadboard
  - 9V 1A Power Supply

**Tools**
  - C++ (ESP32 code for data collection)
  - Python (data analysis)
      - Numpy
      - Matplotlib
  - Arduino IDE (Serial Monitor)

<img width="2048" height="1536" alt="Laser Characterization" src="https://github.com/user-attachments/assets/38bc7bf3-bfe7-4908-933a-a2d6e5df759c" />

> Note that the experiment (video shown in section below) takes place in a dark room. Also, the built-in ESP32 LEDs are covered with dark plastic plates to prevent interference with photoresistor

## Data Collection

https://github.com/user-attachments/assets/4db6cd97-dd47-4af8-84c1-0c3d3c2dd359
> Note that Github limits content to 10Mb per file, so I had to adjust the video to 540p quality. This video is also shorter to include the essence of the experiment. In reality, the blade moved through a greater range of motion and more data was collected

After uploading [my C++ code](firmware/Esp32DataCollection.cpp) to the ESP32, I printed the step-ADC data in the serial monitor and saved it in a [.csv file](analysis/photoresistorData.csv)
















   
  
    
  

