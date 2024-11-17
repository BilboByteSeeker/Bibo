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
    repo_path = "/home/bilbo/Bibo"
    print(f"Checking repository at {repo_path}")  # Debug log

    if not os.path.exists(repo_path):
        error_message = f"Repository not found at {repo_path}"
        print(error_message)  # Debug log
        return {"status": "error", "message": error_message}

    try:
        print("Running git fetch...")  # Debug log
        subprocess.run(
            ["git", "-C", repo_path, "fetch"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Running git log...")  # Debug log
        log_process = subprocess.run(
            ["git", "-C", repo_path, "log", "HEAD..origin/main", "--oneline"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        updates = log_process.stdout.strip()

        if updates:
            print("Updates available")  # Debug log
            return {"status": "updates_available", "details": updates}
        else:
            print("No updates available")  # Debug log
            return {"status": "no_updates"}
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if hasattr(e, "stderr") else str(e)
        print(f"Git error: {error_message}")  # Debug log
        return {"status": "error", "message": f"Git error: {error_message}"}
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)  # Debug log
        return {"status": "error", "message": error_message}

def update_repository():
    """Update the repository."""
    repo_path = "/home/bilbo/Bibo"
    if not os.path.exists(repo_path):
        return {"status": "error", "message": "Repository not found"}
    
    try:
        # Check for uncommitted changes
        status_process = subprocess.run(
            ["git", "-C", repo_path, "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        uncommitted_changes = status_process.stdout.strip()

        if uncommitted_changes:
            return {
                "status": "error",
                "message": "Repository has uncommitted changes. Please commit or stash them before updating."
            }
        
        # Perform the pull
        pull_process = subprocess.run(
            ["git", "-C", repo_path, "pull"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {
            "status": "success",
            "message": "Repository updated successfully",
            "details": pull_process.stdout
        }
    
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if hasattr(e, "stderr") else str(e)
        return {"status": "error", "message": f"Git error: {error_message}"}
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}

