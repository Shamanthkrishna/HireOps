# 📄 Clarification Document (To be confirmed with client before development)

## 1. User Roles, Permissions, and Access Levels

### 1.1 Role Definitions
- **Business Head**: Full admin access - can view/edit all data, manage users, access all reports
- **Business Support Team**: What specific permissions do they need? Same as Business Head or limited?
- **Sales Head**: Can they manage Sales Persons directly or just view their activities?
- **Account Manager (AM)**: Can assign requirements to recruiters, view recruiter performance
- **Sales Person**: Can create requirements, view assigned requirements
- **Recruiter**: Can manage assigned candidates, update statuses

### 1.2 Specific Permission Questions
- Can Sales Persons see candidates assigned to their requirements?
- Can Recruiters see requirements they're not assigned to?
- Should AMs be able to reassign requirements between recruiters?
- Can Business Support Team create/edit users, or just view data?

## 2. Authentication and Login Preferences

### 2.1 Authentication Method
- Simple username/password login with session-based auth? ✓ (as specified)
- Do you need "Remember Me" functionality?
- Password complexity requirements (minimum length, special characters)?
- Password reset functionality needed?

### 2.2 User Management
- Who can create new user accounts? (Business Head only, or also AMs?)
- Self-registration allowed, or admin-only user creation?
- User profile management - can users update their own details?

## 3. Dashboard KPIs and Metrics

### 3.1 Business Head Dashboard
- Total active requirements
- Total candidates in pipeline
- Hiring conversion rates
- Revenue metrics (if budget tracking is needed)
- Team performance metrics

### 3.2 Account Manager Dashboard
- Requirements assigned to their recruiters
- Recruiter performance comparison
- Average time-to-hire for their team
- Candidates by status under their management

### 3.3 Recruiter Dashboard
- Assigned requirements
- Candidates by status
- Personal performance metrics
- Upcoming interviews/deadlines

### 3.4 Sales Dashboard
- Requirements created by them
- Status of their requirements
- Client-wise requirement distribution

**Questions:**
- Which specific metrics are most important for each role?
- Do you need time-based charts (weekly/monthly trends)?
- Should there be target vs actual performance tracking?

## 4. Status Change History Detail

### 4.1 Audit Trail Depth
- What level of detail needed in status history?
  - Just status changes with timestamps?
  - Include notes/comments with each change?
  - Track who made the change?
  - Store old and new values?

### 4.2 Data Retention
- How long should status history be retained?
- Any archiving requirements for old data?
- Should deleted records be soft-deleted (hidden) or hard-deleted?

## 5. Import/Export Needs

### 5.1 Current Data Migration
- Do you have existing Google Sheets data to import?
- What's the format of current data?
- Need a one-time migration script?

### 5.2 Ongoing Import/Export
- Regular CSV export functionality needed?
- Import new requirements/candidates from CSV?
- Export filtered data (by date range, status, etc.)?
- Integration with Google Sheets (sync back and forth)?

## 6. Notifications (Email, Alerts)

### 6.1 Email Notifications
- When candidate status changes?
- When new requirements are assigned?
- Daily/weekly summary reports?
- Deadline reminders?

### 6.2 In-App Notifications
- Real-time notifications within the app?
- Notification history/archive?

### 6.3 SMTP Configuration
- Do you have an SMTP server for sending emails?
- Should notifications be optional (user can enable/disable)?

## 7. File Uploads (Candidate CVs)

### 7.1 File Storage
- Upload candidate CVs/resumes?
- What file types allowed? (PDF, DOC, DOCX)
- File size limits?
- Where to store files? (local filesystem or cloud storage)

### 7.2 Document Management
- Multiple files per candidate?
- Version control for updated CVs?
- File preview functionality?

## 8. Hosting, Scaling, and Backups

### 8.1 Deployment Environment
- Where will this be hosted? (Local server, cloud provider, shared hosting)
- Expected number of concurrent users?
- Database preference: SQLite for simplicity or PostgreSQL for production?

### 8.2 Backup Strategy
- Automated database backups needed?
- How often? (daily, weekly)
- Backup retention period?

### 8.3 Performance Requirements
- Expected data volume (number of requirements, candidates per year)?
- Response time expectations?

## 9. UI Design and Branding Preferences

### 9.1 Design Style
- Modern Bootstrap theme or custom styling?
- Company colors/branding to incorporate?
- Mobile-responsive design needed?

### 9.2 User Experience
- Simple table-based interface or more visual dashboard?
- Preference for single-page or multi-page navigation?
- Any specific UI components preferred (charts, graphs, etc.)?

## 10. Must-Have vs Nice-to-Have Features

### 10.1 Must-Have (Phase 1)
Please prioritize these features:
- [ ] User authentication and role-based access
- [ ] Requirement management (CRUD)
- [ ] Candidate management with status tracking
- [ ] Status change audit trail
- [ ] Basic dashboard with KPIs
- [ ] CSV import/export

### 10.2 Nice-to-Have (Phase 2)
- [ ] Email notifications
- [ ] File upload for CVs
- [ ] Advanced reporting/analytics
- [ ] Google Sheets integration
- [ ] Mobile app
- [ ] API for third-party integrations

## 11. Business Process Clarifications

### 11.1 Requirement Lifecycle
- What are all possible requirement statuses? (Open, Assigned, In Progress, Closed, On Hold?)
- Can requirements be reassigned between AMs or Recruiters?
- When is a requirement considered "closed"?

### 11.2 Candidate Lifecycle
- Complete list of candidate statuses? (Applied, Screened, Submitted, Interview Scheduled, Interviewed, Offered, Hired, Rejected, Withdrawn?)
- Can candidates be associated with multiple requirements?
- What happens when a candidate is hired? (moved to employee management?)

### 11.3 Data Relationships
- Can one candidate apply to multiple requirements?
- Can requirements have multiple hiring needs (quantity > 1)?
- How are contract vs permanent employees differentiated in the system?

---

## Instructions for Client
Please review each section above and provide answers/preferences. Once you've filled in the clarifications, respond with **"Proceed with application"** and I'll begin the development phase.

For any questions you're unsure about, we can implement a basic version first and enhance it later based on usage feedback.
