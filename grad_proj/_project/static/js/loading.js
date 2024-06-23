
// Function to add the class when the script starts running
function startLoading() {
    var loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.classList.add('activeloop');
    }
}

// Function to remove the class when the window finishes loading
function stopLoading() {
    var loadingDiv = document.getElementById('loading');
    if (loadingDiv) {
        loadingDiv.classList.remove('activeloop');
    }
}

// Add the class when the script starts running
startLoading();

// Remove the class when the window finishes loading
window.addEventListener('load', stopLoading);
