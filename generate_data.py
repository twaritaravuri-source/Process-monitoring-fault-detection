import numpy as np
import pandas as pd
np.random.seed(42)

number_of_readings = 1000

timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    periods=number_of_readings,
    freq="min"
)
timestamps = pd.date_range(
    start="2026-01-01 00:00:00",
    periods=number_of_readings,
    freq="min"
)
temperature = np.random.normal(
    loc=75,
    scale=3,
    size=number_of_readings
    
)

temperature[300:305] += 15 #introducing a fult in temperature for data
temperature[700:705] += 20



pressure = np.random.normal(
    loc=5,
    scale=0.2,
    size=number_of_readings
)
rpm = np.random.normal(
    loc=1500,
    scale=50,
    size=number_of_readings
)

rpm[300:305] += 50 #adding 50rpm to the first example of a fault in the rpm data
rpm[700:705] += 100 #adding 100rpm to the second example of a fault in the rpm data
#This deliberately creates a relationship between the 2 sensors. 

vibration = np.random.normal(
    loc=8,
    scale=1.5,
    size=number_of_readings
)
flow_rate = np.random.normal(
    loc=100,
    scale=5,
    size=number_of_readings
)
data = pd.DataFrame({
    "Timestamp": timestamps,
    "Temperature": temperature,
    "Pressure": pressure,
    "Flow Rate": flow_rate,
    "RPM": rpm,
    "Vibration": vibration
})

print(data.head())
data.to_csv("data/plant_sensor_data.csv", index=False)