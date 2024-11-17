from flask import Flask
from routes.home import home_bp
from routes.settings import settings_bp
from routes.controls import controls_bp
from routes.system import system_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(home_bp, url_prefix="/home")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(controls_bp, url_prefix="/controls")
    app.register_blueprint(system_bp, url_prefix="/system")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
