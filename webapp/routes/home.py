from flask import Blueprint, render_template, redirect

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():
    return redirect("/home")

@home_bp.route("/")
def home():
    return render_template("home.html")
