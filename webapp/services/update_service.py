import subprocess
import os

def check_system_updates():
    """Stream the output of checking system updates."""
    process = subprocess.Popen(
        ["sudo", "apt", "update"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for line in iter(process.stdout.readline, ""):
        yield line
    process.stdout.close()
    process.wait()

def install_system_updates():
    """Stream the output of installing system updates."""
    process = subprocess.Popen(
        ["sudo", "apt", "upgrade", "-y"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    for line in iter(process.stdout.readline, ""):
        yield line
    process.stdout.close()
    process.wait()

def check_repo_updates():
    """Check for repository updates."""
    repo_path = os.path.expanduser("~/Bibo")
    if not os.path.exists(repo_path):
        return {"status": "error", "message": "Repository not found"}
    try:
        subprocess.run(["git", "-C", repo_path, "fetch"], check=True)
        updates = subprocess.run(
            ["git", "-C", repo_path, "log", "HEAD..origin/main", "--oneline"],
            stdout=subprocess.PIPE,
            text=True
        ).stdout.strip()
        if updates:
            return {"status": "updates_available", "details": updates}
        else:
            return {"status": "no_updates"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}

def update_repository():
    """Update the repository."""
    repo_path = os.path.expanduser("~/Bibo")
    if not os.path.exists(repo_path):
        return {"status": "error", "message": "Repository not found"}
    try:
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        return {"status": "success", "message": "Repository updated successfully"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
