from flask import Flask, render_template, jsonify, request, redirect, Response
import subprocess
import os

app = Flask(__name__)

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

@app.route("/settings/wifi")
def settings_wifi():
    return render_template("wifi.html")

@app.route("/settings/update")
def settings_update():
    return render_template("update.html")

@app.route("/settings/bluetooth")
def settings_bluetooth():
    return render_template("bluetooth.html")

@app.route("/status")
def status():
    internet_connected = os.system("ping -c 1 8.8.8.8 > /dev/null 2>&1") == 0
    return jsonify({"status": "Online" if internet_connected else "Offline"})

@app.route("/shutdown", methods=["POST"])
def shutdown():
    try:
        subprocess.run(["sudo", "shutdown", "now"], check=True)
        return jsonify({"message": "System is shutting down."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Shutdown failed: {e}"}), 500

@app.route("/reboot", methods=["POST"])
def reboot():
    try:
        subprocess.run(["sudo", "reboot"], check=True)
        return jsonify({"message": "System is rebooting."}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Reboot failed: {e}"}), 500

@app.route("/check-system-updates", methods=["GET"])
def check_system_updates():
    def generate():
        process = subprocess.Popen(
            ["sudo", "apt", "update"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        total_lines = 20  # Approximation for update process
        current_line = 0
        for line in iter(process.stdout.readline, ""):
            current_line += 1
            progress = min(int((current_line / total_lines) * 100), 100)
            yield f"data: {line.strip()}|{progress}\n\n"
        process.stdout.close()
        process.wait()
        yield "data: CHECK_COMPLETE|100\n\n"

    return Response(generate(), content_type="text/event-stream")

@app.route("/install-updates-stream", methods=["GET"])
def install_updates_stream():
    def generate():
        process = subprocess.Popen(
            ["sudo", "apt", "upgrade", "-y"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        total_lines = 50  # Approximation for upgrade process
        current_line = 0
        for line in iter(process.stdout.readline, ""):
            current_line += 1
            progress = min(int((current_line / total_lines) * 100), 100)
            yield f"data: {line.strip()}|{progress}\n\n"
        process.stdout.close()
        process.wait()
        yield "data: INSTALLATION_COMPLETE|100\n\n"

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
