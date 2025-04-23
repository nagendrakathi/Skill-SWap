document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Username validation
            const username = document.getElementById('username');
            const usernameError = document.getElementById('username-error');
            
            if (username.value.length < 3) {
                usernameError.textContent = 'Username must be at least 3 characters long';
                isValid = false;
            } else {
                usernameError.textContent = '';
            }
            
            // Email validation
            const email = document.getElementById('email');
            const emailError = document.getElementById('email-error');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (!emailRegex.test(email.value)) {
                emailError.textContent = 'Please enter a valid email address';
                isValid = false;
            } else {
                emailError.textContent = '';
            }
            
            // Password validation
            const password = document.getElementById('password');
            const passwordError = document.getElementById('password-error');
            
            if (password.value.length < 6) {
                passwordError.textContent = 'Password must be at least 6 characters long';
                isValid = false;
            } else {
                passwordError.textContent = '';
            }
            
            // Confirm password validation
            const confirmPassword = document.getElementById('confirm-password');
            const confirmPasswordError = document.getElementById('confirm-password-error');
            
            if (password.value !== confirmPassword.value) {
                confirmPasswordError.textContent = 'Passwords do not match';
                isValid = false;
            } else {
                confirmPasswordError.textContent = '';
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
});