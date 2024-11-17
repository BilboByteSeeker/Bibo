from flask import Blueprint, jsonify, Response
from services.system_actions import shutdown_system, reboot_system
from services.update_service import check_system_updates, install_system_updates, check_repo_updates, update_repository

system_bp = Blueprint("system", __name__)

@system_bp.route("/shutdown", methods=["POST"])
def shutdown():
    result = shutdown_system()
    if result["status"] == "success":
        return jsonify({"message": "System is shutting down."}), 200
    return jsonify({"error": result["message"]}), 500

@system_bp.route("/reboot", methods=["POST"])
def reboot():
    result = reboot_system()
    if result["status"] == "success":
        return jsonify({"message": "System is rebooting."}), 200
    return jsonify({"error": result["message"]}), 500

@system_bp.route("/check-system-updates", methods=["GET"])
def check_system_updates_route():
    def generate():
        for line in check_system_updates():
            yield f"data: {line.strip()}|0\n\n"
        yield "data: CHECK_COMPLETE|100\n\n"

    return Response(generate(), content_type="text/event-stream")

@system_bp.route("/install-system-updates", methods=["GET"])
def install_system_updates_route():
    def generate():
        for line in install_system_updates():
            yield f"data: {line.strip()}|0\n\n"
        yield "data: INSTALLATION_COMPLETE|100\n\n"

    return Response(generate(), content_type="text/event-stream")

@system_bp.route("/check-repo-updates", methods=["GET"])
def check_repo_updates_route():
    result = check_repo_updates()
    if result["status"] == "error":
        return jsonify({"error": result["message"]}), 500
    return jsonify(result), 200

@system_bp.route("/update-repo", methods=["POST"])
def update_repo_route():
    result = update_repository()
    if result["status"] == "error":
        return jsonify({"error": result["message"]}), 500
    return jsonify(result), 200
