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
        output = subprocess.check_output(["sudo", "apt", "list", "--upgradable"], text=True)
        updates_available = "upgradable" in output
        return jsonify({"updatesAvailable": updates_available, "message": output})
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
    auto_update_enabled = request.json.get("enabled")
    if auto_update_enabled:
        # Logik zur Einrichtung eines Cron-Jobs für automatische Updates
        cron_job = f"*/{interval} * * * * sudo apt update && sudo apt upgrade -y\n"
        with open("/etc/cron.d/system_auto_update", "w") as cron_file:
            cron_file.write(cron_job)
        return jsonify({"message": f"Automatic system updates enabled every {interval} minutes."})
    else:
        # Deaktivieren des Cron-Jobs
        if os.path.exists("/etc/cron.d/system_auto_update"):
            os.remove("/etc/cron.d/system_auto_update")
        return jsonify({"message": "Automatic system updates disabled."})

# Repository Update Routen
@app.route("/check-repo-updates", methods=["GET"])
def check_repo_updates():
    try:
        output = subprocess.check_output(["git", "fetch", "--dry-run"], cwd=REPO_PATH, text=True)
        updates_available = bool(output.strip())
        return jsonify({"updatesAvailable": updates_available, "message": output})
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
    auto_update_enabled = request.json.get("enabled")
    if auto_update_enabled:
        # Logik zur Einrichtung eines Cron-Jobs für automatische Repository-Updates
        cron_job = f"*/{interval} * * * * cd {REPO_PATH} && git pull origin main\n"
        with open("/etc/cron.d/repo_auto_update", "w") as cron_file:
            cron_file.write(cron_job)
        return jsonify({"message": f"Automatic repository updates enabled every {interval} minutes."})
    else:
        # Deaktivieren des Cron-Jobs
        if os.path.exists("/etc/cron.d/repo_auto_update"):
            os.remove("/etc/cron.d/repo_auto_update")
        return jsonify({"message": "Automatic repository updates disabled."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
