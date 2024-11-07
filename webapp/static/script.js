// System Update Funktionen
function checkSystemUpdates() {
    fetch("/check-system-updates", { method: "GET" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

function installSystemUpdates() {
    fetch("/install-system-updates", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

function setSystemAutoUpdate() {
    const interval = document.getElementById("system-auto-update").value;
    fetch("/set-system-auto-update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interval: interval })
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

// Repository Update Funktionen
function checkRepoUpdates() {
    fetch("/check-repo-updates", { method: "GET" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

function installRepoUpdates() {
    fetch("/install-repo-updates", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

function setRepoAutoUpdate() {
    const interval = document.getElementById("repo-auto-update").value;
    fetch("/set-repo-auto-update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interval: interval })
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Error: " + error.message));
}

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
