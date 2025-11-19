// Jobs Management
let currentJobs = [];
let currentJobId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadJobs();
    setupEventListeners();
});

function setupEventListeners() {
    // Create job button
    document.getElementById('createJobBtn').addEventListener('click', () => {
        openJobModal();
    });

    // Form submission
    document.getElementById('jobForm').addEventListener('submit', handleJobSubmit);

    // Search and filters
    document.getElementById('searchInput').addEventListener('input', filterJobs);
    document.getElementById('statusFilter').addEventListener('change', filterJobs);

    // Close modal on background click
    document.getElementById('jobModal').addEventListener('click', (e) => {
        if (e.target.id === 'jobModal') {
            closeJobModal();
        }
    });
}

async function loadJobs() {
    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const tableBody = document.getElementById('jobsTableBody');

    loadingState.style.display = 'flex';
    emptyState.style.display = 'none';

    try {
        const response = await fetch('/api/jobs');
        if (!response.ok) throw new Error('Failed to load jobs');

        currentJobs = await response.json();
        loadingState.style.display = 'none';

        if (currentJobs.length === 0) {
            emptyState.style.display = 'flex';
            tableBody.innerHTML = '';
        } else {
            displayJobs(currentJobs);
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
        loadingState.style.display = 'none';
        window.toast.error('Failed to load jobs');
    }
}

function displayJobs(jobs) {
    const tableBody = document.getElementById('jobsTableBody');
    const emptyState = document.getElementById('emptyState');

    if (jobs.length === 0) {
        tableBody.innerHTML = '';
        emptyState.style.display = 'flex';
        return;
    }

    emptyState.style.display = 'none';
    tableBody.innerHTML = jobs.map(job => `
        <tr>
            <td>
                <strong>${escapeHtml(job.title)}</strong>
                <br>
                <small style="color: var(--gray-600);">${escapeHtml(job.salary_range || 'Salary not specified')}</small>
            </td>
            <td>${escapeHtml(job.location || 'Not specified')}</td>
            <td>${escapeHtml(job.job_type || '-')}</td>
            <td>
                <span class="status-badge ${job.status}">${job.status.replace('_', ' ')}</span>
            </td>
            <td>
                <span style="font-weight: 600; color: var(--primary-color);">${job.application_count || 0}</span>
            </td>
            <td>${formatDate(job.created_at)}</td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn" onclick="viewJob(${job.id})" title="View">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn" onclick="editJob(${job.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" onclick="deleteJob(${job.id}, '${escapeHtml(job.title)}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function filterJobs() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;

    let filtered = currentJobs;

    // Apply search filter
    if (searchTerm) {
        filtered = filtered.filter(job =>
            job.title.toLowerCase().includes(searchTerm) ||
            (job.description && job.description.toLowerCase().includes(searchTerm))
        );
    }

    // Apply status filter
    if (statusFilter) {
        filtered = filtered.filter(job => job.status === statusFilter);
    }

    displayJobs(filtered);
}

function openJobModal(job = null) {
    const modal = document.getElementById('jobModal');
    const modalTitle = document.getElementById('modalTitle');
    const submitBtnText = document.getElementById('submitBtnText');
    const form = document.getElementById('jobForm');

    form.reset();
    currentJobId = null;

    if (job) {
        // Edit mode
        modalTitle.textContent = 'Edit Job Posting';
        submitBtnText.textContent = 'Update Job';
        currentJobId = job.id;

        document.getElementById('jobId').value = job.id;
        document.getElementById('jobTitle').value = job.title;
        document.getElementById('jobLocation').value = job.location || '';
        document.getElementById('jobType').value = job.job_type || '';
        document.getElementById('jobSalary').value = job.salary_range || '';
        document.getElementById('jobStatus').value = job.status;
        document.getElementById('jobDescription').value = job.description;
        document.getElementById('jobRequirements').value = job.requirements || '';
    } else {
        // Create mode
        modalTitle.textContent = 'Create Job Posting';
        submitBtnText.textContent = 'Create Job';
        document.getElementById('jobStatus').value = 'draft';
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeJobModal() {
    const modal = document.getElementById('jobModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    currentJobId = null;
}

async function handleJobSubmit(e) {
    e.preventDefault();

    const jobData = {
        title: document.getElementById('jobTitle').value,
        description: document.getElementById('jobDescription').value,
        requirements: document.getElementById('jobRequirements').value,
        location: document.getElementById('jobLocation').value,
        job_type: document.getElementById('jobType').value,
        salary_range: document.getElementById('jobSalary').value,
        status: document.getElementById('jobStatus').value
    };

    try {
        const url = currentJobId ? `/api/jobs/${currentJobId}` : '/api/jobs';
        const method = currentJobId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jobData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to save job');
        }

        window.toast.success(currentJobId ? 'Job updated successfully!' : 'Job created successfully!');
        closeJobModal();
        loadJobs();
    } catch (error) {
        console.error('Error saving job:', error);
        window.toast.error(error.message || 'Failed to save job');
    }
}

async function viewJob(jobId) {
    const job = currentJobs.find(j => j.id === jobId);
    if (job) {
        // For now, just edit. Later we can add a view-only modal
        editJob(jobId);
    }
}

async function editJob(jobId) {
    try {
        const response = await fetch(`/api/jobs/${jobId}`);
        if (!response.ok) throw new Error('Failed to load job');

        const job = await response.json();
        openJobModal(job);
    } catch (error) {
        console.error('Error loading job:', error);
        window.toast.error('Failed to load job details');
    }
}

async function deleteJob(jobId, jobTitle) {
    if (!confirm(`Are you sure you want to delete "${jobTitle}"? This action cannot be undone.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/jobs/${jobId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete job');

        window.toast.success('Job deleted successfully');
        loadJobs();
    } catch (error) {
        console.error('Error deleting job:', error);
        window.toast.error('Failed to delete job');
    }
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
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
