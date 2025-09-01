import random
import csv
import matplotlib.pyplot as plt
import pandas as pd
import time

# File name
filename = "environment_data.csv"

# Threshold values
PM25_LIMIT = 100
CO2_LIMIT = 1000
NOISE_LIMIT = 70
PH_MIN, PH_MAX = 6.5, 8.5
TDS_LIMIT = 500

# Generate random sensor values
def generate_data():
    return {
        "PM2.5": random.randint(50, 200),
        "CO2": random.randint(400, 2000),
        "Noise": random.randint(40, 100),
        "pH": round(random.uniform(5.5, 9.5), 2),
        "TDS": random.randint(100, 800)
    }

# Write CSV header
with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "PM2.5", "CO2", "Noise", "pH", "TDS", "Alert"])

# Collect 20 readings
for i in range(20):
    data = generate_data()
    alerts = []

    if data["PM2.5"] > PM25_LIMIT: alerts.append("High PM2.5")
    if data["CO2"] > CO2_LIMIT: alerts.append("High CO2")
    if data["Noise"] > NOISE_LIMIT: alerts.append("High Noise")
    if not (PH_MIN <= data["pH"] <= PH_MAX): alerts.append("Unsafe pH")
    if data["TDS"] > TDS_LIMIT: alerts.append("High TDS")

    alert_text = ", ".join(alerts) if alerts else "Normal"

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"),
                         data["PM2.5"], data["CO2"], data["Noise"],
                         data["pH"], data["TDS"], alert_text])

# Read data back
df = pd.read_csv(filename)
print(df.head())

# Plot all parameters
df[["PM2.5","CO2","Noise","TDS"]].plot(kind="line", marker="o", figsize=(10,6))
plt.axhline(y=PM25_LIMIT, color="red", linestyle="--", label="PM2.5 Limit")
plt.axhline(y=CO2_LIMIT, color="green", linestyle="--", label="CO2 Limit")
plt.axhline(y=NOISE_LIMIT, color="blue", linestyle="--", label="Noise Limit")
plt.axhline(y=TDS_LIMIT, color="orange", linestyle="--", label="TDS Limit")
plt.title("Environment Monitoring (Simulated Data)")
plt.xlabel("Readings")
plt.ylabel("Values")
plt.legend()
plt.grid(True)
plt.savefig("environment_dashboard.png")
plt.show()
