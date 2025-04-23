document.addEventListener('DOMContentLoaded', function() {
    // Auto-scroll to the bottom of message list
    const messageList = document.getElementById('message-list');
    
    if (messageList) {
        messageList.scrollTop = messageList.scrollHeight;
    }
    
    // Form submission handling
    const messageForm = document.getElementById('message-form');
    const messageContent = document.getElementById('content');
    
    if (messageForm) {
        messageForm.addEventListener('submit', function(event) {
            if (messageContent.value.trim() === '') {
                event.preventDefault();
                alert('Message cannot be empty');
            }
        });
    }
    
    // Flash message timeout
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.display = 'none';
        }, 3000);
    }
    
    // Enable real-time message updates (could be expanded with WebSockets)
    function checkForNewMessages() {
        // This would typically use fetch or WebSockets to check for new messages
        // For now, just reload the page every 30 seconds
        setTimeout(() => {
            window.location.reload();
        }, 30000);
    }
    
    // Start checking for new messages
    checkForNewMessages();
});