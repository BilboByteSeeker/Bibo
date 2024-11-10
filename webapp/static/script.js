document.addEventListener("DOMContentLoaded", () => {
    updateNetworkStatus();
    setInterval(updateNetworkStatus, 10 * 1000); // Update network status every 10 seconds
});

// Update network status
async function updateNetworkStatus() {
    const statusIcon = document.getElementById("status-icon");
    try {
        const response = await fetch("/status");
        const data = await response.json();
        if (data.status === "Online") {
            statusIcon.src = "/static/network-online.png";
            statusIcon.alt = "Network Online";
        } else {
            statusIcon.src = "/static/network-offline.png";
            statusIcon.alt = "Network Offline";
        }
    } catch (error) {
        statusIcon.src = "/static/network-offline.png";
        statusIcon.alt = "Network Error";
    }
}

// Check for system updates
async function checkSystemUpdates() {
    const button = document.getElementById("check-updates-btn");
    const text = button.querySelector(".button-text");
    const spinner = button.querySelector(".loading-spinner");

    button.disabled = true;
    text.classList.add("hidden");
    spinner.classList.remove("hidden");

    try {
        const response = await fetch("/check-system-updates");
        if (!response.ok) {
            throw new Error("Failed to fetch updates");
        }
        const data = await response.json();

        if (data.updatesAvailable) {
            button.classList.add("available");
            text.textContent = `Updates Available (${data.updatesCount})`;
        } else {
            button.classList.remove("available");
            text.textContent = "No Updates";
        }
    } catch (error) {
        button.classList.remove("available");
        text.textContent = "Error checking updates";
        console.error("Error:", error);
    } finally {
        spinner.classList.add("hidden");
        text.classList.remove("hidden");
        button.disabled = false;
    }
}

// Shutdown functionality
async function shutdown() {
    try {
        const response = await fetch("/shutdown", { method: "POST" });
        const data = await response.json();
        alert(data.message || "System shutting down.");
    } catch (error) {
        alert("Error while shutting down.");
    }
}

// Reboot functionality
async function reboot() {
    try {
        const response = await fetch("/reboot", { method: "POST" });
        const data = await response.json();
        alert(data.message || "System rebooting.");
    } catch (error) {
        alert("Error while rebooting.");
    }
}
