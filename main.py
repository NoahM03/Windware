from flask import Flask, render_template, jsonify
import subprocess
from threading import Timer
from graph import get_latest_wind_speed

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Timer flag (tjekker om timeren skal stoppe)
stop_timer = False

def Data():
    if stop_timer:
        return  # Hvis timeren er true, returner vi og stopper funktionen
    subprocess.run(["python", "graph.py"])
    Timer(30, Data).start()

@app.route("/windwaredata.html")
def windwaredata():
    Data()
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
    if get_latest_wind_speed() >= limit:
        return jsonify({"warning": True, "message": f'Wind speed warning! The wind speed has reached {get_latest_wind_speed()}!'})
    return jsonify({"warning": False})


# app.run(use_reloader=True, host="0.0.0.0", port=5000)