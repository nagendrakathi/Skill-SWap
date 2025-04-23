document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Simple validation
            const username = document.getElementById('username');
            const password = document.getElementById('password');
            
            if (username.value.trim() === '') {
                isValid = false;
                alert('Username cannot be empty');
            }
            
            if (password.value.trim() === '') {
                isValid = false;
                alert('Password cannot be empty');
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});