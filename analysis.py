import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Load plant sensor data
data = pd.read_csv("data/plant_sensor_data.csv")
data["Timestamp"] = pd.to_datetime(data["Timestamp"])

print("First five readings:")
print(data.head())

print("\nSummary statistics:")
print(data.describe())

# Calculate basic statistics for each sensor
print("\nBasic Sensor Statistics")
print("------------------------")

for sensor in ["Temperature", "Pressure", "Flow Rate", "RPM", "Vibration"]:
    print(f"{sensor}:")
    print(f"  Average: {data[sensor].mean():.2f}") #:.2f means 2 decimal places
    print(f"  Maximum: {data[sensor].max():.2f}")

# Define temperature fault thresholds
WARNING_TEMP = 85
CRITICAL_TEMP = 90

warning_readings = data[
    (data["Temperature"] >= WARNING_TEMP) &
    (data["Temperature"] <= CRITICAL_TEMP)
]

critical_readings = data[
    data["Temperature"] > CRITICAL_TEMP
]

#prints all the critical readings for all variables 
print("\nCritical Operating Conditions")
print("----------------------------")
print(
    critical_readings[
        ["Timestamp", "Temperature", "Pressure", "Flow Rate", "RPM", "Vibration"]
    ]
)

print("Number of warning readings:", len(warning_readings))
print("Number of critical readings:", len(critical_readings))
print(critical_readings)

#this function classifies the temperature readings into three categories: "Normal", "Warning", and "Critical".
def classify_temperature(temperature):
    if temperature > CRITICAL_TEMP:
        return "Critical"
    elif temperature >= WARNING_TEMP:
        return "Warning"
    else:
        return "Normal"


data["Status"] = data["Temperature"].apply(classify_temperature) 

# Define multi-sensor fault thresholds
RPM_FAULT = 1550
VIBRATION_FAULT = 9.5

# Detect faults using multiple sensor readings
data["Multi_Sensor_Fault"] = (
    (data["Temperature"] > CRITICAL_TEMP) &
    (
        (data["RPM"] > RPM_FAULT) |
        (data["Vibration"] > VIBRATION_FAULT)
    )
)

# Display multi-sensor fault readings
multi_sensor_points = data[data["Multi_Sensor_Fault"]]

print("\nMulti-Sensor Fault Detection")
print("----------------------------")

print("Number of multi-sensor fault readings:", len(multi_sensor_points))

print("\nDetected readings:")
print(
    multi_sensor_points[
        ["Timestamp", "Temperature", "RPM", "Vibration"]
    ]
)

print(data[["Timestamp", "Temperature", "Status"]].tail(20))

# Compare temperature-based and multi-sensor fault detection
temperature_only_faults = data[
    (data["Status"] == "Critical") &
    (~data["Multi_Sensor_Fault"]) #the symbol is used to show where multi-sensor-fault is faulse, as it negates the condition
]

print("\nFault Detection Comparison")
print("-------------------------")
print("Temperature-critical readings:", len(critical_readings))
print("Multi-sensor fault readings:", data["Multi_Sensor_Fault"].sum())

print("\nCritical readings not flagged by multi-sensor detection:")
print(
    temperature_only_faults[
        ["Timestamp", "Temperature", "RPM", "Vibration"]
    ]
)

#this counts how many times each status occurs
status_counts = data["Status"].value_counts()


print("\nPlant Operating Status")
print("----------------------")
print("Normal:", status_counts.get("Normal", 0))
print("Warning:", status_counts.get("Warning", 0))
print("Critical:", status_counts.get("Critical", 0))

#this saves the abnormal readings to a different file
abnormal_readings = data[data["Status"] != "Normal"]

output_folder = Path(__file__).resolve().parent / "output"
output_folder.mkdir(exist_ok=True)

abnormal_readings.to_csv(
    output_folder / "abnormal_readings.csv",
    index=False
)

