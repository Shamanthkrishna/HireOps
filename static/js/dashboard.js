// Dashboard initialization
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
    loadDashboardStats();
});

function initializeDashboard() {
    // Mobile menu toggle
    setupMobileMenu();
}

function setupMobileMenu() {
    // Create hamburger button if it doesn't exist
    const header = document.querySelector('.dashboard-header');
    if (header && !document.querySelector('.mobile-menu-toggle')) {
        const menuButton = document.createElement('button');
        menuButton.className = 'mobile-menu-toggle';
        menuButton.innerHTML = '<i class="fas fa-bars"></i>';
        menuButton.setAttribute('aria-label', 'Toggle menu');
        
        // Insert before user menu
        const userMenu = header.querySelector('.user-menu');
        header.insertBefore(menuButton, userMenu);
        
        // Toggle sidebar on click
        menuButton.addEventListener('click', () => {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.toggle('mobile-open');
            document.body.classList.toggle('sidebar-open');
        });
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            const sidebar = document.querySelector('.sidebar');
            const menuBtn = document.querySelector('.mobile-menu-toggle');
            if (sidebar.classList.contains('mobile-open') && 
                !sidebar.contains(e.target) && 
                e.target !== menuBtn && 
                !menuBtn.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
                document.body.classList.remove('sidebar-open');
            }
        });
    }
}

async function loadDashboardStats() {
    try {
        const response = await fetch('/api/stats');
        if (response.ok) {
            const stats = await response.json();
            updateDashboardStats(stats);
        } else {
            console.error('Failed to load stats');
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

function updateDashboardStats(stats) {
    // Update stat cards with real data
    const statCards = document.querySelectorAll('.stat-card');
    
    if (statCards[0]) {
        statCards[0].querySelector('.stat-number').textContent = stats.total_jobs || 0;
    }
    if (statCards[1]) {
        statCards[1].querySelector('.stat-number').textContent = stats.active_jobs || 0;
    }
    if (statCards[2]) {
        statCards[2].querySelector('.stat-number').textContent = stats.total_candidates || 0;
    }
    if (statCards[3]) {
        statCards[3].querySelector('.stat-number').textContent = stats.total_applications || 0;
    }
    
    // Animate the numbers
    animateDashboardStats();
}

function showSection(sectionName) {
    // Placeholder function for section switching
    console.log(`Switching to section: ${sectionName}`);
    
    // Show a temporary message
    showPlaceholderMessage(`${sectionName.charAt(0).toUpperCase() + sectionName.slice(1)} section coming in Phase 2`);
}

function showPlaceholderMessage(message) {
    // Use toast notification system
    window.toast.info(message, 3000);
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
