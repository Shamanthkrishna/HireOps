// Toast Notification System
class ToastManager {
    constructor() {
        this.container = this.createContainer();
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(container);
        return container;
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };

        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };

        toast.innerHTML = `
            <i class="fas ${icons[type]}"></i>
            <span>${message}</span>
        `;

        toast.style.cssText = `
            background: var(--white);
            color: var(--gray-800);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            min-width: 300px;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
            border-left: 4px solid ${colors[type]};
            cursor: pointer;
        `;

        toast.querySelector('i').style.color = colors[type];
        toast.querySelector('i').style.fontSize = '1.25rem';

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
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(400px);
                    opacity: 0;
                }
            }
        `;
        if (!document.getElementById('toast-animations')) {
            style.id = 'toast-animations';
            document.head.appendChild(style);
        }

        this.container.appendChild(toast);

        // Click to dismiss
        toast.addEventListener('click', () => {
            this.dismiss(toast);
        });

        // Auto dismiss
        if (duration > 0) {
            setTimeout(() => {
                this.dismiss(toast);
            }, duration);
        }

        return toast;
    }

    dismiss(toast) {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    success(message, duration) {
        return this.show(message, 'success', duration);
    }

    error(message, duration) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration) {
        return this.show(message, 'info', duration);
    }
}

// Initialize toast manager
window.toast = new ToastManager();

// Show welcome toast on page load (only once per session)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!sessionStorage.getItem('welcomeShown')) {
            setTimeout(() => {
                window.toast.info('Welcome to HireOps! 👋');
                sessionStorage.setItem('welcomeShown', 'true');
            }, 500);
        }
    });
} else {
    if (!sessionStorage.getItem('welcomeShown')) {
        setTimeout(() => {
            window.toast.info('Welcome to HireOps! 👋');
            sessionStorage.setItem('welcomeShown', 'true');
        }, 500);
    }
}
