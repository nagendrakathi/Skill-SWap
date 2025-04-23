document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality for requests
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to current button and content
            button.classList.add('active');
            const tabId = button.dataset.tab;
            document.getElementById(`${tabId}-requests`).classList.add('active');
        });
    });
    
    // Flash message timeout
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.display = 'none';
        }, 3000);
    }
    
    // Request action confirmation
    const acceptButtons = document.querySelectorAll('.accept-button');
    const rejectButtons = document.querySelectorAll('.reject-button');
    
    acceptButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to accept this request?')) {
                event.preventDefault();
            }
        });
    });
    
    rejectButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to reject this request?')) {
                event.preventDefault();
            }
        });
    });
});