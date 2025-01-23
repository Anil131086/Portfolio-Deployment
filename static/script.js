document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    function showMessage(message, type) {
        const messageDiv = document.getElementById(type === 'error' ? 'error-message' : 'success-message');
        messageDiv.textContent = message;
        messageDiv.style.display = 'block';
        
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 3000);
    }

    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const rememberMe = document.getElementById('rememberMe').checked;
        
        // Disable the submit button during login
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        submitButton.innerHTML = '<span>Logging in...</span>';
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    remember_me: rememberMe
                })
            });

            const data = await response.json();
            
            if (data.success) {
                window.location.href = '/portfolio';  // Redirect to portfolio page
                // Clear any error messages
                errorMessage.style.display = 'none';
            } else {
                showMessage(data.message || 'Login failed. Please check your credentials.', 'error');
                submitButton.disabled = false;
                submitButton.innerHTML = '<span>Login</span>';
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred during login', 'error');
            submitButton.disabled = false;
            submitButton.innerHTML = '<span>Login</span>';
        }
    });

    // Check for remember me token on page load
    const token = document.cookie.split('; ').find(row => row.startsWith('remember_token='));
    if (token) {
        // Auto-fill the remember me checkbox
        document.getElementById('rememberMe').checked = true;
    }
});
