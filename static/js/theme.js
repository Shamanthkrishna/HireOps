// Theme Management System
class ThemeManager {
    constructor() {
        this.theme = this.getStoredTheme() || 'light';
        this.init();
    }

    init() {
        // Apply stored theme immediately
        this.applyTheme(this.theme);
        
        // Create and add theme toggle button
        this.createThemeToggle();
        
        // Listen for system theme changes
        this.watchSystemTheme();
    }

    getStoredTheme() {
        return localStorage.getItem('hireops-theme');
    }

    setStoredTheme(theme) {
        localStorage.setItem('hireops-theme', theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        this.theme = theme;
        this.updateToggleIcon();
    }

    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
        this.setStoredTheme(newTheme);
        
        // Add a subtle animation
        document.body.style.transition = 'background-color 0.3s ease';
    }

    createThemeToggle() {
        // Try to find nav-links (landing page) or navbar-right (dashboard)
        let container = document.querySelector('.nav-links');
        
        if (!container) {
            container = document.querySelector('.navbar-right');
        }
        
        if (!container) return;

        const toggleButton = document.createElement('button');
        toggleButton.className = 'theme-toggle';
        toggleButton.setAttribute('aria-label', 'Toggle theme');
        toggleButton.innerHTML = `
            <div class="theme-toggle-slider">
                <i class="fas fa-${this.theme === 'dark' ? 'moon' : 'sun'}"></i>
            </div>
        `;

        toggleButton.addEventListener('click', () => this.toggleTheme());
        
        // Insert before user menu on dashboard, or append to nav-links on landing page
        const userMenu = container.querySelector('.user-menu');
        if (userMenu) {
            container.insertBefore(toggleButton, userMenu);
        } else {
            container.appendChild(toggleButton);
        }
    }

    updateToggleIcon() {
        const icon = document.querySelector('.theme-toggle-slider i');
        if (icon) {
            icon.className = `fas fa-${this.theme === 'dark' ? 'moon' : 'sun'}`;
        }
    }

    watchSystemTheme() {
        const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
        darkModeQuery.addEventListener('change', (e) => {
            // Only auto-switch if user hasn't set a preference
            if (!this.getStoredTheme()) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeManager = new ThemeManager();
    });
} else {
    window.themeManager = new ThemeManager();
}
