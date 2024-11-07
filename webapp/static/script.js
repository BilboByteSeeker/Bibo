// System Update Funktionen
function checkSystemUpdates() {
    fetch("/check-system-updates", { method: "GET" })
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById("system-update-status");
            if (data.updatesAvailable) {
                statusElement.textContent = "Updates verfügbar!";
                statusElement.classList.remove("unavailable");
                statusElement.classList.add("available");
            } else {
                statusElement.textContent = "Keine Updates verfügbar.";
                statusElement.classList.remove("available");
                statusElement.classList.add("unavailable");
            }
            alert(data.message); // Zeigt die Details des Updates an
        })
        .catch(error => alert("Error: " + error.message));
}

function installSystemUpdates() {
    fetch("/install-system-updates", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

function setSystemAutoUpdate() {
    const interval = document.getElementById("system-auto-update-interval").value;
    const enabled = document.getElementById("system-auto-update-toggle").checked;
    fetch("/set-system-auto-update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interval: interval, enabled: enabled })
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

// Repository Update Funktionen
function checkRepoUpdates() {
    fetch("/check-repo-updates", { method: "GET" })
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById("repo-update-status");
            if (data.updatesAvailable) {
                statusElement.textContent = "Updates verfügbar!";
                statusElement.classList.remove("unavailable");
                statusElement.classList.add("available");
            } else {
                statusElement.textContent = "Keine Updates verfügbar.";
                statusElement.classList.remove("available");
                statusElement.classList.add("unavailable");
            }
            alert(data.message); // Zeigt die Details des Updates an
        })
        .catch(error => alert("Error: " + error.message));
}

function installRepoUpdates() {
    fetch("/install-repo-updates", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

function setRepoAutoUpdate() {
    const interval = document.getElementById("repo-auto-update-interval").value;
    const enabled = document.getElementById("repo-auto-update-toggle").checked;
    fetch("/set-repo-auto-update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interval: interval, enabled: enabled })
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

// Funktionen für Schiebeschalter
document.getElementById("system-auto-update-toggle").addEventListener("change", function () {
    const settings = document.getElementById("system-auto-update-settings");
    if (this.checked) {
        settings.classList.remove("hidden");
    } else {
        settings.classList.add("hidden");
    }
});

document.getElementById("repo-auto-update-toggle").addEventListener("change", function () {
    const settings = document.getElementById("repo-auto-update-settings");
    if (this.checked) {
        settings.classList.remove("hidden");
    } else {
        settings.classList.add("hidden");
    }
});

// Online-Status aktualisieren
async function updateStatus() {
    const response = await fetch("/status");
    const data = await response.json();
    const statusIcon = document.getElementById("status-icon");

    if (data.status === "Online") {
        statusIcon.src = "/static/network-online.png";
        statusIcon.alt = "Online";
    } else {
        statusIcon.src = "/static/network-offline.png";
        statusIcon.alt = "Offline";
    }
}

// Initialisierung
updateStatus();
