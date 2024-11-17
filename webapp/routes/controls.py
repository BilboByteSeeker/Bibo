from flask import Blueprint, render_template

controls_bp = Blueprint("controls", __name__)

@controls_bp.route("/")
def controls():
    return render_template("controls.html")
