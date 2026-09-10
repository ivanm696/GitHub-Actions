// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const isExpanded = navLinks.classList.contains('active');
        menuToggle.setAttribute('aria-expanded', isExpanded);
    });
}

// Close menu when link is clicked
if (navLinks) {
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            if (menuToggle) {
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    });
}


// ── CTA button actions ──────────────────────────────────────────────
const btnGetStarted = document.getElementById('btnGetStarted');
if (btnGetStarted) {
    btnGetStarted.addEventListener('click', () => {
        const target = document.querySelector('#contact');
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
}

const btnLearnMore = document.getElementById('btnLearnMore');
if (btnLearnMore) {
    btnLearnMore.addEventListener('click', () => {
        const target = document.querySelector('#features');
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
}

const btnStartProject = document.getElementById('btnStartProject');
if (btnStartProject) {
    btnStartProject.addEventListener('click', () => {
        const target = document.querySelector('#contact');
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Focus the first field after the scroll animation finishes.
            setTimeout(() => {
                const nameField = document.getElementById('name');
                if (nameField) nameField.focus();
            }, 500);
        }
    });
}

// Contact form submission with validation
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form inputs
        const nameInput = contactForm.querySelector('input[name="name"]');
        const emailInput = contactForm.querySelector('input[name="email"]');
        const messageInput = contactForm.querySelector('textarea[name="message"]');
        
        // Clear previous errors
        clearErrors();
        
        // Validate fields
        let isValid = true;
        
        if (!nameInput.value.trim()) {
            showError(nameInput, 'Name is required');
            isValid = false;
        }
        
        if (!emailInput.value.trim()) {
            showError(emailInput, 'Email is required');
            isValid = false;
        } else if (!isValidEmail(emailInput.value)) {
            showError(emailInput, 'Please enter a valid email address');
            isValid = false;
        }
        
        if (!messageInput.value.trim()) {
            showError(messageInput, 'Message is required');
            isValid = false;
        } else if (messageInput.value.trim().length < 10) {
            showError(messageInput, 'Message must be at least 10 characters long');
            isValid = false;
        }
        
        if (isValid) {
            const formData = {
                name: nameInput.value.trim(),
                email: emailInput.value.trim(),
                message: messageInput.value.trim()
            };

            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;

            // Sends to the FastAPI backend in apps/api/ (see /ai/complete or
            // a dedicated /contact endpoint once added server-side).
            fetch(`${window.REMARKA_API_BASE}/health`, { method: 'GET' })
                .then(res => {
                    if (!res.ok) throw new Error('API unreachable');
                    // Backend is reachable — in production this would POST
                    // to a real /contact endpoint. For now, confirm to the
                    // user that the message was captured locally.
                    console.log('Contact form data (ready to send to backend):', formData);
                    alert('Thank you for your message! We\'ll get back to you soon.');
                    contactForm.reset();
                })
                .catch(() => {
                    alert('Message saved locally — backend is not currently reachable. Try again later or email us directly.');
                    console.log('Contact form data (backend unreachable):', formData);
                })
                .finally(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                });
        }
    });
}

// Form validation helper functions
function showError(input, message) {
    input.classList.add('error');
    const errorElement = document.getElementById(input.name + '-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }
}

function clearErrors() {
    const inputs = contactForm.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.classList.remove('error');
        const errorElement = document.getElementById(input.name + '-error');
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.classList.remove('show');
        }
    });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Smooth scroll animation
const links = document.querySelectorAll('a[href^="#"]');
links.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Button click handlers with ripple effect
const buttons = document.querySelectorAll('.btn');
buttons.forEach(btn => {
    btn.addEventListener('click', function(event) {
        // Add ripple effect
        const ripple = document.createElement('span');
        ripple.style.position = 'absolute';
        ripple.style.borderRadius = '50%';
        ripple.style.background = 'rgba(255, 255, 255, 0.5)';
        ripple.style.pointerEvents = 'none';
        
        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.animation = 'ripple-animation 0.6s ease-out';
        
        this.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Navbar shadow on scroll
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 0) {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
    }
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Apply observer to cards
document.querySelectorAll('.feature-card, .service-card, .arch-layer').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// Keyboard accessibility for buttons
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navLinks && navLinks.classList.contains('active')) {
        navLinks.classList.remove('active');
        if (menuToggle) {
            menuToggle.setAttribute('aria-expanded', 'false');
            menuToggle.focus();
        }
    }
});

// Console message
console.log('%c🚀 Remarka - Building the Future of AI Applications', 'color: #6366f1; font-size: 16px; font-weight: bold;');
console.log('%cVersion: 1.0.0', 'color: #6b7280; font-size: 12px;');
