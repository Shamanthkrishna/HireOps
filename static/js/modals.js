// Modal Management System
class ModalManager {
    constructor() {
        this.currentModal = null;
        this.init();
    }

    init() {
        // Create modal container if it doesn't exist
        if (!document.getElementById('modal-container')) {
            const container = document.createElement('div');
            container.id = 'modal-container';
            document.body.appendChild(container);
        }

        // Close modal on escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.currentModal) {
                this.closeModal();
            }
        });
    }

    showModal(content, title, size = 'medium') {
        const modalContainer = document.getElementById('modal-container');
        
        const modal = document.createElement('div');
        modal.className = `modal-overlay ${size}`;
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-header">
                    <h3 class="modal-title">${title}</h3>
                    <button class="modal-close" onclick="modalManager.closeModal()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="modal-content">
                    ${content}
                </div>
            </div>
        `;

        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });

        modalContainer.appendChild(modal);
        this.currentModal = modal;
        
        // Animate in
        setTimeout(() => {
            modal.classList.add('show');
        }, 10);

        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        if (!this.currentModal) return;

        this.currentModal.classList.remove('show');
        
        setTimeout(() => {
            if (this.currentModal) {
                this.currentModal.remove();
                this.currentModal = null;
            }
        }, 300);

        // Restore body scroll
        document.body.style.overflow = '';
    }

    // Job Creation Modal
    showCreateJobModal() {
        const content = `
            <form onsubmit="modalManager.handleJobSubmit(event)" class="modal-form">
                <div class="form-grid">
                    <div class="form-field">
                        <label>Job Title *</label>
                        <input type="text" name="title" required placeholder="e.g. Senior Software Engineer">
                    </div>
                    <div class="form-field">
                        <label>Department</label>
                        <select name="department">
                            <option value="">Select Department</option>
                            <option value="engineering">Engineering</option>
                            <option value="marketing">Marketing</option>
                            <option value="sales">Sales</option>
                            <option value="hr">Human Resources</option>
                            <option value="finance">Finance</option>
                            <option value="operations">Operations</option>
                        </select>
                    </div>
                    <div class="form-field">
                        <label>Location</label>
                        <input type="text" name="location" placeholder="e.g. New York, NY or Remote">
                    </div>
                    <div class="form-field">
                        <label>Employment Type</label>
                        <select name="employment_type">
                            <option value="full_time">Full Time</option>
                            <option value="part_time">Part Time</option>
                            <option value="contract">Contract</option>
                            <option value="internship">Internship</option>
                        </select>
                    </div>
                    <div class="form-field">
                        <label>Experience Level</label>
                        <select name="experience_level">
                            <option value="entry">Entry Level</option>
                            <option value="mid">Mid Level</option>
                            <option value="senior">Senior Level</option>
                            <option value="lead">Lead/Principal</option>
                            <option value="executive">Executive</option>
                        </select>
                    </div>
                    <div class="form-field">
                        <label>Salary Range</label>
                        <input type="text" name="salary_range" placeholder="e.g. $80,000 - $120,000">
                    </div>
                </div>
                
                <div class="form-field">
                    <label>Job Description *</label>
                    <textarea name="description" rows="6" required 
                              placeholder="Describe the role, responsibilities, and what you're looking for..."></textarea>
                </div>
                
                <div class="form-field">
                    <label>Requirements</label>
                    <textarea name="requirements" rows="4" 
                              placeholder="List the required skills, experience, and qualifications..."></textarea>
                </div>
                
                <div class="form-field">
                    <label>Benefits</label>
                    <textarea name="benefits" rows="3" 
                              placeholder="Health insurance, 401k, remote work, etc..."></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-outline" onclick="modalManager.closeModal()">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i>
                        Create Job
                    </button>
                </div>
            </form>
        `;

        this.showModal(content, 'Create New Job', 'large');
    }

    // Candidate Creation Modal
    showCreateCandidateModal() {
        const content = `
            <form onsubmit="modalManager.handleCandidateSubmit(event)" class="modal-form">
                <div class="form-grid">
                    <div class="form-field">
                        <label>First Name *</label>
                        <input type="text" name="first_name" required placeholder="John">
                    </div>
                    <div class="form-field">
                        <label>Last Name *</label>
                        <input type="text" name="last_name" required placeholder="Doe">
                    </div>
                    <div class="form-field">
                        <label>Email *</label>
                        <input type="email" name="email" required placeholder="john.doe@example.com">
                    </div>
                    <div class="form-field">
                        <label>Phone</label>
                        <input type="tel" name="phone" placeholder="+1 (555) 123-4567">
                    </div>
                    <div class="form-field">
                        <label>Location</label>
                        <input type="text" name="location" placeholder="New York, NY">
                    </div>
                    <div class="form-field">
                        <label>Years of Experience</label>
                        <select name="experience_years">
                            <option value="">Select Experience</option>
                            <option value="0">0-1 years</option>
                            <option value="1">1-2 years</option>
                            <option value="3">3-5 years</option>
                            <option value="5">5-8 years</option>
                            <option value="8">8-12 years</option>
                            <option value="12">12+ years</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-field">
                    <label>Current Position</label>
                    <input type="text" name="current_position" placeholder="e.g. Software Engineer at Google">
                </div>
                
                <div class="form-field">
                    <label>Skills</label>
                    <textarea name="skills" rows="3" 
                              placeholder="JavaScript, React, Node.js, Python, etc..."></textarea>
                </div>
                
                <div class="form-field">
                    <label>LinkedIn Profile</label>
                    <input type="url" name="linkedin_url" placeholder="https://linkedin.com/in/johndoe">
                </div>
                
                <div class="form-field">
                    <label>Resume/Portfolio URL</label>
                    <input type="url" name="resume_url" placeholder="https://example.com/resume.pdf">
                </div>
                
                <div class="form-field">
                    <label>Notes</label>
                    <textarea name="notes" rows="4" 
                              placeholder="Additional notes about this candidate..."></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-outline" onclick="modalManager.closeModal()">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-user-plus"></i>
                        Add Candidate
                    </button>
                </div>
            </form>
        `;

        this.showModal(content, 'Add New Candidate', 'large');
    }

    // Interview Scheduling Modal
    showScheduleInterviewModal(applicationId) {
        const content = `
            <form onsubmit="modalManager.handleInterviewSubmit(event, ${applicationId})" class="modal-form">
                <div class="form-grid">
                    <div class="form-field">
                        <label>Interview Type *</label>
                        <select name="interview_type" required>
                            <option value="">Select Type</option>
                            <option value="phone">Phone Screening</option>
                            <option value="video">Video Interview</option>
                            <option value="onsite">On-site Interview</option>
                            <option value="technical">Technical Assessment</option>
                            <option value="final">Final Round</option>
                        </select>
                    </div>
                    <div class="form-field">
                        <label>Duration</label>
                        <select name="duration">
                            <option value="30">30 minutes</option>
                            <option value="45">45 minutes</option>
                            <option value="60" selected>1 hour</option>
                            <option value="90">1.5 hours</option>
                            <option value="120">2 hours</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-grid">
                    <div class="form-field">
                        <label>Date *</label>
                        <input type="date" name="interview_date" required 
                               min="${new Date().toISOString().split('T')[0]}">
                    </div>
                    <div class="form-field">
                        <label>Time *</label>
                        <input type="time" name="interview_time" required>
                    </div>
                </div>
                
                <div class="form-field">
                    <label>Interviewer(s)</label>
                    <input type="text" name="interviewers" placeholder="John Smith, Jane Doe">
                </div>
                
                <div class="form-field">
                    <label>Location/Meeting Link</label>
                    <input type="text" name="location" placeholder="Conference Room A or https://zoom.us/j/...">
                </div>
                
                <div class="form-field">
                    <label>Interview Notes</label>
                    <textarea name="notes" rows="4" 
                              placeholder="Topics to cover, questions to ask, etc..."></textarea>
                </div>
                
                <div class="form-field">
                    <label>
                        <input type="checkbox" name="send_calendar_invite" checked>
                        Send calendar invite to candidate
                    </label>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-outline" onclick="modalManager.closeModal()">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-calendar-plus"></i>
                        Schedule Interview
                    </button>
                </div>
            </form>
        `;

        this.showModal(content, 'Schedule Interview', 'medium');
    }

    // Application Details Modal
    showApplicationDetailsModal(applicationId) {
        // For now, show a comprehensive view
        const content = `
            <div class="application-details">
                <div class="details-header">
                    <div class="candidate-summary">
                        <div class="candidate-avatar-large">JD</div>
                        <div class="candidate-info">
                            <h3>John Doe</h3>
                            <p>Applied for Senior Software Engineer</p>
                            <p class="apply-date">Applied 3 days ago</p>
                        </div>
                    </div>
                    <div class="status-actions">
                        <select onchange="modalManager.updateStatus(${applicationId}, this.value)">
                            <option value="applied" selected>Applied</option>
                            <option value="screening">Screening</option>
                            <option value="interview_scheduled">Interview Scheduled</option>
                            <option value="interview_completed">Interview Completed</option>
                            <option value="offer_extended">Offer Extended</option>
                            <option value="hired">Hired</option>
                            <option value="rejected">Rejected</option>
                        </select>
                    </div>
                </div>
                
                <div class="details-tabs">
                    <button class="tab-btn active" onclick="modalManager.showTab('overview')">Overview</button>
                    <button class="tab-btn" onclick="modalManager.showTab('timeline')">Timeline</button>
                    <button class="tab-btn" onclick="modalManager.showTab('documents')">Documents</button>
                    <button class="tab-btn" onclick="modalManager.showTab('notes')">Notes</button>
                </div>
                
                <div id="tab-overview" class="tab-content active">
                    <div class="candidate-details">
                        <h4>Contact Information</h4>
                        <div class="info-grid">
                            <div class="info-item">
                                <label>Email:</label>
                                <span>john.doe@example.com</span>
                            </div>
                            <div class="info-item">
                                <label>Phone:</label>
                                <span>+1 (555) 123-4567</span>
                            </div>
                            <div class="info-item">
                                <label>Location:</label>
                                <span>New York, NY</span>
                            </div>
                            <div class="info-item">
                                <label>Experience:</label>
                                <span>5+ years</span>
                            </div>
                        </div>
                        
                        <h4>Skills & Qualifications</h4>
                        <div class="skills-tags">
                            <span class="skill-tag">JavaScript</span>
                            <span class="skill-tag">React</span>
                            <span class="skill-tag">Node.js</span>
                            <span class="skill-tag">Python</span>
                            <span class="skill-tag">AWS</span>
                        </div>
                    </div>
                </div>
                
                <div id="tab-timeline" class="tab-content">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-marker"></div>
                            <div class="timeline-content">
                                <h5>Application Submitted</h5>
                                <p>Candidate applied for the position</p>
                                <span class="timeline-date">3 days ago</span>
                            </div>
                        </div>
                        <div class="timeline-item">
                            <div class="timeline-marker"></div>
                            <div class="timeline-content">
                                <h5>Application Received</h5>
                                <p>Application automatically moved to review</p>
                                <span class="timeline-date">3 days ago</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="tab-documents" class="tab-content">
                    <div class="documents-list">
                        <div class="document-item">
                            <i class="fas fa-file-pdf"></i>
                            <span>Resume - John_Doe.pdf</span>
                            <button class="btn btn-sm">Download</button>
                        </div>
                        <div class="document-item">
                            <i class="fas fa-link"></i>
                            <span>Portfolio Website</span>
                            <button class="btn btn-sm">Visit</button>
                        </div>
                    </div>
                </div>
                
                <div id="tab-notes" class="tab-content">
                    <div class="notes-section">
                        <textarea placeholder="Add your notes about this candidate..." rows="6"></textarea>
                        <div style="margin-top: 1rem;">
                            <button class="btn btn-primary btn-sm">Save Notes</button>
                        </div>
                    </div>
                </div>
                
                <div class="modal-actions">
                    <button class="btn btn-outline" onclick="modalManager.scheduleInterview(${applicationId})">
                        <i class="fas fa-calendar"></i>
                        Schedule Interview
                    </button>
                    <button class="btn btn-outline" onclick="modalManager.sendEmail(${applicationId})">
                        <i class="fas fa-envelope"></i>
                        Send Email
                    </button>
                    <button class="btn btn-primary" onclick="modalManager.closeModal()">
                        Done
                    </button>
                </div>
            </div>
        `;

        this.showModal(content, 'Application Details', 'large');
    }

    // Form submission handlers
    async handleJobSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const jobData = Object.fromEntries(formData.entries());
        
        // Show loading state
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
        submitBtn.disabled = true;
        
        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            dashboard.showNotification('Job created successfully!', 'success');
            this.closeModal();
            
            // Refresh jobs list if on jobs section
            if (document.getElementById('jobs-section').classList.contains('active')) {
                dashboard.loadSectionContent('jobs');
            }
        } catch (error) {
            dashboard.showNotification('Failed to create job. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    async handleCandidateSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const candidateData = Object.fromEntries(formData.entries());
        
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
        submitBtn.disabled = true;
        
        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            dashboard.showNotification('Candidate added successfully!', 'success');
            this.closeModal();
            
            if (document.getElementById('candidates-section').classList.contains('active')) {
                dashboard.loadSectionContent('candidates');
            }
        } catch (error) {
            dashboard.showNotification('Failed to add candidate. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    async handleInterviewSubmit(event, applicationId) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const interviewData = Object.fromEntries(formData.entries());
        
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scheduling...';
        submitBtn.disabled = true;
        
        try {
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            dashboard.showNotification('Interview scheduled successfully!', 'success');
            this.closeModal();
        } catch (error) {
            dashboard.showNotification('Failed to schedule interview. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    // Tab switching for application details
    showTab(tabName) {
        // Hide all tabs
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Show selected tab
        document.getElementById(`tab-${tabName}`).classList.add('active');
        event.target.classList.add('active');
    }

    // Helper methods
    updateStatus(applicationId, newStatus) {
        dashboard.updateApplicationStatus(applicationId, newStatus);
    }

    scheduleInterview(applicationId) {
        this.closeModal();
        this.showScheduleInterviewModal(applicationId);
    }

    sendEmail(applicationId) {
        dashboard.showNotification(`Email feature for Application #${applicationId} - Feature in development`, 'info');
    }
}

// Initialize modal manager
window.modalManager = new ModalManager();