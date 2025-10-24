// Team Collaboration System
class CollaborationSystem {
    constructor() {
        this.users = [];
        this.comments = [];
        this.tasks = [];
        this.notifications = [];
        this.init();
    }

    init() {
        this.loadTeamMembers();
        this.setupNotificationSystem();
        this.setupTaskManagement();
    }

    loadTeamMembers() {
        // Sample team members - in a real app this would come from API
        this.users = [
            {
                id: 1,
                name: 'Sarah Johnson',
                role: 'HR Manager',
                avatar: 'SJ',
                email: 'sarah@company.com',
                online: true
            },
            {
                id: 2,
                name: 'Mike Chen',
                role: 'Technical Lead',
                avatar: 'MC',
                email: 'mike@company.com',
                online: false
            },
            {
                id: 3,
                name: 'Lisa Rodriguez',
                role: 'Recruiter',
                avatar: 'LR',
                email: 'lisa@company.com',
                online: true
            }
        ];
    }

    setupNotificationSystem() {
        // Create notification center
        this.createNotificationCenter();
        
        // Simulate real-time notifications
        setInterval(() => {
            if (Math.random() > 0.8) { // 20% chance every 30 seconds
                this.simulateNotification();
            }
        }, 30000);
    }

    createNotificationCenter() {
        const notificationBtn = document.createElement('button');
        notificationBtn.className = 'notification-btn';
        notificationBtn.innerHTML = `
            <i class="fas fa-bell"></i>
            <span class="notification-count" id="notification-count">0</span>
        `;
        notificationBtn.onclick = () => this.showNotificationPanel();

        // Add to header
        const headerActions = document.querySelector('.header-actions');
        headerActions.insertBefore(notificationBtn, headerActions.firstChild);

        // Create notification panel
        this.createNotificationPanel();
    }

    createNotificationPanel() {
        const panel = document.createElement('div');
        panel.className = 'notification-panel';
        panel.id = 'notification-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <h3>Notifications</h3>
                <button onclick="collaborationSystem.closeNotificationPanel()" class="btn-icon">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="panel-content">
                <div class="notification-tabs">
                    <button class="tab-btn active" onclick="collaborationSystem.showNotificationTab('all')">All</button>
                    <button class="tab-btn" onclick="collaborationSystem.showNotificationTab('mentions')">Mentions</button>
                    <button class="tab-btn" onclick="collaborationSystem.showNotificationTab('tasks')">Tasks</button>
                </div>
                <div class="notifications-list" id="notifications-list">
                    <div class="empty-state">
                        <i class="fas fa-bell-slash empty-state-icon"></i>
                        <h4>No notifications</h4>
                        <p>You're all caught up!</p>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(panel);
    }

    showNotificationPanel() {
        document.getElementById('notification-panel').classList.add('open');
        this.loadNotifications();
    }

    closeNotificationPanel() {
        document.getElementById('notification-panel').classList.remove('open');
    }

    simulateNotification() {
        const types = ['comment', 'mention', 'task', 'status_update'];
        const type = types[Math.floor(Math.random() * types.length)];
        const user = this.users[Math.floor(Math.random() * this.users.length)];
        
        const notification = {
            id: Date.now(),
            type: type,
            user: user,
            message: this.generateNotificationMessage(type, user),
            timestamp: new Date(),
            read: false,
            applicationId: Math.floor(Math.random() * 10) + 1
        };
        
        this.notifications.unshift(notification);
        this.updateNotificationCount();
        this.showToastNotification(notification);
    }

    generateNotificationMessage(type, user) {
        const messages = {
            comment: `${user.name} added a comment on an application`,
            mention: `${user.name} mentioned you in a comment`,
            task: `${user.name} assigned you a task`,
            status_update: `${user.name} updated an application status`
        };
        return messages[type];
    }

    updateNotificationCount() {
        const unreadCount = this.notifications.filter(n => !n.read).length;
        const countElement = document.getElementById('notification-count');
        if (countElement) {
            countElement.textContent = unreadCount;
            countElement.style.display = unreadCount > 0 ? 'block' : 'none';
        }
    }

