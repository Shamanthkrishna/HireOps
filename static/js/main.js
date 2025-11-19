// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)';
    } else {
        navbar.style.boxShadow = '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
    }
    
    lastScroll = currentScroll;
});

// Animate stats on scroll
const animateStats = () => {
    const stats = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent;
                const duration = 2000;
                const increment = 50;
                let current = 0;
                
                // Check if it's a number or text with special characters
                if (finalValue.includes('+')) {
                    const num = parseInt(finalValue.replace(/\D/g, ''));
                    const suffix = finalValue.replace(/[0-9]/g, '');
                    
                    const timer = setInterval(() => {
                        current += Math.ceil(num / (duration / increment));
                        if (current >= num) {
                            target.textContent = num + suffix;
                            clearInterval(timer);
                        } else {
                            target.textContent = current + suffix;
                        }
                    }, increment);
                }
                
                observer.unobserve(target);
            }
        });
    }, { threshold: 0.5 });
    
    stats.forEach(stat => observer.observe(stat));
};

// Run animations when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', animateStats);
} else {
    animateStats();
}

// Feature cards hover effect
document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px)';
    });
    
    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
    });
});

// Check for authentication errors in URL
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('error') === 'auth_failed') {
    const errorMessage = document.createElement('div');
    errorMessage.className = 'error-notification';
    errorMessage.innerHTML = `
        <div style="background: #fee; color: #c00; padding: 1rem; border-radius: 8px; margin: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <strong>Authentication Failed</strong>
            <p style="margin: 0.5rem 0 0 0;">There was an error signing in with Google. Please try again.</p>
        </div>
    `;
    document.body.insertBefore(errorMessage, document.body.firstChild);
    
    // Remove error notification after 5 seconds
    setTimeout(() => {
        errorMessage.style.transition = 'opacity 0.5s';
        errorMessage.style.opacity = '0';
        setTimeout(() => errorMessage.remove(), 500);
    }, 5000);
}
