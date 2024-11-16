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

function checkRepoUpdates() {
    const checkButton = document.getElementById("check-repo-btn");
    const spinner = checkButton.querySelector(".loading-spinner");
    const buttonText = checkButton.querySelector(".button-text");
    const progressBar = document.getElementById("repo-progress-bar");
    const progressContainer = document.getElementById("repo-progress-container");
    const progressText = document.getElementById("repo-progress-text");
    const updateRepoButton = document.getElementById("update-repo-btn");

    spinner.classList.remove("hidden");
    buttonText.textContent = "Checking Repository Updates...";
    progressBar.style.width = "0%";
    progressText.textContent = "Starting...";
    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource("/check-repo-updates");

    eventSource.onmessage = (event) => {
        const [output, progress] = event.data.split("|");
        const parsedProgress = parseInt(progress);
        if (output === "UPDATES_AVAILABLE") {
            eventSource.close();
            buttonText.textContent = "Updates Available";
            updateRepoButton.classList.remove("hidden");
            progressBar.style.width = "100%";
            progressText.textContent = "Updates Available";
            spinner.classList.add("hidden");
        } else if (output === "NO_UPDATES") {
            eventSource.close();
            buttonText.textContent = "No Updates Available";
            progressBar.style.width = "100%";
            progressText.textContent = "No Updates Available";
            spinner.classList.add("hidden");
        } else if (output === "ERROR") {
            eventSource.close();
            buttonText.textContent = "Error Checking Updates";
            progressText.textContent = "Error";
            spinner.classList.add("hidden");
        } else if (!isNaN(parsedProgress)) {
            progressBar.style.width = `${parsedProgress}%`;
            progressText.textContent = output;
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        progressText.textContent = "Error Checking Updates";
        buttonText.textContent = "Check Repository Updates";
        spinner.classList.add("hidden");
    };
}

function checkSystemUpdates() {
    const checkButton = document.getElementById("check-updates-btn");
    const spinner = checkButton.querySelector(".loading-spinner");
    const buttonText = checkButton.querySelector(".button-text");
    const progressBar = document.getElementById("progress-bar");
    const progressContainer = document.getElementById("progress-container");
    const progressText = document.getElementById("progress-text");

    spinner.classList.remove("hidden");
    buttonText.textContent = "Checking for Updates...";
    progressBar.style.width = "0%";
    progressText.textContent = "Starting...";
    progressContainer.classList.remove("hidden");

    const eventSource = new EventSource("/check-system-updates");

    eventSource.onmessage = (event) => {
        const [output, progress] = event.data.split("|");
        const parsedProgress = parseInt(progress);
        if (output === "CHECK_COMPLETE") {
            eventSource.close();
            buttonText.textContent = "No Updates Available (Check Again)";
            progressBar.style.width = "100%";
            progressText.textContent = "Check Complete";
            spinner.classList.add("hidden");
        } else if (!isNaN(parsedProgress)) {
            progressBar.style.width = `${parsedProgress}%`;
            progressText.textContent = output;
        }
    };

    eventSource.onerror = () => {
        eventSource.close();
        progressText.textContent = "Error Checking Updates";
        buttonText.textContent = "Check for Updates";
        spinner.classList.add("hidden");
    };
}

function updateRepository() {
    const updateButton = document.getElementById("update-repo-btn");
    const spinner = updateButton.querySelector(".loading-spinner");
    const buttonText = updateButton.querySelector(".button-text");

    spinner.classList.remove("hidden");
    buttonText.textContent = "Updating Repository...";

    fetch("/update-repo", { method: "POST" })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || "Failed to update repository");
                });
            }
        })
        .then(data => {
            buttonText.textContent = "Repository Updated";
            console.log("Update Details:", data.details);
            spinner.classList.add("hidden");
        })
        .catch(error => {
            console.error("Error updating repository:", error);
            buttonText.textContent = "Update Failed";
            spinner.classList.add("hidden");
        });
}
