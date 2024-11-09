from flask import Flask, render_template, jsonify, request, redirect
import subprocess
import os

app = Flask(__name__)

# Base route
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
    # Check internet connection status
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
    try:
        # Update package list
        update_result = subprocess.run(
            ["sudo", "apt", "update"], check=True, capture_output=True, text=True
        )
        print(f"APT Update Output:\n{update_result.stdout}")

        # Check for upgradable packages
        list_result = subprocess.check_output(
            ["sudo", "apt", "list", "--upgradable"], text=True
        )
        updates_available = "upgradable" in list_result.lower()
        print(f"APT List Output:\n{list_result}")

        return jsonify({"updatesAvailable": updates_available, "message": list_result})
    except subprocess.CalledProcessError as e:
        print(f"Error during update check: {e.stderr}")
        return jsonify({"error": f"Command failed: {e.stderr}"}), 500
    except Exception as ex:
        print(f"Unexpected error: {str(ex)}")
        return jsonify({"error": f"Unexpected error: {str(ex)}"}), 500

@app.route("/install-system-updates", methods=["POST"])
def install_system_updates():
    try:
        # Install updates
        install_result = subprocess.check_output(
            ["sudo", "apt", "upgrade", "-y"], text=True
        )
        print(f"APT Install Output:\n{install_result}")

        return jsonify({"message": "System updates installed successfully."}), 200
    except subprocess.CalledProcessError as e:
        print(f"Error during updates installation: {e.stderr}")
        return jsonify({"error": f"Installation failed: {e.stderr}"}), 500
    except Exception as ex:
        print(f"Unexpected error: {str(ex)}")
        return jsonify({"error": f"Unexpected error: {str(ex)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
