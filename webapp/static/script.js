// Automatische Überprüfung alle 12 Stunden
document.addEventListener("DOMContentLoaded", () => {
    checkSystemUpdates();
    setInterval(checkSystemUpdates, 12 * 60 * 60 * 1000); // 12 Stunden in Millisekunden
});

// System Update Status anzeigen
async function checkSystemUpdates() {
    const checkButton = document.getElementById("check-updates-btn");
    const statusElement = document.getElementById("update-status");
    toggleButtonLoading(checkButton, true);

    try {
        const response = await fetch("/check-system-updates");
        const data = await response.json();

        if (data.updatesAvailable) {
            statusElement.textContent = "Update verfügbar!";
            statusElement.classList.add("available");
            statusElement.classList.remove("unavailable");
        } else {
            statusElement.textContent = "Keine Updates verfügbar.";
            statusElement.classList.add("unavailable");
            statusElement.classList.remove("available");
        }
    } catch (error) {
        statusElement.textContent = "Fehler beim Prüfen der Updates.";
        statusElement.classList.add("unavailable");
    } finally {
        toggleButtonLoading(checkButton, false);
    }
}

// System Update Installation
async function installSystemUpdates() {
    const installButton = document.getElementById("install-updates-btn");
    toggleButtonLoading(installButton, true);

    try {
        const response = await fetch("/install-system-updates", { method: "POST" });
        const data = await response.json();
        alert(data.message);
    } catch (error) {
        alert("Fehler beim Installieren der Updates.");
    } finally {
        toggleButtonLoading(installButton, false);
    }
}

// Automatische Updates einrichten
function setSystemAutoUpdate() {
    const interval = document.getElementById("system-auto-update-interval").value;
    const enabled = document.getElementById("system-auto-update-toggle").checked;

    const saveButton = document.getElementById("save-interval-btn");
    toggleButtonLoading(saveButton, true);

    fetch("/set-system-auto-update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ interval: interval, enabled: enabled })
    })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => alert("Fehler beim Speichern der automatischen Updates."))
        .finally(() => toggleButtonLoading(saveButton, false));
}

// Hilfsfunktion: Button-Feedback
function toggleButtonLoading(button, isLoading) {
    const textElement = button.querySelector(".button-text");
    const spinnerElement = button.querySelector(".loading-spinner");

    if (isLoading) {
        button.disabled = true;
        textElement.classList.add("hidden");
        spinnerElement.classList.remove("hidden");
    } else {
        button.disabled = false;
        textElement.classList.remove("hidden");
        spinnerElement.classList.add("hidden");
    }
}
