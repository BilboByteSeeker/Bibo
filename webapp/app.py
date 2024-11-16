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
        for line in iter(process.stdout.readline, ""):
            yield f"data: {line.strip()}|0\n\n"
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
        for line in iter(process.stdout.readline, ""):
            yield f"data: {line.strip()}|0\n\n"
        process.stdout.close()
        process.wait()
        yield "data: INSTALLATION_COMPLETE|100\n\n"

    return Response(generate(), content_type="text/event-stream")

@app.route("/check-repo-updates", methods=["GET"])
def check_repo_updates():
    def generate():
        repo_path = os.path.expanduser("~/Bibo")
        if not os.path.exists(repo_path):
            yield "data: ERROR|Repository not found\n\n"
            return
        try:
            process = subprocess.Popen(
                ["git", "-C", repo_path, "fetch"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            for line in iter(process.stdout.readline, ""):
                yield f"data: {line.strip()}|0\n\n"
            process.stdout.close()
            process.wait()

            updates_available = subprocess.run(
                ["git", "-C", repo_path, "log", "HEAD..origin/main", "--oneline"],
                stdout=subprocess.PIPE,
                text=True
            ).stdout.strip()

            if updates_available:
                yield "data: UPDATES_AVAILABLE|100\n\n"
            else:
                yield "data: NO_UPDATES|100\n\n"
        except Exception as e:
            yield f"data: ERROR|{str(e)}\n\n"

    return Response(generate(), content_type="text/event-stream")

@app.route("/update-repo", methods=["POST"])
def update_repo():
    try:
        repo_path = os.path.expanduser("~/Bibo")
        if not os.path.exists(repo_path):
            return jsonify({"error": "Repository not found"}), 404

        process = subprocess.run(
            ["git", "-C", repo_path, "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return jsonify({"message": "Repository updated", "details": process.stdout}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Update failed: {e.stderr}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
