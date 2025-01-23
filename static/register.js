document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    function showMessage(element, message) {
        element.textContent = message;
        element.style.display = 'block';
        setTimeout(() => {
            element.style.display = 'none';
        }, 3000);
    }

    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            showMessage(errorMessage, 'Passwords do not match');
            return;
        }
        
        // Disable the submit button during registration
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = '<span>Registering...</span>';
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();
            
            if (data.success) {
                showMessage(successMessage, 'Registration successful! Redirecting to login...');
                // Clear any error messages
                errorMessage.style.display = 'none';
                
                // Redirect to login page after a short delay
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            } else {
                showMessage(errorMessage, data.message || 'Registration failed. Please try again.');
                submitButton.disabled = false;
                submitButton.innerHTML = '<span>Register</span>';
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage(errorMessage, 'An error occurred during registration. Please try again.');
            submitButton.disabled = false;
            submitButton.innerHTML = '<span>Register</span>';
        }
    });
});
