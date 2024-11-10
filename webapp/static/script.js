function updateProgressBar(progressBar, progressContainer, spinner, progress, output) {
    // Update the progress bar and text
    progressBar.style.width = `${progress}%`;
    progressBar.textContent = `${progress}% - ${output}`;

    // Hide spinner when progress is 100%
    if (progress === 100) {
        spinner.classList.add("hidden");
    }
}

function checkSystemUpdates() {
    const checkButton = document.getElementById("check-updates-btn");
    const spinner = checkButton.querySelector(".loading-spinner");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");

    // Reset progress and show spinner
    spinner.classList.remove("hidden");
    progressBar.style.width = "0%";
    progressBar.textContent = "";
    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource("/check-system-updates");

    eventSource.onmessage = (event) => {
        const [output, progress] = event.data.split("|");
        const parsedProgress = parseInt(progress);

        console.log("Received event:", { output, progress: parsedProgress }); // Debugging log

        if (output === "CHECK_COMPLETE") {
            eventSource.close();
            updateProgressBar(progressBar, progressContainer, spinner, 100, "Check Complete");
            return;
        }

        if (!isNaN(parsedProgress) && parsedProgress >= 0 && parsedProgress <= 100) {
            updateProgressBar(progressBar, progressContainer, spinner, parsedProgress, output);
        } else {
            console.warn("Invalid progress value received:", progress);
        }
    };

    eventSource.onerror = () => {
        console.error("EventSource error occurred");
        eventSource.close();
        progressBar.textContent = "Error Checking Updates";
        spinner.classList.add("hidden");
    };
}

function installSystemUpdates() {
    const installButton = document.getElementById("install-updates-btn");
    const spinner = installButton.querySelector(".loading-spinner");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");

    // Reset progress and show spinner
    spinner.classList.remove("hidden");
    progressBar.style.width = "0%";
    progressBar.textContent = "";
    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource("/install-updates-stream");

    eventSource.onmessage = (event) => {
        const [output, progress] = event.data.split("|");
        const parsedProgress = parseInt(progress);

        console.log("Received event:", { output, progress: parsedProgress }); // Debugging log

        if (output === "INSTALLATION_COMPLETE") {
            eventSource.close();
            updateProgressBar(progressBar, progressContainer, spinner, 100, "Installation Complete");
            return;
        }

        if (!isNaN(parsedProgress) && parsedProgress >= 0 && parsedProgress <= 100) {
            updateProgressBar(progressBar, progressContainer, spinner, parsedProgress, output);
        } else {
            console.warn("Invalid progress value received:", progress);
        }
    };

    eventSource.onerror = () => {
        console.error("EventSource error occurred");
        eventSource.close();
        progressBar.textContent = "Error Installing Updates";
        spinner.classList.add("hidden");
    };
}

function shutdown() {
    fetch("/shutdown", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message || "Shutting down..."))
        .catch(error => alert("Error shutting down: " + error));
}

function reboot() {
    fetch("/reboot", { method: "POST" })
        .then(response => response.json())
        .then(data => alert(data.message || "Rebooting..."))
        .catch(error => alert("Error rebooting: " + error));
}

function initializeButtons() {
    const buttons = document.querySelectorAll(".button-with-spinner");
    buttons.forEach(button => {
        const spinner = document.createElement("div");
        spinner.className = "loading-spinner hidden";
        button.appendChild(spinner);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initializeButtons();
});
