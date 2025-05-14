from flask import Flask, render_template, jsonify
# import subprocess
import threading
from graph import get_latest_wind_speed, wind_speed_data, wind_direction_data
from receive_data_raspberry import start_receiver_thread
import time

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
        except Exception as e:
            print(f"[Graph loader] Error: {e}")
        time.sleep(60)
            
    

threading.Thread(target=Data, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/windwaredata.html")
def windwaredata():
    return render_template("windwaredata.html")

@app.route("/about us.html")
def about_us():
    return render_template("about us.html")

@app.route("/downloaddata.html")
def downloaddata():
    return render_template("downloaddata.html")

# Ny route til at stoppe timeren
@app.route("/check_limit")
def check_limit():
    limit = 13  # Sætter grænsen for vindhastighed
    latest_wind_speed = get_latest_wind_speed()
    if latest_wind_speed >= limit:
        return jsonify({"warning": True, "message": f'Wind speed warning! The wind speed has reached {latest_wind_speed}!'})
    return jsonify({"warning": False})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)