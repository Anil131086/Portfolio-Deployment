// Navigation and Section Display
document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-link');
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    // Navigation handling
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.classList.contains('logout')) {
                // Handle logout
                fetch('/logout', {
                    method: 'POST',
                    credentials: 'include'
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = '/';
                    }
                })
                .catch(error => console.error('Error:', error));
                return;
            }

            e.preventDefault();
            const targetId = link.getAttribute('href').slice(1);

            // Update active states
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetId) {
                    section.classList.add('active');
                }
            });

            // Close mobile menu if open
            navMenu.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });

    // Mobile menu toggle
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Contact form handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value
            };

            fetch('/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Message sent successfully!');
                    contactForm.reset();
                } else {
                    alert('Error sending message. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error sending message. Please try again.');
            });
        });
    }

    // Form input animation
    const formInputs = document.querySelectorAll('.form-group input, .form-group textarea');
    formInputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', () => {
            if (!input.value) {
                input.parentElement.classList.remove('focused');
            }
        });
    });
});
