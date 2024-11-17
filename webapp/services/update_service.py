import subprocess
import os

def configure_git_identity_and_strategy(repo_path):
    """Ensure Git identity and pull strategy are configured for commits."""
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
        subprocess.run(
            ["git", "-C", repo_path, "config", "pull.rebase", "false"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Git identity and pull strategy configured successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring Git identity or strategy: {e.stderr}")

def check_system_updates():
    """Stream the output of checking system updates."""
    try:
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
    except Exception as e:
        yield f"Error checking system updates: {str(e)}"

def install_system_updates():
    """Stream the output of installing system updates."""
    try:
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
    except Exception as e:
        yield f"Error installing system updates: {str(e)}"

def check_repo_updates():
    """Check for repository updates."""
    repo_path = "/home/test/Bibo"  # Adjusted dynamically in the installation script
    print(f"Checking repository at {repo_path}")

    if not os.path.exists(repo_path):
        error_message = f"Repository not found at {repo_path}"
        print(error_message)
        return {"status": "error", "message": error_message}

    try:
        subprocess.run(
            ["git", "-C", repo_path, "fetch"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        log_process = subprocess.run(
            ["git", "-C", repo_path, "log", "HEAD..origin/main", "--oneline"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        updates = log_process.stdout.strip()

        if updates:
            return {"status": "updates_available", "details": updates}
        else:
            return {"status": "no_updates"}
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if hasattr(e, "stderr") else str(e)
        print(f"Git error: {error_message}")
        return {"status": "error", "message": f"Git error: {error_message}"}
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}

def update_repository():
    """Update the repository by committing local changes before pulling."""
    repo_path = "/home/test/Bibo"
    if not os.path.exists(repo_path):
        return {"status": "error", "message": "Repository not found"}

    try:
        print("Configuring Git identity and pull strategy...")
        configure_git_identity_and_strategy(repo_path)

        print("Checking for uncommitted changes...")
        status_process = subprocess.run(
            ["git", "-C", repo_path, "status", "--porcelain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        uncommitted_changes = status_process.stdout.strip()

        if uncommitted_changes:
            print("Uncommitted changes detected. Committing changes...")
            subprocess.run(
                ["git", "-C", repo_path, "add", "."],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            subprocess.run(
                ["git", "-C", repo_path, "commit", "-m", "Auto-commit local changes before pull"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

        print("Fetching updates...")
        subprocess.run(
            ["git", "-C", repo_path, "fetch"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Performing git pull...")
        pull_process = subprocess.run(
            ["git", "-C", repo_path, "pull"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Git pull output: {pull_process.stdout}")

        status_check = subprocess.run(
            ["git", "-C", repo_path, "status"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "up to date" in status_check.stdout.lower():
            print("Repository is already up to date.")
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
        return {"status": "error", "message": error_message"}
