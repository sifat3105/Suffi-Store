document.addEventListener("DOMContentLoaded", function() {
    const importButton = document.getElementById("import-button");
    if (!importButton) return;

    const overlay = document.createElement("div");
    overlay.className = "loader-overlay";
    overlay.style.display = "none";

    const loader = document.createElement("div");
    loader.className = "loader";

    const message = document.createElement("div");
    message.className = "loader-message";
    message.textContent = "Uploading and processing file...";

    overlay.appendChild(loader);
    overlay.appendChild(message);
    document.body.appendChild(overlay);

    importButton.addEventListener("click", function(e) {
        const fileInput = document.querySelector("input[name='excel_file']");
        if (!fileInput || !fileInput.value) {
            alert("Please select an Excel file first!");
            return;  // stop here if no file selected
        }

        overlay.style.display = "flex";  // show loader
        message.textContent = "Uploading and processing file...";
    });
});
