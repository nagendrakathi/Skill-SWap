document.addEventListener('DOMContentLoaded', function() {
    // Flash message timeout
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.display = 'none';
        }, 3000);
    }
    
    // Dynamic content toggling for skill lists
    const skillItems = document.querySelectorAll('.skill-item');
    
    skillItems.forEach(item => {
        const description = item.querySelector('.skill-description');
        const heading = item.querySelector('h4');
        
        if (heading && description) {
            heading.addEventListener('click', () => {
                if (description.style.display === 'none' || description.style.display === '') {
                    description.style.display = 'block';
                } else {
                    description.style.display = 'none';
                }
            });
        }
    });
});