// Dashboard initialization
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
});

function initializeDashboard() {
    // Sidebar navigation
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // Add active class to clicked item
            this.classList.add('active');
            
            // Show corresponding section (placeholder for now)
            const section = this.getAttribute('href').substring(1);
            showSection(section);
        });
    });
    
    // Quick action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.querySelector('span').textContent;
            showPlaceholderMessage(action);
        });
    });
    
    // Animate stats on load
    animateDashboardStats();
}

function showSection(sectionName) {
    // Placeholder function for section switching
    console.log(`Switching to section: ${sectionName}`);
    
    // Show a temporary message
    showPlaceholderMessage(`${sectionName.charAt(0).toUpperCase() + sectionName.slice(1)} section coming in Phase 2`);
}

function showPlaceholderMessage(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
        max-width: 300px;
    `;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <i class="fas fa-info-circle" style="font-size: 1.25rem;"></i>
            <div>
                <strong style="display: block; margin-bottom: 0.25rem;">Feature Preview</strong>
                <span style="font-size: 0.875rem;">${message}</span>
            </div>
        </div>
    `;
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transition = 'all 0.3s ease-out';
        notification.style.transform = 'translateX(400px)';
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function animateDashboardStats() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        const duration = 1500;
        const increment = 50;
        let current = 0;
        
        const timer = setInterval(() => {
            current += Math.ceil(finalValue / (duration / increment));
            if (current >= finalValue) {
                stat.textContent = finalValue;
                clearInterval(timer);
            } else {
                stat.textContent = current;
            }
        }, increment);
    });
}

// User menu dropdown
const userMenu = document.querySelector('.user-menu');
if (userMenu) {
    userMenu.addEventListener('click', (e) => {
        e.stopPropagation();
        const dropdown = userMenu.querySelector('.user-dropdown');
        if (dropdown) {
            dropdown.style.display = dropdown.style.display === 'flex' ? 'none' : 'flex';
        }
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        const dropdown = userMenu.querySelector('.user-dropdown');
        if (dropdown) {
            dropdown.style.display = 'none';
        }
    });
}

// Fetch and display user info
async function loadUserInfo() {
    try {
        const response = await fetch('/api/user');
        if (response.ok) {
            const user = await response.json();
            console.log('User:', user);
        }
    } catch (error) {
        console.error('Error loading user info:', error);
    }
}

// Load user info on dashboard load
loadUserInfo();
