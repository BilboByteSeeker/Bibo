from flask import Blueprint, render_template

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/")
def settings():
    return render_template("settings.html")

@settings_bp.route("/wifi")
def wifi_settings():
    return render_template("wifi.html")

@settings_bp.route("/bluetooth")
def bluetooth_settings():
    return render_template("bluetooth.html")

@settings_bp.route("/update")
def update_settings():
    return render_template("update.html")
