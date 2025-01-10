// Automatically hide the message after 5 seconds
setTimeout(function () {
    const messageContainer = document.getElementById('message-container');
    if (messageContainer) {
        messageContainer.style.transition = "opacity 0.5s ease"; // Smooth transition
        messageContainer.style.opacity = '0'; // Fade out
        setTimeout(() => {
            messageContainer.style.display = 'none'; // Remove after fade-out
        }, 500); // Match the transition duration
    }
}, 5000); // Wait for 5 seconds
