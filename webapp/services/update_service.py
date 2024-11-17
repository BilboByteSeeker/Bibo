import subprocess
import os

def configure_git_identity(repo_path):
    """Ensure Git identity is configured for commits in the specific repository."""
    try:
        subprocess.run(
            ["git", "-C", repo_path, "config", "user.email", "robot@example.com"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        subprocess.run(
            ["git", "-C", repo_path, "config", "user.name", "Robot System"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Git identity configured successfully.")  # Debug log
    except subprocess.CalledProcessError as e:
        print(f"Error configuring Git identity: {e.stderr}")  # Debug log

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
    """Update the repository by committing local changes before pulling."""
    repo_path = "/home/bilbo/Bibo"
    if not os.path.exists(repo_path):
        return {"status": "error", "message": "Repository not found"}

    try:
        # Configure Git identity
        print("Configuring Git identity...")  # Debug log
        configure_git_identity(repo_path)

        # Check for uncommitted changes
        print("Checking for uncommitted changes...")  # Debug log
        status_process = subprocess.run(
            ["git", "-C", repo_path, "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        uncommitted_changes = status_process.stdout.strip()

        if uncommitted_changes:
            print("Uncommitted changes detected. Committing changes...")  # Debug log
            commit_process = subprocess.run(
                ["git", "-C", repo_path, "add", "."],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"Git add output: {commit_process.stdout}")  # Debug log

            commit_process = subprocess.run(
                ["git", "-C", repo_path, "commit", "-m", "Auto-commit local changes before pull"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(f"Git commit output: {commit_process.stdout}")  # Debug log

        # Perform the pull
        print("Performing git pull...")  # Debug log
        pull_process = subprocess.run(
            ["git", "-C", repo_path, "pull"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Git pull output: {pull_process.stdout}")  # Debug log

        return {
            "status": "success",
            "message": "Repository updated successfully",
            "details": pull_process.stdout
        }
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if hasattr(e, "stderr") else str(e)
        print(f"Git error: {error_message}")
        return {"status": "error", "message": f"Git error: {error_message}"}
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(f"Unexpected error: {error_message}")
        return {"status": "error", "message": error_message}
