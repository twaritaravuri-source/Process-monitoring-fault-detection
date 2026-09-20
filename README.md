# Process Monitoring and Fault Detection

## Overview

This project uses Python to analyse simulated chemical plant sensor data and identify abnormal operating conditions.

The project monitors five process variables:

* Temperature
* Pressure
* Flow Rate
* RPM
* Vibration

A rule-based fault detection system is used to classify temperature readings as Normal, Warning, or Critical. A multi-sensor detection system is then used to identify potential faults by considering temperature alongside RPM and vibration.

The project demonstrates how Python, Pandas and Matplotlib can be applied to process monitoring and basic fault detection in chemical engineering.

## Objectives

The main objectives of this project are to:

* Generate and analyse simulated chemical plant sensor data.
* Use Python and Pandas to process and analyse process data.
* Identify abnormal temperature conditions using predefined operating thresholds.
* Detect potential faults using multiple sensor measurements.
* Identify individual fault events from continuous sensor data.
* Visualise process behaviour and detected faults using Matplotlib.
* Compare sensor behaviour during normal and critical operating conditions.

## Project Structure

```text
Process-monitoring-fault-detection/
│
├── data/
│   └── plant_sensor_data.csv
│
├── output/
│   └── abnormal_readings.csv
│
├── analysis.py
├── generate_data.py
└── README.md
```

### File descriptions:

generate_data.py — generates the simulated plant sensor dataset.

analysis.py — analyses the sensor data, detects abnormal operating conditions and identifies fault events.

data/plant_sensor_data.csv — contains the simulated plant sensor readings.

output/abnormal_readings.csv — contains readings classified as abnormal.

README.md — provides an overview of the project and explains the methodology and results.

## Methodology

The project follows several stages:

1. **Data generation**

   Simulated plant sensor data is generated using Python, representing normal operating conditions with deliberately introduced abnormal behaviour.

2. **Data analysis**

   Pandas is used to load and analyse the sensor dataset, including calculating summary statistics and examining sensor behaviour.

3. **Temperature fault detection**

   Temperature readings are classified using predefined thresholds:

   * Below 85°C: Normal
   * 85–90°C: Warning
   * Above 90°C: Critical

4. **Multi-sensor fault detection**

   Potential faults are identified when the temperature is above the critical threshold and either RPM or vibration exceeds its defined fault threshold.

5. **Fault event detection**

   Consecutive critical readings are grouped into individual fault events, allowing the duration and timing of abnormal operating periods to be identified.

6. **Data visualisation**

   Matplotlib is used to visualise temperature, RPM and detected faults over time.

7. **Sensor comparison**

   Average sensor values during normal and critical operation are compared to identify changes in process behaviour.

## Results

The fault detection system identified the following operating conditions:

* 989 normal readings
* 4 warning readings
* 7 critical readings
* 6 multi-sensor fault readings
* 2 separate critical fault events

The first critical event occurred between 05:02 and 05:03, while the second occurred between 11:40 and 11:44.

The multi-sensor detection system identified 6 of the 7 temperature-critical readings. One critical temperature reading was not classified as a multi-sensor fault because neither RPM nor vibration exceeded the additional fault thresholds.

The analysis also showed differences in average sensor values between normal and critical operating conditions. These results demonstrate how combining multiple process variables can provide additional information compared with monitoring temperature alone.

## Limitations

This project uses simulated sensor data rather than measurements from a real chemical plant.

The fault detection system is rule-based and relies on predefined thresholds. These thresholds were selected for the purposes of demonstrating the detection method and may not represent safe operating limits for a real industrial process.

The system currently focuses on a limited number of process variables and does not use machine learning or advanced statistical fault detection methods.

Therefore, the results demonstrate the application of Python-based process monitoring rather than providing a validated industrial fault detection syste

## Future Development

The project could be extended in several ways:

* Introduce machine learning models to identify abnormal operating conditions automatically.
* Use historical sensor data to train a fault classification model.
* Include additional process variables and investigate relationships between sensors.
* Develop more advanced statistical methods for detecting unusual process behaviour.
* Create an interactive dashboard for real-time monitoring of plant conditions.
* Evaluate the fault detection system using additional datasets and performance metrics
## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Git and GitHub
