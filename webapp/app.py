from flask import Flask, render_template, jsonify, request, redirect
import subprocess
import os

app = Flask(__name__)

# Pfad zu deinem Git-Repository
REPO_PATH = "/home/bilbo/robotest"  # Ersetze diesen Pfad mit deinem tatsächlichen Repository-Pfad

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/controls")
def controls():
    return render_template("controls.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/wifi")
def wifi():
    return render_template("wifi.html")

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/bluetooth")
def bluetooth():
    return render_template("bluetooth.html")

@app.route("/status")
def status():
    internet_connected = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1") == 0
    return jsonify({"status": "Online" if internet_connected else "Offline"})

# System Update Routen
@app.route("/check-system-updates", methods=["GET"])
def check_system_updates():
    try:
        output = subprocess.check_output(["sudo", "apt", "update"], text=True)
        return jsonify({"message": "System updates checked:\n" + output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/install-system-updates", methods=["POST"])
def install_system_updates():
    try:
        output = subprocess.check_output(["sudo", "apt", "upgrade", "-y"], text=True)
        return jsonify({"message": "System updates installed:\n" + output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set-system-auto-update", methods=["POST"])
def set_system_auto_update():
    interval = request.json.get("interval")
    # Implementiere Logik für automatische Updates (z. B. mit Cron-Job)
    return jsonify({"message": f"Automatic system updates set to every {interval} minutes."})

# Repository Update Routen
@app.route("/check-repo-updates", methods=["GET"])
def check_repo_updates():
    try:
        output = subprocess.check_output(
            ["git", "fetch", "origin"], cwd=REPO_PATH, text=True
        )
        return jsonify({"message": "Repository updates checked:\n" + output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/install-repo-updates", methods=["POST"])
def install_repo_updates():
    try:
        output = subprocess.check_output(
            ["git", "pull", "origin", "main"], cwd=REPO_PATH, text=True
        )
        return jsonify({"message": "Repository updates installed:\n" + output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set-repo-auto-update", methods=["POST"])
def set_repo_auto_update():
    interval = request.json.get("interval")
    # Implementiere Logik für automatische Repository-Updates
    return jsonify({"message": f"Automatic repository updates set to every {interval} minutes."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)