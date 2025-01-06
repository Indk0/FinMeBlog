// Automatically hide the message after 5 seconds
setTimeout(function () {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        messageContainer.style.opacity = '0'; // Fade out
        setTimeout(() => messageContainer.style.display = 'none', 500); // Remove after fade-out
    }
}, 5000);
