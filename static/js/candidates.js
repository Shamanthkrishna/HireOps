// Candidates Management
let currentCandidates = [];
let currentCandidateId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadCandidates();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('createCandidateBtn').addEventListener('click', () => {
        openCandidateModal();
    });

    document.getElementById('candidateForm').addEventListener('submit', handleCandidateSubmit);
    document.getElementById('searchInput').addEventListener('input', filterCandidates);

    document.getElementById('candidateModal').addEventListener('click', (e) => {
        if (e.target.id === 'candidateModal') {
            closeCandidateModal();
        }
    });
}

async function loadCandidates() {
    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const tableBody = document.getElementById('candidatesTableBody');

    loadingState.style.display = 'flex';
    emptyState.style.display = 'none';

    try {
        const response = await fetch('/api/candidates');
        if (!response.ok) throw new Error('Failed to load candidates');

        currentCandidates = await response.json();
        loadingState.style.display = 'none';

        if (currentCandidates.length === 0) {
            emptyState.style.display = 'flex';
            tableBody.innerHTML = '';
        } else {
            displayCandidates(currentCandidates);
        }
    } catch (error) {
        console.error('Error loading candidates:', error);
        loadingState.style.display = 'none';
        window.toast.error('Failed to load candidates');
    }
}

function displayCandidates(candidates) {
    const tableBody = document.getElementById('candidatesTableBody');
    const emptyState = document.getElementById('emptyState');

    if (candidates.length === 0) {
        tableBody.innerHTML = '';
        emptyState.style.display = 'flex';
        return;
    }

    emptyState.style.display = 'none';
    tableBody.innerHTML = candidates.map(candidate => `
        <tr>
            <td>
                <strong>${escapeHtml(candidate.name)}</strong>
                ${candidate.skills ? `<br><small style="color: var(--gray-600);">${escapeHtml(truncate(candidate.skills, 50))}</small>` : ''}
            </td>
            <td>${escapeHtml(candidate.email)}</td>
            <td>${escapeHtml(candidate.phone || '-')}</td>
            <td>${candidate.experience_years ? candidate.experience_years + ' years' : '-'}</td>
            <td>
                ${candidate.current_position ? `<strong>${escapeHtml(candidate.current_position)}</strong>` : '-'}
                ${candidate.current_company ? `<br><small style="color: var(--gray-600);">${escapeHtml(candidate.current_company)}</small>` : ''}
            </td>
            <td>${formatDate(candidate.created_at)}</td>
            <td>
                <div class="action-buttons">
                    ${candidate.linkedin_url ? `
                        <a href="${escapeHtml(candidate.linkedin_url)}" target="_blank" class="action-btn" title="LinkedIn">
                            <i class="fab fa-linkedin"></i>
                        </a>
                    ` : ''}
                    <button class="action-btn" onclick="editCandidate(${candidate.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="action-btn delete" onclick="deleteCandidate(${candidate.id}, '${escapeHtml(candidate.name)}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function filterCandidates() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    if (!searchTerm) {
        displayCandidates(currentCandidates);
        return;
    }

    const filtered = currentCandidates.filter(candidate =>
        candidate.name.toLowerCase().includes(searchTerm) ||
        candidate.email.toLowerCase().includes(searchTerm) ||
        (candidate.skills && candidate.skills.toLowerCase().includes(searchTerm)) ||
        (candidate.current_company && candidate.current_company.toLowerCase().includes(searchTerm)) ||
        (candidate.current_position && candidate.current_position.toLowerCase().includes(searchTerm))
    );

    displayCandidates(filtered);
}

function openCandidateModal(candidate = null) {
    const modal = document.getElementById('candidateModal');
    const modalTitle = document.getElementById('modalTitle');
    const submitBtnText = document.getElementById('submitBtnText');
    const form = document.getElementById('candidateForm');

    form.reset();
    currentCandidateId = null;

    if (candidate) {
        modalTitle.textContent = 'Edit Candidate';
        submitBtnText.textContent = 'Update Candidate';
        currentCandidateId = candidate.id;

        document.getElementById('candidateId').value = candidate.id;
        document.getElementById('candidateName').value = candidate.name;
        document.getElementById('candidateEmail').value = candidate.email;
        document.getElementById('candidatePhone').value = candidate.phone || '';
        document.getElementById('candidateExperience').value = candidate.experience_years || '';
        document.getElementById('candidateCompany').value = candidate.current_company || '';
        document.getElementById('candidatePosition').value = candidate.current_position || '';
        document.getElementById('candidateLinkedIn').value = candidate.linkedin_url || '';
        document.getElementById('candidateSkills').value = candidate.skills || '';
    } else {
        modalTitle.textContent = 'Add Candidate';
        submitBtnText.textContent = 'Add Candidate';
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeCandidateModal() {
    const modal = document.getElementById('candidateModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    currentCandidateId = null;
}

async function handleCandidateSubmit(e) {
    e.preventDefault();

    const candidateData = {
        name: document.getElementById('candidateName').value,
        email: document.getElementById('candidateEmail').value,
        phone: document.getElementById('candidatePhone').value || null,
        experience_years: parseInt(document.getElementById('candidateExperience').value) || null,
        current_company: document.getElementById('candidateCompany').value || null,
        current_position: document.getElementById('candidatePosition').value || null,
        linkedin_url: document.getElementById('candidateLinkedIn').value || null,
        skills: document.getElementById('candidateSkills').value || null
    };

    try {
        const url = currentCandidateId ? `/api/candidates/${currentCandidateId}` : '/api/candidates';
        const method = currentCandidateId ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(candidateData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to save candidate');
        }

        window.toast.success(currentCandidateId ? 'Candidate updated successfully!' : 'Candidate added successfully!');
        closeCandidateModal();
        loadCandidates();
    } catch (error) {
        console.error('Error saving candidate:', error);
        window.toast.error(error.message || 'Failed to save candidate');
    }
}

async function editCandidate(candidateId) {
    try {
        const response = await fetch(`/api/candidates/${candidateId}`);
        if (!response.ok) throw new Error('Failed to load candidate');

        const candidate = await response.json();
        openCandidateModal(candidate);
    } catch (error) {
        console.error('Error loading candidate:', error);
        window.toast.error('Failed to load candidate details');
    }
}

async function deleteCandidate(candidateId, candidateName) {
    if (!confirm(`Are you sure you want to delete "${candidateName}"? This action cannot be undone.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/candidates/${candidateId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete candidate');

        window.toast.success('Candidate deleted successfully');
        loadCandidates();
    } catch (error) {
        console.error('Error deleting candidate:', error);
        window.toast.error('Failed to delete candidate');
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

function truncate(str, length) {
    if (!str || str.length <= length) return str;
    return str.substring(0, length) + '...';
}
