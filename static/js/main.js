// Main JavaScript for HireOps Frontend
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeNavigation();
    initializeTabs();
    initializeAnimations();
    initializeAuth();
});

// Navigation functionality
function initializeNavigation() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Smooth scrolling for navigation links
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
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    });
}

// Tab functionality
function initializeTabs() {
    // Set default active tab
    showTab('overview');
}

function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab content
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Animation and interaction effects
function initializeAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease-out';
        observer.observe(card);
    });

    // Add hover effects to demo items
    document.querySelectorAll('.demo-item').forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px)';
            this.style.background = '#f8fafc';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
            this.style.background = 'transparent';
        });
    });

    // Animate stats counter
    animateCounters();
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number, .demo-number, .card-number, .stage-count');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/[^\d]/g, ''));
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                counter.textContent = counter.textContent.replace(/\d+/, target);
                clearInterval(timer);
            } else {
                counter.textContent = counter.textContent.replace(/\d+/, Math.floor(current));
            }
        }, 30);
    });
}

// Authentication functionality
function initializeAuth() {
    // API base URL - Set both window and global variable
    window.API_BASE = 'http://127.0.0.1:8000';
    
    // Debug log to confirm API base is set
    console.log('API_BASE set to:', window.API_BASE);
    
    // Check if user is already logged in
    checkAuthStatus();
}

// Helper function to get API base URL
function getApiBase() {
    return window.API_BASE || 'http://127.0.0.1:8000';
}

