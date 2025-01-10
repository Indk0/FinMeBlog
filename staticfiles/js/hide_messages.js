document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelector('.messages'); // Select the messages element
    if (messages) {
        setTimeout(function () {
            messages.style.transition = "opacity 0.5s ease"; // Add a fade-out effect
            messages.style.opacity = 0;

            setTimeout(function () {
                messages.style.display = 'none'; // Hide the element completely after fade-out
            }, 500); // Match the transition duration (0.5s)
        }, 5000); // Wait 5 seconds before starting the fade-out
    }
});
