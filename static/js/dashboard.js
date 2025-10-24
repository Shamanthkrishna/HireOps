// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication
    checkDashboardAuth();
    
    // Initialize dashboard
    initializeDashboard();
    
    // Load initial data
    loadDashboardData();
});

function checkDashboardAuth() {
    const token = localStorage.getItem('hireops_token');
    if (!token) {
        window.location.href = '/';
        return;
    }
    
    // Verify token and load user info
    fetch(`${window.API_BASE}/api/auth/me`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Invalid token');
        }
        return response.json();
    })
    .then(user => {
        document.getElementById('user-name').textContent = user.full_name;
    })
    .catch(error => {
        localStorage.removeItem('hireops_token');
        window.location.href = '/';
    });
}

function initializeDashboard() {
    // Show default section
    showSection('overview');
}

function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Show selected section
    const section = document.getElementById(`${sectionName}-section`);
    if (section) {
        section.classList.add('active');
    }
    
    // Add active class to nav item
    const navItem = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
    if (navItem) {
        navItem.classList.add('active');
    }
    
    // Load section-specific data
    loadSectionData(sectionName);
}

async function loadDashboardData() {
    const token = localStorage.getItem('hireops_token');
    if (!token) return;
    
    const headers = {
        'Authorization': `Bearer ${token}`
    };
    
    try {
        // Load stats
        await Promise.all([
            loadStats(headers),
            loadPipelineData(headers),
            loadRecentActivity(headers)
        ]);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showErrorMessage('Failed to load dashboard data');
    }
}

