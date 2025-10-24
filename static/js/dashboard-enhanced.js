// Enhanced Dashboard with Drag-and-Drop Pipeline
class HireOpsDashboard {
    constructor() {
        this.currentUser = null;
        this.applications = [];
        this.draggedElement = null;
        this.collaborationPanel = null;
        this.analytics = {
            timeToHire: [],
            conversionRates: {},
            sourceEffectiveness: {}
        };
        
        this.init();
    }

    async init() {
        await this.checkAuth();
        this.setupDragAndDrop();
        this.setupCollaboration();
        this.setupRealTimeUpdates();
        this.loadDashboardData();
        this.setupMobileOptimizations();
    }

    async checkAuth() {
        const token = localStorage.getItem('hireops_token');
        if (!token) {
            window.location.href = '/';
            return;
        }

        try {
            const apiBase = window.API_BASE || window.location.origin;
            const response = await fetch(`${apiBase}/api/auth/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (!response.ok) throw new Error('Invalid token');
            
            this.currentUser = await response.json();
            document.getElementById('user-name').textContent = this.currentUser.full_name;
        } catch (error) {
            localStorage.removeItem('hireops_token');
            window.location.href = '/';
        }
    }

    setupDragAndDrop() {
        // Enable drag and drop for application cards
        this.setupDropZones();
        this.setupTouchSupport();
    }

    setupDropZones() {
        const columns = ['applied', 'screening', 'interview', 'offer'];
        
        columns.forEach(status => {
            const listId = status === 'interview' ? 'interview-list' : `${status}-list`;
            const dropZone = document.getElementById(listId);
            
            if (!dropZone) return;

            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('drag-over');
            });

            dropZone.addEventListener('dragleave', () => {
                dropZone.classList.remove('drag-over');
            });

            dropZone.addEventListener('drop', async (e) => {
                e.preventDefault();
                dropZone.classList.remove('drag-over');
                
                const applicationId = e.dataTransfer.getData('text/plain');
                await this.updateApplicationStatus(applicationId, status);
            });
        });
    }

    setupTouchSupport() {
        // Touch support for mobile drag and drop
        let touchItem = null;
        let touchOffset = { x: 0, y: 0 };

        document.addEventListener('touchstart', (e) => {
            const card = e.target.closest('.application-card');
            if (!card) return;

            touchItem = card;
            const touch = e.touches[0];
            const rect = card.getBoundingClientRect();
            touchOffset.x = touch.clientX - rect.left;
            touchOffset.y = touch.clientY - rect.top;
            
            card.style.zIndex = '1000';
            card.classList.add('dragging');
        });

        document.addEventListener('touchmove', (e) => {
            if (!touchItem) return;
            e.preventDefault();

            const touch = e.touches[0];
            touchItem.style.position = 'fixed';
            touchItem.style.left = `${touch.clientX - touchOffset.x}px`;
            touchItem.style.top = `${touch.clientY - touchOffset.y}px`;
        });

        document.addEventListener('touchend', async (e) => {
            if (!touchItem) return;

            const touch = e.changedTouches[0];
            const dropTarget = document.elementFromPoint(touch.clientX, touch.clientY);
            const dropZone = dropTarget.closest('.applications-list');
            
            if (dropZone) {
                const newStatus = this.getStatusFromDropZone(dropZone.id);
                const applicationId = touchItem.dataset.applicationId;
                
                if (newStatus && applicationId) {
                    await this.updateApplicationStatus(applicationId, newStatus);
                }
            }

            // Reset drag state
            touchItem.style.position = '';
            touchItem.style.left = '';
            touchItem.style.top = '';
            touchItem.style.zIndex = '';
            touchItem.classList.remove('dragging');
            touchItem = null;
        });
    }

    getStatusFromDropZone(dropZoneId) {
        const statusMap = {
            'applied-list': 'applied',
            'screening-list': 'screening',
            'interview-list': 'interview_scheduled',
            'offer-list': 'offer_extended'
        };
        return statusMap[dropZoneId];
    }

    async updateApplicationStatus(applicationId, newStatus) {
        const token = localStorage.getItem('hireops_token');
        
        try {
            const apiBase = window.API_BASE || window.location.origin;
            const response = await fetch(`${apiBase}/api/applications/${applicationId}/status`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (response.ok) {
                this.showNotification(`Application moved to ${newStatus.replace('_', ' ')}`, 'success');
                await this.refreshPipelineData();
                this.logActivity(`Application status updated to ${newStatus}`, applicationId);
            } else {
                throw new Error('Failed to update status');
            }
        } catch (error) {
            this.showNotification('Failed to update application status', 'error');
        }
    }

    async loadDashboardData() {
        const token = localStorage.getItem('hireops_token');
        const headers = { 'Authorization': `Bearer ${token}` };

        try {
            // Load all data in parallel
            await Promise.all([
                this.loadStats(headers),
                this.loadEnhancedPipelineData(headers),
                this.loadRecentActivity(headers),
                this.loadAnalyticsData(headers)
            ]);
        } catch (error) {
            console.error('Error loading dashboard:', error);
            this.showNotification('Failed to load dashboard data', 'error');
        }
    }

    async loadEnhancedPipelineData(headers) {
        try {
            const apiBase = window.API_BASE || window.location.origin;
            const response = await fetch(`${apiBase}/api/applications/?size=100`, { headers });
            const data = await response.json();
            
            this.applications = data.items || [];
            this.renderPipelineCards();
        } catch (error) {
            console.error('Error loading pipeline data:', error);
        }
    }

    renderPipelineCards() {
        const statusGroups = {
            'applied': [],
            'screening': [],
            'interview_scheduled': [],
            'offer_extended': []
        };

        // Group applications by status
        this.applications.forEach(app => {
            if (statusGroups[app.status]) {
                statusGroups[app.status].push(app);
            }
        });

        // Render cards for each status
        Object.keys(statusGroups).forEach(status => {
            const listId = status === 'interview_scheduled' ? 'interview-list' : 
                          status === 'offer_extended' ? 'offer-list' : `${status}-list`;
            const countId = status === 'interview_scheduled' ? 'interview-count' : 
                           status === 'offer_extended' ? 'offer-count' : `${status}-count`;
            
            const listElement = document.getElementById(listId);
            const countElement = document.getElementById(countId);
            
            if (!listElement || !countElement) return;

            const applications = statusGroups[status];
            countElement.textContent = applications.length;

            if (applications.length === 0) {
                listElement.innerHTML = '<div class="empty-state"><i class="fas fa-inbox empty-state-icon"></i><h3>No applications</h3><p>Drag applications here</p></div>';
                return;
            }

            listElement.innerHTML = applications.map(app => this.createApplicationCard(app)).join('');
        });
    }

    createApplicationCard(application) {
        const initials = `${application.candidate?.first_name?.[0] || ''}${application.candidate?.last_name?.[0] || ''}`;
        const priority = this.calculatePriority(application);
        const timeInStage = this.calculateTimeInStage(application);

        return `
            <div class="application-card" 
                 draggable="true" 
                 data-application-id="${application.id}"
                 ondragstart="dashboard.handleDragStart(event, ${application.id})"
                 onclick="dashboard.viewApplicationDetails(${application.id})">
                <div class="candidate-info">
                    <div class="candidate-avatar">${initials}</div>
                    <div>
                        <div class="candidate-name">${application.candidate?.first_name} ${application.candidate?.last_name}</div>
                        <div class="job-title">${application.job?.title}</div>
                    </div>
                </div>
                <div class="card-meta">
                    <span class="priority-badge priority-${priority.toLowerCase()}">${priority}</span>
                    <span>${timeInStage}</span>
                </div>
                <div class="card-actions" onclick="event.stopPropagation()">
                    <button class="btn-icon" onclick="dashboard.openCollaboration(${application.id})" title="Add Comment">
                        <i class="fas fa-comment"></i>
                    </button>
                    <button class="btn-icon" onclick="dashboard.scheduleInterview(${application.id})" title="Schedule Interview">
                        <i class="fas fa-calendar"></i>
                    </button>
                </div>
            </div>
        `;
    }

    calculatePriority(application) {
        const daysInStage = Math.floor((Date.now() - new Date(application.applied_at)) / (1000 * 60 * 60 * 24));
        
        if (daysInStage > 7) return 'High';
        if (daysInStage > 3) return 'Medium';
        return 'Low';
    }

    calculateTimeInStage(application) {
        const days = Math.floor((Date.now() - new Date(application.applied_at)) / (1000 * 60 * 60 * 24));
        return days === 0 ? 'Today' : `${days}d ago`;
    }

    handleDragStart(event, applicationId) {
        event.dataTransfer.setData('text/plain', applicationId);
        event.target.classList.add('dragging');
    }

    // Collaboration Features
    setupCollaboration() {
        this.collaborationPanel = document.createElement('div');
        this.collaborationPanel.className = 'collaboration-panel';
        this.collaborationPanel.innerHTML = `
            <div class="panel-header">
                <h3>Collaboration</h3>
                <button onclick="dashboard.closeCollaboration()" class="btn-icon">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="panel-content" id="collaboration-content">
                <!-- Dynamic content -->
            </div>
        `;
        document.body.appendChild(this.collaborationPanel);
    }

    async openCollaboration(applicationId) {
        this.collaborationPanel.classList.add('open');
        collaborationSystem.showEnhancedCollaboration(applicationId);
    }

    closeCollaboration() {
        this.collaborationPanel.classList.remove('open');
    }

    async loadCollaborationData(applicationId) {
        const content = document.getElementById('collaboration-content');
        content.innerHTML = `
            <div class="collaboration-header">
                <h4>Application #${applicationId}</h4>
            </div>
            
            <div class="comment-thread">
                <h5>Comments & Notes</h5>
                <div id="comments-list">
                    <!-- Comments will be loaded here -->
                </div>
                
                <form onsubmit="dashboard.addComment(event, ${applicationId})">
                    <textarea class="comment-input" placeholder="Add a comment..." required></textarea>
                    <div style="margin-top: 0.5rem;">
                        <button type="submit" class="btn btn-primary btn-sm">Add Comment</button>
                    </div>
                </form>
            </div>
            
            <div class="collaboration-actions">
                <h5>Quick Actions</h5>
                <button class="btn btn-outline btn-sm" onclick="dashboard.scheduleInterview(${applicationId})">
                    <i class="fas fa-calendar"></i> Schedule Interview
                </button>
                <button class="btn btn-outline btn-sm" onclick="dashboard.sendEmail(${applicationId})">
                    <i class="fas fa-envelope"></i> Send Email
                </button>
                <button class="btn btn-outline btn-sm" onclick="dashboard.assignReviewer(${applicationId})">
                    <i class="fas fa-user-plus"></i> Assign Reviewer
                </button>
            </div>
        `;
    }

    async addComment(event, applicationId) {
        event.preventDefault();
        const textarea = event.target.querySelector('textarea');
        const comment = textarea.value.trim();
        
        if (!comment) return;

        // In a real app, this would save to the backend
        this.showNotification('Comment added successfully', 'success');
        textarea.value = '';
        
        // Simulate adding comment to UI
        const commentsList = document.getElementById('comments-list');
        const commentElement = document.createElement('div');
        commentElement.className = 'comment';
        commentElement.innerHTML = `
            <div class="comment-avatar"></div>
            <div class="comment-content">
                <div class="comment-header">
                    <span class="comment-author">${this.currentUser.full_name}</span>
                    <span class="comment-time">Just now</span>
                </div>
                <div class="comment-text">${comment}</div>
            </div>
        `;
        commentsList.appendChild(commentElement);
    }

    // Analytics Dashboard
    async loadAnalyticsData(headers) {
        // This would typically fetch real analytics data
        this.analytics = {
            timeToHire: [
                { stage: 'Applied to Screening', avgDays: 2.5, trend: 'down' },
                { stage: 'Screening to Interview', avgDays: 4.2, trend: 'up' },
                { stage: 'Interview to Offer', avgDays: 3.1, trend: 'down' },
                { stage: 'Total Time to Hire', avgDays: 9.8, trend: 'down' }
            ],
            conversionRates: {
                'Applied to Screening': 45,
                'Screening to Interview': 62,
                'Interview to Offer': 28,
                'Offer Acceptance': 89
            },
            sourceEffectiveness: {
                'LinkedIn': { applications: 45, hires: 12 },
                'Company Website': { applications: 32, hires: 8 },
                'Referrals': { applications: 18, hires: 9 },
                'Job Boards': { applications: 25, hires: 4 }
            }
        };
    }

    renderAnalytics() {
        const analyticsContent = document.querySelector('.analytics-content');
        
        analyticsContent.innerHTML = `
            <div class="analytics-grid">
                <div class="analytics-card">
                    <h3>Time to Hire Metrics</h3>
                    <div class="metrics-list">
                        ${this.analytics.timeToHire.map(metric => `
                            <div class="metric-row">
                                <span class="metric-label">${metric.stage}</span>
                                <span class="metric-value trend-${metric.trend}">
                                    ${metric.avgDays} days
                                    <i class="fas fa-arrow-${metric.trend === 'up' ? 'up' : 'down'}"></i>
                                </span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="analytics-card">
                    <h3>Conversion Rates</h3>
                    <div class="chart-container">
                        ${this.renderConversionChart()}
                    </div>
                </div>
                
                <div class="analytics-card">
                    <h3>Source Effectiveness</h3>
                    <div class="metrics-list">
                        ${Object.entries(this.analytics.sourceEffectiveness).map(([source, data]) => `
                            <div class="metric-row">
                                <span class="metric-label">${source}</span>
                                <span class="metric-value">
                                    ${Math.round((data.hires / data.applications) * 100)}% 
                                    (${data.hires}/${data.applications})
                                </span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="analytics-card">
                    <h3>Pipeline Health</h3>
                    <div class="chart-container">
                        ${this.renderPipelineChart()}
                    </div>
                </div>
            </div>
        `;
    }

    renderConversionChart() {
        return `
            <div class="simple-bar-chart">
                ${Object.entries(this.analytics.conversionRates).map(([stage, rate]) => `
                    <div class="chart-bar">
                        <div class="bar-label">${stage}</div>
                        <div class="bar-container">
                            <div class="bar-fill" style="width: ${rate}%"></div>
                            <span class="bar-value">${rate}%</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    renderPipelineChart() {
        const stages = ['Applied', 'Screening', 'Interview', 'Offer'];
        const counts = [25, 18, 12, 7]; // Sample data
        
        return `
            <div class="pipeline-funnel">
                ${stages.map((stage, index) => `
                    <div class="funnel-stage">
                        <div class="stage-bar" style="width: ${(counts[index] / counts[0]) * 100}%">
                            <span class="stage-label">${stage}</span>
                            <span class="stage-count">${counts[index]}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Real-time updates
    setupRealTimeUpdates() {
        // Simulate real-time updates
        setInterval(() => {
            if (document.visibilityState === 'visible') {
                this.checkForUpdates();
            }
        }, 30000); // Check every 30 seconds
    }

    async checkForUpdates() {
        // This would typically use WebSockets or Server-Sent Events
        // For now, we'll periodically refresh data
        await this.refreshPipelineData();
    }

    async refreshPipelineData() {
        const token = localStorage.getItem('hireops_token');
        const headers = { 'Authorization': `Bearer ${token}` };
        await this.loadEnhancedPipelineData(headers);
    }

    // Mobile Optimizations
    setupMobileOptimizations() {
        // Detect mobile device
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (isMobile) {
            document.body.classList.add('mobile-device');
            this.setupMobileGestures();
        }
    }

    setupMobileGestures() {
        // Add mobile-specific gesture support
        let startY = 0;
        
        document.addEventListener('touchstart', (e) => {
            startY = e.touches[0].clientY;
        });
        
        document.addEventListener('touchend', (e) => {
            const endY = e.changedTouches[0].clientY;
            const diff = startY - endY;
            
            // Pull to refresh
            if (diff < -100 && window.scrollY === 0) {
                this.refreshDashboard();
            }
        });
    }

    async refreshDashboard() {
        this.showNotification('Refreshing dashboard...', 'info');
        await this.loadDashboardData();
        this.showNotification('Dashboard refreshed', 'success');
    }

    // Utility Methods
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification-toast ${type}`;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 4000);
    }

    logActivity(activity, entityId = null) {
        console.log(`[${new Date().toISOString()}] ${activity}`, entityId);
        // In a real app, this would log to the backend
    }

    // Navigation
    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Remove active class from nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Show selected section
        const section = document.getElementById(`${sectionName}-section`);
        if (section) {
            section.classList.add('active');
        }
        
        // Add active class to nav item
        const navItem = document.querySelector(`[onclick="dashboard.showSection('${sectionName}')"]`);
        if (navItem) {
            navItem.classList.add('active');
        }
        
        // Load section-specific content
        this.loadSectionContent(sectionName);
    }

    async loadSectionContent(sectionName) {
        switch (sectionName) {
            case 'analytics':
                analyticsSystem.renderAnalyticsDashboard();
                break;
            case 'jobs':
                await this.loadJobsWithActions();
                break;
            case 'candidates':
                await this.loadCandidatesWithActions();
                break;
            default:
                break;
        }
    }

    async loadJobsWithActions() {
        // Enhanced jobs loading with CRUD operations
        const jobsContent = document.querySelector('.jobs-content');
        jobsContent.innerHTML = `
            <div class="advanced-filters">
                <div class="filter-group">
                    <label>Department</label>
                    <select onchange="dashboard.filterJobs()">
                        <option value="">All Departments</option>
                        <option value="engineering">Engineering</option>
                        <option value="marketing">Marketing</option>
                        <option value="sales">Sales</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Status</label>
                    <select onchange="dashboard.filterJobs()">
                        <option value="">All Status</option>
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>Search</label>
                    <input type="text" placeholder="Search jobs..." onkeyup="dashboard.searchJobs(this.value)">
                </div>
            </div>
            <div id="jobs-list">
                <div class="loading-spinner"><div class="spinner"></div></div>
            </div>
        `;
        
        // Load actual jobs data
        setTimeout(() => {
            document.getElementById('jobs-list').innerHTML = `
                <div class="no-data">
                    <div class="empty-state">
                        <i class="fas fa-briefcase empty-state-icon"></i>
                        <h3>No jobs created yet</h3>
                        <p>Start by creating your first job posting</p>
                        <button class="btn btn-primary" onclick="dashboard.showCreateJobModal()">
                            <i class="fas fa-plus"></i> Create Job
                        </button>
                    </div>
                </div>
            `;
        }, 1000);
    }

    async loadCandidatesWithActions() {
        // Enhanced candidates loading
        const candidatesContent = document.querySelector('.candidates-content');
        candidatesContent.innerHTML = `
            <div class="no-data">
                <div class="empty-state">
                    <i class="fas fa-users empty-state-icon"></i>
                    <h3>No candidates added yet</h3>
                    <p>Start building your talent pool</p>
                    <button class="btn btn-primary" onclick="dashboard.showCreateCandidateModal()">
                        <i class="fas fa-user-plus"></i> Add Candidate
                    </button>
                </div>
            </div>
        `;
    }

    // Modal integration
    showCreateJobModal() {
        modalManager.showCreateJobModal();
    }

    showCreateCandidateModal() {
        modalManager.showCreateCandidateModal();
    }

    scheduleInterview(applicationId) {
        modalManager.showScheduleInterviewModal(applicationId);
    }

    sendEmail(applicationId) {
        this.showNotification(`Email feature for Application #${applicationId} - Feature in development`, 'info');
    }

    assignReviewer(applicationId) {
        this.showNotification(`Reviewer assignment for Application #${applicationId} - Feature in development`, 'info');
    }

    viewApplicationDetails(applicationId) {
        modalManager.showApplicationDetailsModal(applicationId);
    }

    filterJobs() {
        this.showNotification('Job filtering - Feature in development', 'info');
    }

    searchJobs(query) {
        if (query.length > 2) {
            this.showNotification(`Searching for: ${query} - Feature in development`, 'info');
        }
    }

    // Load basic stats (keeping existing functionality)
    async loadStats(headers) {
        try {
            // Simulate API calls for demo
            document.getElementById('total-jobs').textContent = '0';
            document.getElementById('total-candidates').textContent = '0';
            document.getElementById('total-applications').textContent = '0';
            document.getElementById('offers-made').textContent = '0';
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    async loadRecentActivity(headers) {
        const activityList = document.getElementById('recent-activity');
        activityList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-clock empty-state-icon"></i>
                <h3>No recent activity</h3>
                <p>Activity will appear here as you use the system</p>
            </div>
        `;
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Ensure API_BASE is available
    if (!window.API_BASE) {
        window.API_BASE = window.location.origin;
    }
    window.dashboard = new HireOpsDashboard();
});

// Export for global access
window.HireOpsDashboard = HireOpsDashboard;