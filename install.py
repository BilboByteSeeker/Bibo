import os
import getpass
import subprocess

def run_command(command, use_sudo=False):
    """Führt einen Shell-Befehl aus."""
    if use_sudo:
        command = f"sudo {command}"
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def main():
    # Benutzer ermitteln, der das Skript gestartet hat
    user = os.environ.get("SUDO_USER", getpass.getuser())
    home_dir = os.path.expanduser(f"~{user}")

    # Update und Installation der notwendigen Pakete
    run_command("apt update && apt upgrade -y", use_sudo=True)
    run_command("apt install python3 python3-pip python3-venv nginx -y", use_sudo=True)
    run_command("pip install flask gunicorn")

    # Einrichten der Webanwendung
    webapp_dir = f"{home_dir}/webapp"
    if not os.path.exists(webapp_dir):
        os.makedirs(webapp_dir)

    # Virtuelle Umgebung erstellen
    run_command(f"python3 -m venv {webapp_dir}/venv")

    # Flask und Gunicorn im virtuellen Environment installieren
    run_command(f"{webapp_dir}/venv/bin/pip install flask gunicorn")

    # Nginx-Konfigurationsdatei erstellen
    nginx_conf_path = "/etc/nginx/sites-available/webapp"
    nginx_conf_content = f"""
server {{
    listen 80;
    server_name _;

    location /static/ {{
        alias {webapp_dir}/static/;
    }}

    location / {{
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }}
}}
"""
    with open("webapp_nginx.conf", "w") as nginx_conf_file:
        nginx_conf_file.write(nginx_conf_content)
    run_command(f"mv webapp_nginx.conf {nginx_conf_path}", use_sudo=True)

    # Symbolischen Link für Nginx erstellen und Nginx neu starten
    if os.path.islink("/etc/nginx/sites-enabled/webapp"):
        run_command("rm /etc/nginx/sites-enabled/webapp", use_sudo=True)
    run_command(f"ln -s {nginx_conf_path} /etc/nginx/sites-enabled/", use_sudo=True)
    run_command("systemctl restart nginx", use_sudo=True)

    # Systemd-Dienstdatei erstellen
    systemd_service_path = "/etc/systemd/system/webapp.service"
    systemd_service_content = f"""
[Unit]
Description=Gunicorn instance to serve webapp
After=network.target

[Service]
User={user}
Group=www-data
WorkingDirectory={webapp_dir}
ExecStart={webapp_dir}/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
"""
    with open("webapp.service", "w") as service_file:
        service_file.write(systemd_service_content)
    run_command(f"mv webapp.service {systemd_service_path}", use_sudo=True)
    run_command("systemctl daemon-reload", use_sudo=True)  # Dienst neu laden
    run_command("systemctl start webapp", use_sudo=True)
    run_command("systemctl enable webapp", use_sudo=True)

    # Sudo-Berechtigungen aktualisieren
    visudo_path = "/etc/sudoers.d/webapp"
    visudo_content = f"""
{user} ALL=(ALL) NOPASSWD: /sbin/shutdown, /sbin/reboot
{user} ALL=(ALL) NOPASSWD: /usr/bin/apt, /usr/bin/git
"""
    with open("webapp_sudoers", "w") as sudoers_file:
        sudoers_file.write(visudo_content)
    run_command(f"mv webapp_sudoers {visudo_path}", use_sudo=True)

    # `app.py` aktualisieren, falls vorhanden
    app_py_path = f"{home_dir}/bibo/app.py"
    if os.path.exists(app_py_path):
        with open(app_py_path, "r") as app_py_file:
            app_content = app_py_file.read()
        updated_content = app_content.replace(
            'REPO_PATH =', f'REPO_PATH = "{home_dir}/bibo"'
        )
        with open(app_py_path, "w") as app_py_file:
            app_py_file.write(updated_content)
        print(f"Updated REPO_PATH in {app_py_path}")
    else:
        print(f"app.py not found in {home_dir}/bibo. Skipping update.")

    print("Setup completed successfully!")

if __name__ == "__main__":
    main()