async function loadStats(headers) {
    try {
        const [jobsRes, candidatesRes, applicationsRes] = await Promise.all([
            fetch(`${window.API_BASE}/api/jobs/?size=1`, { headers }),
            fetch(`${window.API_BASE}/api/candidates/?size=1`, { headers }),
            fetch(`${window.API_BASE}/api/applications/?size=1`, { headers })
        ]);
        
        const jobsData = await jobsRes.json();
        const candidatesData = await candidatesRes.json();
        const applicationsData = await applicationsRes.json();
        
        document.getElementById('total-jobs').textContent = jobsData.total || 0;
        document.getElementById('total-candidates').textContent = candidatesData.total || 0;
        document.getElementById('total-applications').textContent = applicationsData.total || 0;
        
        // Calculate offers (applications with offer status)
        const offersRes = await fetch(`${window.API_BASE}/api/applications/?status=offer_extended&size=1`, { headers });
        const offersData = await offersRes.json();
        document.getElementById('offers-made').textContent = offersData.total || 0;
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadPipelineData(headers) {
    try {
        const statuses = ['applied', 'screening', 'interview_scheduled', 'offer_extended'];
        
        for (const status of statuses) {
            const response = await fetch(`${window.API_BASE}/api/applications/?status=${status}&size=5`, { headers });
            const data = await response.json();
            
            const countId = status === 'interview_scheduled' ? 'interview-count' : `${status.replace('_', '-')}-count`;
            const listId = status === 'interview_scheduled' ? 'interview-list' : `${status.replace('_', '-')}-list`;
            
            // Update count
            document.getElementById(countId).textContent = data.total || 0;
            
            // Update list
            const listElement = document.getElementById(listId);
            if (data.items && data.items.length > 0) {
                listElement.innerHTML = data.items.map(app => `
                    <div class="application-card" onclick="viewApplication(${app.id})">
                        <div class="application-title">${app.candidate?.first_name} ${app.candidate?.last_name}</div>
                        <div class="application-meta">
                            <span>${app.job?.title}</span>
                            <span>${new Date(app.applied_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                `).join('');
            } else {
                listElement.innerHTML = '<div class="no-data">No applications</div>';
            }
        }
    } catch (error) {
        console.error('Error loading pipeline data:', error);
    }
}

async function loadRecentActivity(headers) {
    try {
        const response = await fetch(`${window.API_BASE}/api/applications/?size=10`, { headers });
        const data = await response.json();
        
        const activityList = document.getElementById('recent-activity');
        
        if (data.items && data.items.length > 0) {
            activityList.innerHTML = data.items.map(app => `
                <div class="activity-item">
                    <div class="activity-icon">
                        <i class="fas fa-user-plus"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-text">
                            ${app.candidate?.first_name} ${app.candidate?.last_name} applied for ${app.job?.title}
                        </div>
                        <div class="activity-time">${timeAgo(app.applied_at)}</div>
                    </div>
                </div>
            `).join('');
        } else {
            activityList.innerHTML = '<div class="no-data">No recent activity</div>';
        }
    } catch (error) {
        console.error('Error loading recent activity:', error);
        document.getElementById('recent-activity').innerHTML = '<div class="error">Failed to load activity</div>';
    }
}

async function loadSectionData(sectionName) {
    const token = localStorage.getItem('hireops_token');
    if (!token) return;
    
    const headers = {
        'Authorization': `Bearer ${token}`
    };
    
    switch (sectionName) {
        case 'jobs':
            await loadJobsSection(headers);
            break;
        case 'candidates':
            await loadCandidatesSection(headers);
            break;
        case 'applications':
            await loadApplicationsSection(headers);
            break;
        case 'interviews':
            await loadInterviewsSection(headers);
            break;
        case 'analytics':
            await loadAnalyticsSection(headers);
            break;
    }
}

async function loadJobsSection(headers) {
    const jobsContent = document.querySelector('.jobs-content');
    jobsContent.innerHTML = '<div class="loading">Loading jobs...</div>';
    
    try {
        const response = await fetch(`${window.API_BASE}/api/jobs/?size=20`, { headers });
        const data = await response.json();
        
        if (data.items && data.items.length > 0) {
            jobsContent.innerHTML = `
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Department</th>
                                <th>Location</th>
                                <th>Applications</th>
                                <th>Status</th>
                                <th>Created</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.items.map(job => `
                                <tr>
                                    <td><strong>${job.title}</strong></td>
                                    <td>${job.department || 'N/A'}</td>
                                    <td>${job.location || 'Remote'}</td>
                                    <td>${job.applications_count || 0}</td>
                                    <td><span class="status-badge ${job.is_active ? 'applied' : 'interview'}">${job.is_active ? 'Active' : 'Inactive'}</span></td>
                                    <td>${new Date(job.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <button class="btn btn-sm" onclick="editJob(${job.id})">Edit</button>
                                        <button class="btn btn-sm btn-outline" onclick="viewJobApplications(${job.id})">Applications</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            jobsContent.innerHTML = '<div class="no-data">No jobs found. <button class="btn btn-primary" onclick="showCreateJobModal()">Create your first job</button></div>';
        }
    } catch (error) {
        jobsContent.innerHTML = '<div class="error">Failed to load jobs</div>';
    }
}

async function loadCandidatesSection(headers) {
    const candidatesContent = document.querySelector('.candidates-content');
    candidatesContent.innerHTML = '<div class="loading">Loading candidates...</div>';
    
    try {
        const response = await fetch(`${window.API_BASE}/api/candidates/?size=20`, { headers });
        const data = await response.json();
        
        if (data.items && data.items.length > 0) {
            candidatesContent.innerHTML = `
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Experience</th>
                                <th>Location</th>
                                <th>Applications</th>
                                <th>Added</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.items.map(candidate => `
                                <tr>
                                    <td><strong>${candidate.first_name} ${candidate.last_name}</strong></td>
                                    <td>${candidate.email}</td>
                                    <td>${candidate.experience_years || 0} years</td>
                                    <td>${candidate.location || 'N/A'}</td>
                                    <td>${candidate.applications_count || 0}</td>
                                    <td>${new Date(candidate.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <button class="btn btn-sm" onclick="editCandidate(${candidate.id})">Edit</button>
                                        <button class="btn btn-sm btn-outline" onclick="viewCandidateApplications(${candidate.id})">Applications</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            candidatesContent.innerHTML = '<div class="no-data">No candidates found. <button class="btn btn-primary" onclick="showCreateCandidateModal()">Add your first candidate</button></div>';
        }
    } catch (error) {
        candidatesContent.innerHTML = '<div class="error">Failed to load candidates</div>';
    }
}

async function loadApplicationsSection(headers) {
    const applicationsContent = document.querySelector('.applications-content');
    applicationsContent.innerHTML = '<div class="loading">Loading applications...</div>';
    
    try {
        const response = await fetch(`${window.API_BASE}/api/applications/?size=20`, { headers });
        const data = await response.json();
        
        if (data.items && data.items.length > 0) {
            applicationsContent.innerHTML = `
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Candidate</th>
                                <th>Job</th>
                                <th>Status</th>
                                <th>Source</th>
                                <th>Applied</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.items.map(app => `
                                <tr>
                                    <td><strong>${app.candidate?.first_name} ${app.candidate?.last_name}</strong></td>
                                    <td>${app.job?.title}</td>
                                    <td><span class="status-badge ${app.status}">${app.status.replace('_', ' ')}</span></td>
                                    <td>${app.source || 'Direct'}</td>
                                    <td>${new Date(app.applied_at).toLocaleDateString()}</td>
                                    <td>
                                        <button class="btn btn-sm" onclick="viewApplication(${app.id})">View</button>
                                        <button class="btn btn-sm btn-outline" onclick="updateApplicationStatus(${app.id})">Update Status</button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            `;
        } else {
            applicationsContent.innerHTML = '<div class="no-data">No applications found</div>';
        }
    } catch (error) {
        applicationsContent.innerHTML = '<div class="error">Failed to load applications</div>';
    }
}

async function loadInterviewsSection(headers) {
    const interviewsContent = document.querySelector('.interviews-content');
    interviewsContent.innerHTML = '<div class="coming-soon">Interviews section coming soon!</div>';
}

async function loadAnalyticsSection(headers) {
    const analyticsContent = document.querySelector('.analytics-content');
    analyticsContent.innerHTML = '<div class="coming-soon">Analytics section coming soon!</div>';
}

// Modal functions (placeholders)
function showCreateJobModal() {
    showNotification('Create Job modal will be implemented in the next phase', 'info');
}

function showCreateCandidateModal() {
    showNotification('Create Candidate modal will be implemented in the next phase', 'info');
}

function showScheduleInterviewModal() {
    showNotification('Schedule Interview modal will be implemented in the next phase', 'info');
}

function editJob(jobId) {
    showNotification(`Edit Job ${jobId} - Coming soon!`, 'info');
}

function viewJobApplications(jobId) {
    showNotification(`View Job ${jobId} Applications - Coming soon!`, 'info');
}

function editCandidate(candidateId) {
    showNotification(`Edit Candidate ${candidateId} - Coming soon!`, 'info');
}

function viewCandidateApplications(candidateId) {
    showNotification(`View Candidate ${candidateId} Applications - Coming soon!`, 'info');
}

function viewApplication(applicationId) {
    showNotification(`View Application ${applicationId} - Coming soon!`, 'info');
}

function updateApplicationStatus(applicationId) {
    showNotification(`Update Application ${applicationId} Status - Coming soon!`, 'info');
}

// Utility functions
function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 60) {
        return `${diffMins} minutes ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hours ago`;
    } else {
        return `${diffDays} days ago`;
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'info' ? '#3b82f6' : type === 'success' ? '#10b981' : '#ef4444'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 3000;
            animation: slideIn 0.3s ease-out;
            max-width: 400px;
        ">
            <i class="fas fa-info-circle" style="margin-right: 0.5rem;"></i>
            ${message}
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

function showErrorMessage(message) {
    showNotification(message, 'error');
}

// Filter applications
function filterApplications() {
    const status = document.getElementById('status-filter').value;
    showNotification(`Filter by status: ${status || 'All'} - Coming soon!`, 'info');
}