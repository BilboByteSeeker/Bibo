document.addEventListener("DOMContentLoaded", () => {
    initializeButtons();
});

function initializeButtons() {
    const buttons = document.querySelectorAll(".button-with-spinner");
    buttons.forEach(button => {
        const spinner = document.createElement("div");
        spinner.className = "loading-spinner hidden";
        button.appendChild(spinner);
    });
}

function shutdown() {
    fetch("/shutdown", { method: "POST" })
        .then(response => {
            if (response.ok) {
                alert("The system is shutting down.");
            } else {
                alert("Failed to shutdown the system.");
            }
        })
        .catch(error => {
            console.error("Error during shutdown:", error);
        });
}

function reboot() {
    fetch("/reboot", { method: "POST" })
        .then(response => {
            if (response.ok) {
                alert("The system is rebooting.");
            } else {
                alert("Failed to reboot the system.");
            }
        })
        .catch(error => {
            console.error("Error during reboot:", error);
        });
}

function updateProgressBar(progressBar, progressContainer, spinner, progress, output) {
    progressBar.style.width = `${progress}%`;
    const progressText = document.getElementById("progress-text");
    progressText.textContent = `${progress}% - ${output}`;
    if (progress === 100) {
        spinner.classList.add("hidden");
    }
}

function checkSystemUpdates() {
    const checkButton = document.getElementById("check-updates-btn");
    const spinner = checkButton.querySelector(".loading-spinner");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");
    const progressText = document.getElementById("progress-text");

    spinner.classList.remove("hidden");
    progressBar.style.width = "0%";
    progressText.textContent = "Starting...";
    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource("/check-system-updates");

    eventSource.onmessage = (event) => {
        const [output, progress] = event.data.split("|");
        const parsedProgress = parseInt(progress);
        if (output === "CHECK_COMPLETE") {
            eventSource.close();
            updateProgressBar(progressBar, progressContainer, spinner, 100, "Check Complete");
            return;
        }
        if (!isNaN(parsedProgress)) {
            updateProgressBar(progressBar, progressContainer, spinner, parsedProgress, output);
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        progressText.textContent = "Error Checking Updates";
        spinner.classList.add("hidden");
    };
}

function installSystemUpdates() {
    const installButton = document.getElementById("install-updates-btn");
    const spinner = installButton.querySelector(".loading-spinner");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");
    const progressText = document.getElementById("progress-text");

    spinner.classList.remove("hidden");
    progressBar.style.width = "0%";
    progressText.textContent = "Starting...";
    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource("/install-updates-stream");

    eventSource.onmessage = (event) => {
        const [output, progress] = event.data.split("|");
        const parsedProgress = parseInt(progress);
        if (output === "INSTALLATION_COMPLETE") {
            eventSource.close();
            updateProgressBar(progressBar, progressContainer, spinner, 100, "Installation Complete");
            return;
        }
        if (!isNaN(parsedProgress)) {
            updateProgressBar(progressBar, progressContainer, spinner, parsedProgress, output);
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        progressText.textContent = "Error Installing Updates";
        spinner.classList.add("hidden");
    };
}