function checkAuthStatus() {
    const token = localStorage.getItem('hireops_token');
    if (token) {
        // Verify token with API
        fetch(`${getApiBase()}/api/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Invalid token');
        })
        .then(user => {
            updateNavForLoggedInUser(user);
        })
        .catch(error => {
            localStorage.removeItem('hireops_token');
        });
    }
}

function updateNavForLoggedInUser(user) {
    const navAuth = document.querySelector('.nav-auth');
    navAuth.innerHTML = `
        <span class="user-welcome">Welcome, ${user.full_name}</span>
        <button class="btn btn-secondary" onclick="showDashboard()">Dashboard</button>
        <button class="btn btn-outline" onclick="logout()">Logout</button>
    `;
}

// Modal functions
function showModal() {
    document.getElementById('auth-modal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('auth-modal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function showLogin() {
    const authContainer = document.getElementById('auth-container');
    authContainer.innerHTML = `
        <div class="auth-form">
            <h2>Sign In to HireOps</h2>
            <p>Enter your credentials to access your dashboard</p>
            <form id="login-form" onsubmit="handleLogin(event)">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required 
                           placeholder="Enter your username">
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required 
                           placeholder="Enter your password">
                </div>
                <button type="submit" class="btn btn-primary btn-large" style="width: 100%;">
                    <i class="fas fa-sign-in-alt"></i>
                    Sign In
                </button>
            </form>
            <div class="auth-switch">
                <p>Don't have an account? <a href="#" onclick="showRegister()">Sign up</a></p>
            </div>
            <div id="login-error" class="error-message" style="display: none;"></div>
        </div>
    `;
    showModal();
}

function showRegister() {
    const authContainer = document.getElementById('auth-container');
    authContainer.innerHTML = `
        <div class="auth-form">
            <h2>Join HireOps</h2>
            <p>Create your account to get started</p>
            <form id="register-form" onsubmit="handleRegister(event)">
                <div class="form-group">
                    <label for="reg-username">Username</label>
                    <input type="text" id="reg-username" name="username" required 
                           placeholder="Choose a username">
                </div>
                <div class="form-group">
                    <label for="reg-email">Email</label>
                    <input type="email" id="reg-email" name="email" required 
                           placeholder="Enter your email">
                </div>
                <div class="form-group">
                    <label for="reg-fullname">Full Name</label>
                    <input type="text" id="reg-fullname" name="full_name" required 
                           placeholder="Enter your full name">
                </div>
                <div class="form-group">
                    <label for="reg-role">Role</label>
                    <select id="reg-role" name="role" required>
                        <option value="">Select your role</option>
                        <option value="recruiter">Recruiter</option>
                        <option value="hiring_manager">Hiring Manager</option>
                        <option value="interviewer">Interviewer</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="reg-password">Password</label>
                    <input type="password" id="reg-password" name="password" required 
                           placeholder="Choose a strong password" minlength="8">
                </div>
                <button type="submit" class="btn btn-primary btn-large" style="width: 100%;">
                    <i class="fas fa-user-plus"></i>
                    Create Account
                </button>
            </form>
            <div class="auth-switch">
                <p>Already have an account? <a href="#" onclick="showLogin()">Sign in</a></p>
            </div>
            <div id="register-error" class="error-message" style="display: none;"></div>
        </div>
    `;
    showModal();
}

function showDemo() {
    // Scroll to dashboard section
    document.getElementById('dashboard').scrollIntoView({
        behavior: 'smooth'
    });
    
    // Highlight the demo section
    const dashboardSection = document.getElementById('dashboard');
    dashboardSection.style.background = 'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)';
    setTimeout(() => {
        dashboardSection.style.background = '#f8fafc';
    }, 3000);
}

function showDashboard() {
    // Redirect to dashboard (will be implemented)
    window.location.href = '/dashboard';
}

// Auth handlers
async function handleLogin(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const loginData = new URLSearchParams();
    loginData.append('username', formData.get('username'));
    loginData.append('password', formData.get('password'));
    
    const errorDiv = document.getElementById('login-error');
    
    // Debug logging
    console.log('Login attempt:', formData.get('username'));
    console.log('API URL:', `${getApiBase()}/api/auth/login`);
    
    try {
        // Convert form data to JSON
        const loginJson = {
            username: formData.get('username'),
            password: formData.get('password')
        };
        
        const response = await fetch(`${getApiBase()}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(loginJson)
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('hireops_token', data.access_token);
            
            // Get user info
            const userResponse = await fetch(`${getApiBase()}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${data.access_token}`
                }
            });
            
            if (userResponse.ok) {
                const user = await userResponse.json();
                updateNavForLoggedInUser(user);
                closeModal();
                showSuccessMessage('Welcome back! You are now signed in.');
            }
        } else {
            try {
                const error = await response.json();
                showError(errorDiv, error.detail || `Login failed (Status: ${response.status})`);
            } catch (e) {
                showError(errorDiv, `Login failed with status: ${response.status}`);
            }
        }
    } catch (error) {
        console.error('Login error:', error);
        showError(errorDiv, `Connection error: ${error.message}`);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const registerData = {
        username: formData.get('username'),
        email: formData.get('email'),
        full_name: formData.get('full_name'),
        role: formData.get('role'),
        password: formData.get('password')
    };
    
    const errorDiv = document.getElementById('register-error');
    
    // Debug logging
    console.log('Registration attempt:', registerData.username);
    console.log('API URL:', `${getApiBase()}/api/auth/register`);
    
    try {
        const response = await fetch(`${getApiBase()}/api/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registerData)
        });
        
        if (response.ok) {
            showSuccessMessage('Account created successfully! Please sign in.');
            showLogin();
        } else {
            try {
                const error = await response.json();
                showError(errorDiv, error.detail || `Registration failed (Status: ${response.status})`);
            } catch (e) {
                showError(errorDiv, `Registration failed with status: ${response.status}`);
            }
        }
    } catch (error) {
        console.error('Registration error:', error);
        showError(errorDiv, `Connection error: ${error.message}`);
    }
}

function logout() {
    localStorage.removeItem('hireops_token');
    const navAuth = document.querySelector('.nav-auth');
    navAuth.innerHTML = `
        <button class="btn btn-secondary" onclick="showLogin()">Login</button>
        <button class="btn btn-primary" onclick="showRegister()">Get Started</button>
    `;
    showSuccessMessage('You have been signed out.');
}

// Utility functions
function showError(element, message) {
    element.textContent = message;
    element.style.display = 'block';
    element.style.color = '#ef4444';
    element.style.padding = '0.75rem';
    element.style.background = '#fef2f2';
    element.style.border = '1px solid #fecaca';
    element.style.borderRadius = '0.5rem';
    element.style.marginTop = '1rem';
}

function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 3000;
            animation: slideIn 0.3s ease-out;
        ">
            <i class="fas fa-check-circle" style="margin-right: 0.5rem;"></i>
            ${message}
        </div>
    `;
    
    document.body.appendChild(successDiv);
    
    setTimeout(() => {
        successDiv.remove();
    }, 4000);
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('auth-modal');
    if (event.target === modal) {
        closeModal();
    }
});

// Add CSS for auth forms
const authStyles = `
    .auth-form {
        max-width: 400px;
        margin: 0 auto;
    }
    
    .auth-form h2 {
        text-align: center;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .auth-form p {
        text-align: center;
        margin-bottom: 2rem;
        color: var(--text-secondary);
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-group label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .form-group input,
    .form-group select {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        font-size: 1rem;
        transition: var(--transition);
    }
    
    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    .auth-switch {
        text-align: center;
        margin-top: 1.5rem;
    }
    
    .auth-switch a {
        color: var(--primary-color);
        text-decoration: none;
        font-weight: 500;
    }
    
    .auth-switch a:hover {
        text-decoration: underline;
    }
    
    .error-message {
        margin-top: 1rem;
    }
    
    .user-welcome {
        color: var(--text-secondary);
        font-weight: 500;
        margin-right: 1rem;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
`;

// Inject auth styles
const styleSheet = document.createElement('style');
styleSheet.textContent = authStyles;
document.head.appendChild(styleSheet);