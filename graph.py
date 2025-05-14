import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd
import json

def get_latest_wind_speed():
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0) 
    return ((CSV_read["WIND_SPEED"].iloc[-1])/100)

def load_latest_wind_speed():
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0) 
    latest_wind_speed = ((CSV_read["WIND_SPEED"].iloc[-1])/100)
    with open("static/data/wind_speed.json", "w") as f:   
        json.dump({"latest_wind_speed": latest_wind_speed}, f)

def wind_speed_data():
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0) # Læser CSV filen
    # pre_Wind_speed_data = CSV_read["WIND_SPEED"].tail(20).tolist()
    pre_Wind_speed_data = [x / 100 for x in CSV_read["WIND_SPEED"].tail(20).tolist()]
    # Eksempel data set
    Wind_speed_data = np.column_stack((np.arange(1, len(pre_Wind_speed_data)+1),pre_Wind_speed_data)) #

    # x og y Wind_speed_data hentes
    x = Wind_speed_data[:, 0]
    y = Wind_speed_data[:, 1]
    

    # Plot 
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.plot(x, y, marker='o', linestyle='-')
    plt.xlabel('Time (60s intervals)')
    plt.ylabel('Wind Speed (m/s)')
    plt.title('Wind Speed Data')
    plt.grid(True)

    plt.xticks(np.arange(min(x), max(x) + 1, 2))  # Justere selv x-aksens størrelse
    plt.xlim(0, max(x))  # Grænser for x-aksen
    #plt.ylim(0, max(y))  # Grænser for y-aksen
    
    y_min = min(y)
    y_max = max(y)
    
    if y_min == y_max:
        plt.ylim(y_min-1,y_max+1)
    else:
        plt.ylim(0,y_max+1)
    plt.yticks(np.arange(0, max(y) + 1, 2))  # Justere selv y-aksens størrelse

    plt.savefig("static/images/winddata")
    plt.close()

def wind_direction_data():
    # Wind direction data indsamling (sidste) 
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0) # Læser CSV filen
    pre_Wind_direction_data = CSV_read["WIND_DIR"].iloc[-1]
    wind_direction = pre_Wind_direction_data
    print(pre_Wind_direction_data)

    # Create a circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x = np.cos(theta)
    y = np.sin(theta)

    # Convert the number (degrees) to radians
    adjust_index = (wind_direction/100-11) % 16
    angle_degrees = adjust_index * 22.5
    print(f"Adjusted Index: {adjust_index}, Angle Degrees: {angle_degrees}")
    radians = np.deg2rad(np.negative(angle_degrees)+90)

    # Calculate the arrow's endpoint
    arrow_x = np.cos(radians)
    arrow_y = np.sin(radians)

    # Plot the circle
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, label="Circle")  # Circle outline
    plt.scatter(0, 0, color="black", label="Center")  # Center point

    # Plot the arrow
    plt.arrow(0, 0, arrow_x, arrow_y, head_width=0.05, head_length=0.1, fc='blue', ec='blue', label="Arrow")

    # Set axis limits and labels
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axhline(0, color='gray', linewidth=0.5)
    plt.axvline(0, color='gray', linewidth=0.5)
    plt.title(f"Arrow pointing at {angle_degrees}°")
    plt.legend()
    plt.grid(True)

    # Save and show the plot
    plt.savefig("static/images/wind_direction.png")
    plt.close()

def power_data():
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0) # Læser CSV filen
    pre_Power_data = [x / 100 for x in CSV_read["POWER"].tail(20).tolist()]
    power_data = pre_Power_data

    # Plot Power data
    plt.figure(figsize=(10, 6))
    plt.plot(power_data, marker='o', linestyle='-')
    plt.xlabel('Time (60s intervals)')
    plt.ylabel('Power (mW)')
    plt.title('Power Data')
    plt.grid(True)

    plt.savefig("static/images/powerdata")
    plt.close()

def get_current_power():
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0)
    current_power = (CSV_read["POWER"].iloc[-1])/100
    with open("static/data/power.json", "w") as f:
        json.dump({"current_power": current_power}, f)

def get_current_direction():
    CSV_read = pd.read_csv("sensor_data.csv", sep=",", header=0)
    current_direction = (CSV_read["WIND_DIR"].iloc[-1])
    adjust_index = (current_direction/100-11) % 16
    angle_degrees = adjust_index * 22.5

    direction= ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    degrees= [0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5]
    adjusted_angle = (angle_degrees + 11.25) % 360

    for i in range(len(degrees)):
        if adjusted_angle >= degrees[i] and adjusted_angle < degrees[i] + 22.5:
            compass_direction = direction[i]
            break

    with open("static/data/wind_direction.json", "w") as f:
        json.dump({"current_direction": compass_direction}, f)

wind_speed_data()
wind_direction_data()
power_data()
