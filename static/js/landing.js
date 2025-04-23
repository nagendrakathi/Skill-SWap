document.addEventListener('DOMContentLoaded', function() {
    // Simple content reveal functionality
    const featuresSection = document.getElementById('feature-blocks');
    if (featuresSection) {
        const features = featuresSection.querySelectorAll('.feature');
        features.forEach(feature => {
            feature.classList.remove('hidden');
        });
    }

    // Basic content toggling for mobile 
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const navMenu = document.querySelector('nav ul');
    
    if (mobileMenuToggle && navMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            if (navMenu.style.display === 'block') {
                navMenu.style.display = 'none';
            } else {
                navMenu.style.display = 'block';
            }
        });
    }
});