    showToastNotification(notification) {
        const toast = document.createElement('div');
        toast.className = 'notification-toast';
        toast.innerHTML = `
            <div class="toast-header">
                <div class="toast-avatar">${notification.user.avatar}</div>
                <div class="toast-content">
                    <div class="toast-title">${notification.message}</div>
                    <div class="toast-time">Just now</div>
                </div>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            toast.remove();
        }, 4000);
        
        // Click to view
        toast.onclick = () => {
            this.markAsRead(notification.id);
            toast.remove();
        };
    }

    setupTaskManagement() {
        this.createTaskSystem();
    }

    createTaskSystem() {
        // Task management will be integrated into the collaboration panel
        // This creates the foundation for assigning tasks to team members
    }

    // Enhanced collaboration features for applications
    showEnhancedCollaboration(applicationId) {
        const content = `
            <div class="collaboration-enhanced">
                <!-- Team Members Section -->
                <div class="team-section">
                    <h4>Team Members</h4>
                    <div class="team-members">
                        ${this.users.map(user => `
                            <div class="team-member ${user.online ? 'online' : 'offline'}">
                                <div class="member-avatar">${user.avatar}</div>
                                <div class="member-info">
                                    <div class="member-name">${user.name}</div>
                                    <div class="member-role">${user.role}</div>
                                </div>
                                <div class="member-status">
                                    <i class="fas fa-circle ${user.online ? 'text-green' : 'text-gray'}"></i>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Comments Section -->
                <div class="comments-section">
                    <h4>Discussion</h4>
                    <div class="comments-list" id="enhanced-comments">
                        ${this.renderComments(applicationId)}
                    </div>
                    
                    <div class="comment-composer">
                        <div class="composer-header">
                            <div class="composer-avatar">${dashboard.currentUser?.full_name?.split(' ').map(n => n[0]).join('') || 'U'}</div>
                            <div class="composer-tools">
                                <button class="tool-btn" onclick="collaborationSystem.mentionUser()" title="Mention user">
                                    <i class="fas fa-at"></i>
                                </button>
                                <button class="tool-btn" onclick="collaborationSystem.addTask()" title="Add task">
                                    <i class="fas fa-tasks"></i>
                                </button>
                                <button class="tool-btn" onclick="collaborationSystem.attachFile()" title="Attach file">
                                    <i class="fas fa-paperclip"></i>
                                </button>
                            </div>
                        </div>
                        <textarea class="comment-input" 
                                placeholder="Add a comment, mention someone with @name, or create a task..."
                                onkeydown="collaborationSystem.handleCommentKeydown(event, ${applicationId})"></textarea>
                        <div class="composer-actions">
                            <button class="btn btn-primary btn-sm" onclick="collaborationSystem.submitComment(${applicationId})">
                                Comment
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Tasks Section -->
                <div class="tasks-section">
                    <h4>Tasks & Action Items</h4>
                    <div class="tasks-list" id="tasks-list-${applicationId}">
                        ${this.renderTasks(applicationId)}
                    </div>
                    
                    <button class="btn btn-outline btn-sm" onclick="collaborationSystem.showCreateTaskModal(${applicationId})">
                        <i class="fas fa-plus"></i>
                        Add Task
                    </button>
                </div>

                <!-- Activity Timeline -->
                <div class="activity-timeline">
                    <h4>Activity Timeline</h4>
                    <div class="timeline-list">
                        ${this.renderActivityTimeline(applicationId)}
                    </div>
                </div>
            </div>
        `;

        // Update the collaboration panel content
        modalManager.collaborationPanel = modalManager.collaborationPanel || modalManager.setupCollaboration();
        document.getElementById('collaboration-content').innerHTML = content;
    }

    renderComments(applicationId) {
        // Sample comments - in real app would come from API
        const sampleComments = [
            {
                id: 1,
                user: this.users[0],
                text: "Great candidate! Technical skills look solid. Let's schedule a technical interview.",
                timestamp: new Date(Date.now() - 3600000), // 1 hour ago
                mentions: []
            },
            {
                id: 2,
                user: this.users[1],
                text: "Agreed! @Sarah Johnson can you handle the scheduling? I'm available Tuesday-Thursday next week.",
                timestamp: new Date(Date.now() - 1800000), // 30 minutes ago
                mentions: ['Sarah Johnson']
            }
        ];

        return sampleComments.map(comment => `
            <div class="comment-item">
                <div class="comment-avatar">${comment.user.avatar}</div>
                <div class="comment-content">
                    <div class="comment-header">
                        <span class="comment-author">${comment.user.name}</span>
                        <span class="comment-time">${this.timeAgo(comment.timestamp)}</span>
                    </div>
                    <div class="comment-text">${this.formatCommentText(comment.text)}</div>
                    <div class="comment-actions">
                        <button class="action-btn" onclick="collaborationSystem.replyToComment(${comment.id})">
                            <i class="fas fa-reply"></i> Reply
                        </button>
                        <button class="action-btn" onclick="collaborationSystem.likeComment(${comment.id})">
                            <i class="fas fa-heart"></i> Like
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    renderTasks(applicationId) {
        // Sample tasks
        const sampleTasks = [
            {
                id: 1,
                title: 'Schedule technical interview',
                assignee: this.users[0],
                creator: this.users[1],
                dueDate: new Date(Date.now() + 86400000), // Tomorrow
                status: 'pending',
                priority: 'high'
            },
            {
                id: 2,
                title: 'Reference check',
                assignee: this.users[2],
                creator: this.users[0],
                dueDate: new Date(Date.now() + 172800000), // 2 days
                status: 'completed',
                priority: 'medium'
            }
        ];

        return sampleTasks.map(task => `
            <div class="task-item ${task.status}">
                <div class="task-checkbox">
                    <input type="checkbox" ${task.status === 'completed' ? 'checked' : ''} 
                           onchange="collaborationSystem.toggleTask(${task.id})">
                </div>
                <div class="task-content">
                    <div class="task-title ${task.status === 'completed' ? 'completed' : ''}">${task.title}</div>
                    <div class="task-meta">
                        <span class="task-assignee">Assigned to ${task.assignee.name}</span>
                        <span class="task-due">Due ${this.formatDate(task.dueDate)}</span>
                        <span class="task-priority priority-${task.priority}">${task.priority}</span>
                    </div>
                </div>
                <div class="task-actions">
                    <button class="action-btn" onclick="collaborationSystem.editTask(${task.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }

    renderActivityTimeline(applicationId) {
        const activities = [
            {
                type: 'status_update',
                user: this.users[0],
                action: 'moved application to Interview stage',
                timestamp: new Date(Date.now() - 7200000) // 2 hours ago
            },
            {
                type: 'comment',
                user: this.users[1],
                action: 'added a comment',
                timestamp: new Date(Date.now() - 3600000) // 1 hour ago
            },
            {
                type: 'task_created',
                user: this.users[1],
                action: 'created task "Schedule technical interview"',
                timestamp: new Date(Date.now() - 1800000) // 30 minutes ago
            }
        ];

        return activities.map(activity => `
            <div class="timeline-item">
                <div class="timeline-marker ${activity.type}">
                    <i class="fas fa-${this.getActivityIcon(activity.type)}"></i>
                </div>
                <div class="timeline-content">
                    <span class="activity-user">${activity.user.name}</span>
                    <span class="activity-action">${activity.action}</span>
                    <div class="activity-time">${this.timeAgo(activity.timestamp)}</div>
                </div>
            </div>
        `).join('');
    }

    formatCommentText(text) {
        // Format mentions
        return text.replace(/@([A-Za-z\s]+)/g, '<span class="mention">@$1</span>');
    }

    getActivityIcon(type) {
        const icons = {
            status_update: 'arrow-right',
            comment: 'comment',
            task_created: 'tasks',
            task_completed: 'check',
            mention: 'at'
        };
        return icons[type] || 'info';
    }

    timeAgo(date) {
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

    formatDate(date) {
        return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric' 
        });
    }

    // Event handlers
    handleCommentKeydown(event, applicationId) {
        if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
            event.preventDefault();
            this.submitComment(applicationId);
        }
    }

    submitComment(applicationId) {
        const textarea = document.querySelector('.comment-input');
        const text = textarea.value.trim();
        
        if (!text) return;

        // Simulate comment submission
        dashboard.showNotification('Comment added successfully', 'success');
        textarea.value = '';
        
        // In real app, would make API call and refresh comments
        setTimeout(() => {
            // Refresh comments list
            document.getElementById('enhanced-comments').innerHTML = this.renderComments(applicationId);
        }, 500);
    }

    mentionUser() {
        const textarea = document.querySelector('.comment-input');
        const usersList = this.users.map(user => user.name).join(', ');
        
        // Simple mention functionality - in a real app this would be a dropdown
        dashboard.showNotification(`Available users to mention: ${usersList}`, 'info');
        
        // Focus textarea and add @ symbol
        textarea.focus();
        textarea.value += '@';
    }

    addTask() {
        dashboard.showNotification('Quick task creation - Feature in development', 'info');
    }

    attachFile() {
        dashboard.showNotification('File attachment - Feature in development', 'info');
    }

    replyToComment(commentId) {
        dashboard.showNotification(`Reply to comment ${commentId} - Feature in development`, 'info');
    }

    likeComment(commentId) {
        dashboard.showNotification('Comment liked!', 'success');
    }

    toggleTask(taskId) {
        dashboard.showNotification(`Task ${taskId} status updated`, 'success');
    }

    editTask(taskId) {
        dashboard.showNotification(`Edit task ${taskId} - Feature in development`, 'info');
    }

    showCreateTaskModal(applicationId) {
        const content = `
            <form onsubmit="collaborationSystem.handleTaskSubmit(event, ${applicationId})" class="modal-form">
                <div class="form-field">
                    <label>Task Title *</label>
                    <input type="text" name="title" required placeholder="What needs to be done?">
                </div>
                
                <div class="form-grid">
                    <div class="form-field">
                        <label>Assign To</label>
                        <select name="assignee_id" required>
                            <option value="">Select team member</option>
                            ${this.users.map(user => `
                                <option value="${user.id}">${user.name} - ${user.role}</option>
                            `).join('')}
                        </select>
                    </div>
                    <div class="form-field">
                        <label>Due Date</label>
                        <input type="date" name="due_date" 
                               min="${new Date().toISOString().split('T')[0]}">
                    </div>
                </div>
                
                <div class="form-field">
                    <label>Priority</label>
                    <select name="priority">
                        <option value="low">Low</option>
                        <option value="medium" selected>Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                
                <div class="form-field">
                    <label>Description</label>
                    <textarea name="description" rows="4" 
                              placeholder="Additional details about this task..."></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-outline" onclick="modalManager.closeModal()">
                        Cancel
                    </button>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-plus"></i>
                        Create Task
                    </button>
                </div>
            </form>
        `;

        modalManager.showModal(content, 'Create Task', 'medium');
    }

    async handleTaskSubmit(event, applicationId) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const taskData = Object.fromEntries(formData.entries());
        
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
        submitBtn.disabled = true;
        
        try {
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            dashboard.showNotification('Task created and assigned successfully!', 'success');
            modalManager.closeModal();
            
            // Refresh tasks list
            document.getElementById(`tasks-list-${applicationId}`).innerHTML = this.renderTasks(applicationId);
        } catch (error) {
            dashboard.showNotification('Failed to create task. Please try again.', 'error');
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    }

    loadNotifications() {
        const notificationsList = document.getElementById('notifications-list');
        
        if (this.notifications.length === 0) {
            notificationsList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-bell-slash empty-state-icon"></i>
                    <h4>No notifications</h4>
                    <p>You're all caught up!</p>
                </div>
            `;
            return;
        }

        notificationsList.innerHTML = this.notifications.map(notification => `
            <div class="notification-item ${notification.read ? 'read' : 'unread'}" 
                 onclick="collaborationSystem.markAsRead(${notification.id})">
                <div class="notification-avatar">${notification.user.avatar}</div>
                <div class="notification-content">
                    <div class="notification-text">${notification.message}</div>
                    <div class="notification-time">${this.timeAgo(notification.timestamp)}</div>
                </div>
                ${!notification.read ? '<div class="unread-indicator"></div>' : ''}
            </div>
        `).join('');
    }

    markAsRead(notificationId) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
            notification.read = true;
            this.updateNotificationCount();
            this.loadNotifications();
        }
    }

    showNotificationTab(tab) {
        // Filter notifications based on tab
        dashboard.showNotification(`Notification filter: ${tab} - Feature in development`, 'info');
    }
}

// Initialize collaboration system
window.collaborationSystem = new CollaborationSystem();