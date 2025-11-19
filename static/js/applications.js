// Applications Pipeline Management
let currentApplications = [];
let allJobs = [];
let allCandidates = [];

const statusColumns = ['applied', 'screening', 'interview', 'offer', 'hired', 'rejected'];

document.addEventListener('DOMContentLoaded', () => {
    loadAllData();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('createApplicationBtn').addEventListener('click', () => {
        openApplicationModal();
    });

    document.getElementById('applicationForm').addEventListener('submit', handleApplicationSubmit);
    document.getElementById('statusForm').addEventListener('submit', handleStatusUpdate);

    document.getElementById('applicationModal').addEventListener('click', (e) => {
        if (e.target.id === 'applicationModal') {
            closeApplicationModal();
        }
    });

    document.getElementById('statusModal').addEventListener('click', (e) => {
        if (e.target.id === 'statusModal') {
            closeStatusModal();
        }
    });
}

async function loadAllData() {
    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const pipelineView = document.getElementById('pipelineView');

    loadingState.style.display = 'flex';
    pipelineView.style.display = 'none';
    emptyState.style.display = 'none';

    try {
        // Load all data in parallel
        const [applicationsRes, jobsRes, candidatesRes] = await Promise.all([
            fetch('/api/applications'),
            fetch('/api/jobs'),
            fetch('/api/candidates')
        ]);

        if (!applicationsRes.ok || !jobsRes.ok || !candidatesRes.ok) {
            throw new Error('Failed to load data');
        }

        currentApplications = await applicationsRes.json();
        allJobs = await jobsRes.json();
        allCandidates = await candidatesRes.json();

        loadingState.style.display = 'none';

        if (currentApplications.length === 0) {
            emptyState.style.display = 'flex';
        } else {
            pipelineView.style.display = 'flex';
            displayApplications();
        }
    } catch (error) {
        console.error('Error loading data:', error);
        loadingState.style.display = 'none';
        window.toast.error('Failed to load applications');
    }
}

function displayApplications() {
    // Clear all columns
    statusColumns.forEach(status => {
        const container = document.getElementById(`cards-${status}`);
        container.innerHTML = '';
    });

    // Group applications by status
    const grouped = {};
    statusColumns.forEach(status => {
        grouped[status] = currentApplications.filter(app => app.status === status);
    });

    // Display applications in each column
    statusColumns.forEach(status => {
        const container = document.getElementById(`cards-${status}`);
        const count = grouped[status].length;
        
        // Update count badge
        document.getElementById(`count-${status}`).textContent = count;

        if (count === 0) {
            container.innerHTML = `
                <div class="empty-pipeline">
                    <i class="fas fa-inbox"></i>
                    <p>No applications</p>
                </div>
            `;
        } else {
            container.innerHTML = grouped[status].map(app => createApplicationCard(app)).join('');
        }
    });
}

function createApplicationCard(application) {
    const daysAgo = getDaysAgo(application.applied_at);
    
    return `
        <div class="application-card">
            <div class="candidate-name">${escapeHtml(application.candidate.name)}</div>
            <div class="job-title">${escapeHtml(application.job.title)}</div>
            <div class="meta">
                <span><i class="fas fa-clock"></i> ${daysAgo}</span>
                ${application.candidate.experience_years ? 
                    `<span><i class="fas fa-briefcase"></i> ${application.candidate.experience_years}y exp</span>` : ''}
            </div>
            <div class="actions">
                <button class="btn-update" onclick="openStatusModal(${application.id})">
                    <i class="fas fa-arrow-right"></i> Move
                </button>
            </div>
        </div>
    `;
}

async function openApplicationModal() {
    const modal = document.getElementById('applicationModal');
    const jobSelect = document.getElementById('applicationJob');
    const candidateSelect = document.getElementById('applicationCandidate');

    // Populate jobs dropdown
    jobSelect.innerHTML = '<option value="">Select a job...</option>' + 
        allJobs
            .filter(job => job.status === 'active')
            .map(job => `<option value="${job.id}">${escapeHtml(job.title)}</option>`)
            .join('');

    // Populate candidates dropdown
    candidateSelect.innerHTML = '<option value="">Select a candidate...</option>' +
        allCandidates
            .map(candidate => `<option value="${candidate.id}">${escapeHtml(candidate.name)} - ${escapeHtml(candidate.email)}</option>`)
            .join('');

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeApplicationModal() {
    const modal = document.getElementById('applicationModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.getElementById('applicationForm').reset();
}

async function handleApplicationSubmit(e) {
    e.preventDefault();

    const applicationData = {
        job_id: parseInt(document.getElementById('applicationJob').value),
        candidate_id: parseInt(document.getElementById('applicationCandidate').value),
        notes: document.getElementById('applicationNotes').value || null
    };

    try {
        const response = await fetch('/api/applications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(applicationData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create application');
        }

        window.toast.success('Application created successfully!');
        closeApplicationModal();
        loadAllData();
    } catch (error) {
        console.error('Error creating application:', error);
        window.toast.error(error.message || 'Failed to create application');
    }
}

function openStatusModal(applicationId) {
    const application = currentApplications.find(app => app.id === applicationId);
    if (!application) return;

    const modal = document.getElementById('statusModal');
    
    document.getElementById('statusApplicationId').value = applicationId;
    document.getElementById('statusCandidateName').textContent = application.candidate.name;
    document.getElementById('statusJobTitle').textContent = application.job.title;
    document.getElementById('newStatus').value = application.status;
    document.getElementById('statusNotes').value = '';

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeStatusModal() {
    const modal = document.getElementById('statusModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    document.getElementById('statusForm').reset();
}

async function handleStatusUpdate(e) {
    e.preventDefault();

    const applicationId = parseInt(document.getElementById('statusApplicationId').value);
    const updateData = {
        status: document.getElementById('newStatus').value,
        notes: document.getElementById('statusNotes').value || null
    };

    try {
        const response = await fetch(`/api/applications/${applicationId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updateData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to update status');
        }

        window.toast.success('Status updated successfully!');
        closeStatusModal();
        loadAllData();
    } catch (error) {
        console.error('Error updating status:', error);
        window.toast.error(error.message || 'Failed to update status');
    }
}

// Utility functions
function getDaysAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    return `${Math.floor(diffDays / 30)} months ago`;
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
