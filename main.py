from flask import Flask, render_template, jsonify, send_file
# import subprocess
import threading
from graph import get_latest_wind_speed, wind_speed_data, wind_direction_data, load_latest_wind_speed, get_current_direction, power_data, get_current_power, prep_download_data
from receive_data_raspberry import start_receiver_thread
import time
import json

app = Flask(__name__)

# Timer flag (tjekker om timeren skal stoppe)
stop_timer = False

start_receiver_thread()

def Data():
    while True:
        try:
            get_latest_wind_speed()
            wind_speed_data()
            wind_direction_data()
            load_latest_wind_speed()
            get_current_direction()
            power_data()
            get_current_power()
        except Exception as e:
            print(f"[Graph loader] Error: {e}")
        time.sleep(5)

threading.Thread(target=Data, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/windwaredata.html")
def windwaredata():
    with open("static/data/wind_speed.json", "r") as f:
        data = json.load(f)
    with open("static/data/wind_direction.json", "r") as f:
        data2 = json.load(f)
    with open("static/data/power.json", "r") as f:
        data3 = json.load(f)
    return render_template("windwaredata.html", wind_speed=data["latest_wind_speed"], direction=data2["current_direction"], power=data3["current_power"])

@app.route("/about us.html")
def about_us():
    return render_template("about us.html")

@app.route("/downloaddata.html")
def downloaddata():
    return render_template("downloaddata.html")

# Ny route til at stoppe timeren
@app.route("/check_limit")
def check_limit():
    limit = 17  # Sætter grænsen for vindhastighed
    latest_wind_speed = get_latest_wind_speed()
    if latest_wind_speed >= limit:
        return jsonify({"warning": True, "message": f'Wind speed warning! The wind speed has reached {latest_wind_speed} ms/s!'})
    return jsonify({"warning": False})

@app.route("/no_power_when_wind_speed")
def no_power_when_wind_speed():
    latest_wind_speed = get_latest_wind_speed()
    latest_power = get_current_power()
    print(latest_power,latest_wind_speed)
    if latest_wind_speed >= 10 and latest_power == 0.0:
        return jsonify({"warning": True, "message": f'Power warning! There is no generated power when wind speed is {latest_wind_speed} ms/s!'})
    return jsonify({"warning": False})

@app.route("/download_data")
def download_data():
    prep_download_data()
    return send_file("static/download/sensor_data_copy.csv", as_attachment=True)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)