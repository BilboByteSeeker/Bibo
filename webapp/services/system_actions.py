import subprocess

def shutdown_system():
    """Shut down the system."""
    try:
        subprocess.run(["sudo", "shutdown", "now"], check=True)
        return {"status": "success"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Shutdown failed: {str(e)}"}

def reboot_system():
    """Reboot the system."""
    try:
        subprocess.run(["sudo", "reboot"], check=True)
        return {"status": "success"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Reboot failed: {str(e)}"}
