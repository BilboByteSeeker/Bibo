document.addEventListener("DOMContentLoaded", () => {
    updateNetworkStatus();
    if (window.location.pathname.includes("/settings/update")) {
        checkSystemUpdates();
    }
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

// Shutdown functionality
async function shutdown() {
    try {
        const response = await fetch("/shutdown", { method: "POST" });
        const data = await response.json();

        if (response.ok) {
            alert(data.message);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert("Error while shutting down the system.");
    }
}

// Reboot functionality
async function reboot() {
    try {
        const response = await fetch("/reboot", { method: "POST" });
        const data = await response.json();

        if (response.ok) {
            alert(data.message);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        alert("Error while rebooting the system.");
    }
}

// Toggle button loading animation
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