plt.figure(figsize=(10, 5))

plt.plot(
    data["Timestamp"],
    data["Temperature"],
    label="Temperature"
)

warning_points = data[data["Status"] == "Warning"] #show only the rows where the status is warning
critical_points = data[data["Status"] == "Critical"] #show only the rows where the status is critical

print("\nNumber of critical readings:", len(critical_readings)) #counts critical readings

critical_indices = critical_readings.index #gets the row numbers of these readings


# Find the start and end of each critical event
events = []

if len(critical_indices) > 0:
    start = critical_indices[0]
    previous = critical_indices[0]

    for index in critical_indices[1:]:
        if index != previous + 1:
            events.append((start, previous))
            start = index
        previous = index

    events.append((start, previous))

print("\nCritical Events")
print("---------------")

for number, (start, end) in enumerate(events, 1):
    print(
        f"Event {number}: "
        f"{data.loc[start, 'Timestamp']} to "
        f"{data.loc[end, 'Timestamp']}"
    )
print("Number of critical events:", len(events))

#puts these readings on top of the temperature plot as scatter points
plt.scatter(
    warning_points["Timestamp"],
    warning_points["Temperature"],
    label="Warning"
)

plt.scatter(
    critical_points["Timestamp"],
    critical_points["Temperature"],
    label="Critical"
)

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Plant Temperature and Detected Faults")

plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()


# Compare average sensor values during normal and critical operation
normal_readings = data[data["Status"] == "Normal"]

sensors = ["Temperature", "Pressure", "Flow Rate", "RPM", "Vibration"]

print("\nAverage Sensor Values")
print("---------------------")

for sensor in sensors:
    normal_average = normal_readings[sensor].mean()
    critical_average = critical_readings[sensor].mean()

    print(f"{sensor}:")
    print(f"  Normal:   {normal_average:.2f}")
    print(f"  Critical: {critical_average:.2f}")



#This shows a pattern where the highest temperatures occur around the same period as elevated RPM.
#However the temperature fault was deliberately created, but not the RPM fault.
#So it can't be claimed that the model has discovered that high RPM causes high temperature. 
#The data only shows correlation not causation.


#The code below is for plotting a graph of temperature and RPM over time.
fig, ax1 = plt.subplots(figsize=(10, 5))

# Temperature
ax1.plot(
    data["Timestamp"],
    data["Temperature"],
    label="Temperature"
)

# Highlight critical temperature readings
ax1.scatter(
    critical_points["Timestamp"],
    critical_points["Temperature"],
    label="Critical"
)


ax1.scatter(
    multi_sensor_points["Timestamp"],
    multi_sensor_points["Temperature"],
    label="Multi-Sensor Fault"
)

# Highlight the periods when critical fault events occurred
for number, (start, end) in enumerate(events, 1):
    ax1.axvspan( #the axvspan shades the background of the graph between the start and end times.
        data.loc[start, "Timestamp"],
        data.loc[end, "Timestamp"],
        alpha=0.3,
        label="Fault Event" if number == 1 else None
    )

ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)") #this is left hand axis for temperature

# RPM
ax2 = ax1.twinx() # this is the right hand axis for RPM. twinx is for using a different scale

ax2.plot(
    data["Timestamp"],
    data["RPM"],
    label="RPM"
)

ax2.set_ylabel("RPM")

plt.title("Plant Temperature, RPM and Detected Faults")

plt.xticks(rotation=45)

# Combine legends from both axes
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines_1 + lines_2,
    labels_1 + labels_2,
    loc="upper left"
)

plt.tight_layout()
plt.show()

#this is using rule-based fault detection, but a more sophisticated approach would be to use machine learning models to detect anomalies based on multiple sensor readings.
#Temperature > 90°C
#        ↓
#     Critical
#        ↓
#Investigate RPM
#        ↓
#RPM also elevated
#        ↓
#Potential multi-sensor fault


