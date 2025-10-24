# HireOps User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [User Roles & Permissions](#user-roles--permissions)
4. [Features Overview](#features-overview)
5. [Detailed Feature Guide](#detailed-feature-guide)
6. [API Documentation](#api-documentation)
7. [Administration](#administration)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Introduction

HireOps is a comprehensive recruitment tracking system designed to streamline your hiring process. It replaces traditional spreadsheet-based tracking with a modern, web-based platform that provides real-time collaboration, audit trails, and advanced analytics.

### Key Benefits
- **Centralized Management**: All recruitment data in one secure platform
- **Role-Based Access**: Different permissions for HR, managers, and candidates
- **Audit Trail**: Complete history of all actions and status changes
- **Real-Time Updates**: Instant notifications and status synchronization
- **Analytics Dashboard**: Insights into recruitment performance and bottlenecks
- **Mobile Friendly**: Access from any device with responsive design

---

## Getting Started

### System Requirements
- **Browser**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **Internet Connection**: Required for real-time features
- **Screen Resolution**: Minimum 1024x768 (responsive design)

### First Time Setup

#### For Administrators
1. **Access the System**
   - Navigate to your HireOps URL
   - Use default credentials: `admin@hireops.com` / `admin123`
   - **IMPORTANT**: Change password immediately after first login

2. **Initial Configuration**
   - Set up company information
   - Configure email notifications
   - Add user accounts for your team
   - Customize job application fields

#### For Regular Users
1. **Account Access**
   - Receive invitation email from administrator
   - Click activation link and set your password
   - Log in with your credentials

2. **Profile Setup**
   - Complete your profile information
   - Set notification preferences
   - Upload profile picture (optional)

---

## User Roles & Permissions

### Administrator
**Full system access with all permissions:**
- User management (create, edit, delete accounts)
- System configuration and settings
- View all analytics and reports
- Export data and generate reports
- Access audit logs
- Manage integrations

### HR Manager
**Comprehensive recruitment management:**
- Create and manage job postings
- View all applications and candidates
- Schedule and conduct interviews
- Update application statuses
- Access recruitment analytics
- Send notifications to candidates
- Generate recruitment reports

### Hiring Manager
**Department-specific recruitment:**
- View applications for their department
- Participate in interview process
- Provide feedback on candidates
- Approve/reject applications in their area
- View analytics for their positions

### Interviewer
**Interview-focused access:**
- View assigned interviews
- Access candidate profiles for interviews
- Submit interview feedback
- Update interview status
- Calendar integration

### Candidate (Self-Service Portal)
**Application tracking:**
- Submit job applications
- Upload resume and documents
- Track application status
- Receive status notifications
- Schedule interview slots
- View job postings

---

## Features Overview

### 🎯 Job Management
- Create detailed job postings with requirements
- Set application deadlines and status
- Department-wise job organization
- Job posting templates
- Application form customization

### 👥 Candidate Management
- Comprehensive candidate profiles
- Resume parsing and storage
- Skills and experience tracking
- Communication history
- Document management

### 📋 Application Tracking
- Real-time status updates
- Customizable workflow stages
- Bulk actions for efficiency
- Advanced filtering and search
- Application timeline view

### 📅 Interview Scheduling
- Calendar integration (Google, Outlook)
- Automated email invitations
- Interview feedback forms
- Multi-stage interview process
- Conflict detection and resolution

### 📊 Analytics & Reporting
- Recruitment funnel analysis
- Time-to-hire metrics
- Source effectiveness tracking
- Interviewer performance reports
- Custom dashboard widgets

### 🔔 Notifications
- Email notifications for status changes
- Real-time in-app notifications
- Customizable notification preferences
- Automated reminder system
- Mobile push notifications

---

## Detailed Feature Guide

### Job Management

#### Creating a New Job Posting

1. **Navigate to Jobs**
   - Click "Jobs" in the main navigation
   - Click "Create New Job" button

2. **Basic Information**
   ```
   Job Title: Software Developer
   Department: Engineering
   Location: New York, NY / Remote
   Employment Type: Full-time
   ```

3. **Job Details**
   ```
   Description: Detailed job description...
   Requirements: Required skills and experience...
   Salary Range: $80,000 - $120,000
   Benefits: Health, dental, 401k...
   ```

4. **Application Settings**
   ```
   Application Deadline: MM/DD/YYYY
   Required Documents: Resume, Cover Letter
   Custom Questions: Optional screening questions
   Auto-screening Rules: Automatic filtering criteria
   ```

5. **Review and Publish**
   - Preview the job posting
   - Set visibility (Public/Internal)
   - Click "Publish Job"

#### Managing Job Applications

**Viewing Applications:**
- Access through Jobs → [Job Title] → Applications
- Use filters: Status, Date Range, Department
- Sort by: Date Applied, Last Activity, Rating

**Bulk Actions:**
- Select multiple applications
- Update status for all selected
- Send bulk notifications
- Export selected applications

### Candidate Management

#### Adding a New Candidate

1. **Manual Entry**
   - Click "Candidates" → "Add New Candidate"
   - Fill in basic information
   - Upload resume and documents
   - Add notes and tags

2. **Import from Application**
   - Candidates are automatically created from applications
   - Additional information can be added later
   - Multiple applications link to same candidate profile

#### Candidate Profile Features

**Personal Information:**
- Contact details
- Address and location
- Social media profiles
- Emergency contact

**Professional Information:**
- Current position and company
- Work experience history
- Education background
- Skills and certifications

**Application History:**
- All applications submitted
- Interview feedback
- Status change history
- Communication log

**Documents:**
- Resume (multiple versions)
- Cover letters
- Certificates
- Reference letters
- Portfolio items

### Application Workflow

#### Standard Workflow Stages

1. **Applied** - Initial application submission
2. **Screening** - Initial review and filtering
3. **Phone Screen** - Brief phone/video interview
4. **Technical Assessment** - Skills testing
5. **On-site Interview** - In-person/video interview
6. **Final Interview** - Decision-maker interview
7. **Reference Check** - Background verification
8. **Offer** - Job offer extended
9. **Hired** - Offer accepted, onboarding
10. **Rejected** - Application declined

#### Customizing Workflow

**Adding Custom Stages:**
- Go to Settings → Workflow Configuration
- Click "Add Stage"
- Define stage name and description
- Set required actions and permissions
- Configure automatic notifications

**Stage Actions:**
- Move to next stage
- Request additional information
- Schedule interview
- Send notification
- Add internal notes
- Assign to team member

### Interview Management

#### Scheduling Interviews

1. **Create Interview**
   - From application page, click "Schedule Interview"
   - Select interview type and duration
   - Choose interviewer(s)
   - Set date and time

2. **Calendar Integration**
   ```
   Google Calendar: Automatic sync
   Outlook: Two-way integration
   iCal: Download/import support
   Zoom: Video call links
   ```

3. **Interview Confirmation**
   - Automatic email to all participants
   - Calendar invitations sent
   - Interview details and instructions
   - Preparation materials attached

#### Conducting Interviews

**Interview Panel:**
- Access candidate information
- View resume and application
- Previous interview feedback
- Prepared questions
- Real-time note taking

**Feedback Form:**
```
Technical Skills: 1-5 rating
Communication: 1-5 rating
Cultural Fit: 1-5 rating
Overall Recommendation: Hire/No Hire/Maybe
Detailed Comments: Text feedback
Next Steps: Recommendations
```

**Post-Interview:**
- Submit feedback immediately
- Update application status
- Schedule follow-up if needed
- Send thank you email to candidate

### Analytics Dashboard

#### Key Metrics

**Overview Widgets:**
- Total active jobs
- Applications this month
- Interviews scheduled
- Offers extended
- Time to hire average
- Success rate percentage

**Recruitment Funnel:**
```
Applications → 100%
Screening → 70%
Phone Screen → 40%
Technical → 25%
Final Interview → 15%
Offer → 10%
Hired → 8%
```

**Trend Analysis:**
- Applications over time
- Source effectiveness
- Department performance
- Interviewer statistics
- Seasonal patterns

#### Custom Reports

**Creating Reports:**
1. Go to Analytics → Custom Reports
2. Select data sources
3. Choose metrics and dimensions
4. Apply filters
5. Generate and export

**Available Exports:**
- PDF reports
- Excel spreadsheets
- CSV data files
- Scheduled email reports

### Notification Management

#### Email Notifications

**Automatic Triggers:**
- New application received
- Status change updates
- Interview scheduled
- Feedback requested
- Offer extended
- Document uploaded

**Customizable Templates:**
```html
Subject: Interview Scheduled - {{job_title}}

Dear {{candidate_name}},

You have been scheduled for an interview for the position of {{job_title}}.

Interview Details:
Date: {{interview_date}}
Time: {{interview_time}}
Location: {{interview_location}}
Interviewer: {{interviewer_name}}

Please confirm your attendance by replying to this email.

Best regards,
{{company_name}} Recruitment Team
```

#### In-App Notifications

**Real-Time Updates:**
- New messages appear instantly
- Status changes highlighted
- Urgent items marked with priority
- Click to navigate to relevant page

**Notification Preferences:**
- Email frequency settings
- Mobile push preferences
- Specific event subscriptions
- Quiet hours configuration

---

## API Documentation

### Authentication

All API requests require authentication using JWT tokens.

```bash
# Login to get token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@company.com", "password": "password"}'

# Use token in subsequent requests
curl -X GET "http://localhost:8000/api/jobs" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Core Endpoints

#### Jobs API
```bash
# Get all jobs
GET /api/jobs

# Create new job
POST /api/jobs
{
  "title": "Software Developer",
  "department": "Engineering",
  "description": "Job description...",
  "requirements": "Required skills...",
  "location": "New York, NY",
  "salary_min": 80000,
  "salary_max": 120000,
  "employment_type": "full-time",
  "status": "open"
}

# Get job by ID
GET /api/jobs/{job_id}

# Update job
PUT /api/jobs/{job_id}

# Delete job
DELETE /api/jobs/{job_id}
```

#### Applications API
```bash
# Get all applications
GET /api/applications

# Submit new application
POST /api/applications
{
  "job_id": 1,
  "candidate_id": 1,
  "cover_letter": "Cover letter text...",
  "resume_file": "base64_encoded_file"
}

# Update application status
PUT /api/applications/{app_id}/status
{
  "status": "interview",
  "notes": "Moving to interview stage"
}

# Get applications by job
GET /api/applications/job/{job_id}
```

#### Analytics API
```bash
# Dashboard analytics
GET /api/analytics/dashboard

# Job-specific analytics
GET /api/analytics/job/{job_id}

# Recruiter performance
GET /api/analytics/recruiters/performance

# Candidate pipeline
GET /api/analytics/pipeline
```

### Webhooks

Configure webhooks to receive real-time notifications:

```bash
# Register webhook
POST /api/webhooks
{
  "url": "https://your-app.com/webhook",
  "events": ["application.created", "status.changed"],
  "secret": "webhook_secret"
}
```

**Webhook Events:**
- `application.created`
- `application.status_changed`
- `interview.scheduled`
- `interview.completed`
- `job.created`
- `job.status_changed`

---

## Administration

### User Management

#### Adding New Users

1. **Navigate to Admin Panel**
   - Click "Admin" in main navigation
   - Select "User Management"

2. **Create User Account**
   ```
   Email: user@company.com
   First Name: John
   Last Name: Doe
   Role: hr_manager
   Department: Human Resources
   ```

3. **Set Permissions**
   - Choose role from dropdown
   - Custom permissions (if needed)
   - Access level restrictions
   - Feature availability

4. **Send Invitation**
   - Automatic email invitation
   - Temporary password generation
   - Account activation link
   - Login instructions

#### Managing User Roles

**Role Permissions Matrix:**

| Feature | Admin | HR Manager | Hiring Manager | Interviewer |
|---------|-------|------------|----------------|-------------|
| Create Jobs | ✅ | ✅ | Department Only | ❌ |
| View All Applications | ✅ | ✅ | Department Only | Interview Only |
| Schedule Interviews | ✅ | ✅ | ✅ | Own Only |
| Access Analytics | ✅ | ✅ | Limited | ❌ |
| User Management | ✅ | ❌ | ❌ | ❌ |
| System Settings | ✅ | ❌ | ❌ | ❌ |

### System Configuration

#### Email Settings

```bash
# SMTP Configuration
SMTP_HOST=smtp.company.com
SMTP_PORT=587
SMTP_USERNAME=hireops@company.com
SMTP_PASSWORD=secure_password
FROM_EMAIL=noreply@company.com
```

#### Database Maintenance

**Backup Schedule:**
```bash
# Daily backup at 2 AM
0 2 * * * /opt/hireops/scripts/backup.sh

# Weekly full backup
0 1 * * 0 /opt/hireops/scripts/full-backup.sh
```

**Cleanup Tasks:**
- Remove old application files (90 days)
- Archive completed applications (1 year)
- Clean temporary uploads (24 hours)
- Optimize database indexes (weekly)

#### Security Settings

**Password Policy:**
- Minimum 8 characters
- Must contain uppercase, lowercase, number
- Special character required
- Password history (last 5 passwords)
- Reset required every 90 days

**Session Management:**
- JWT token expiry: 30 minutes
- Refresh token: 7 days
- Concurrent sessions: 3 maximum
- Automatic logout: 1 hour inactivity

### Backup and Recovery

#### Automated Backups

**Database Backup:**
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump hireops_db > /backups/db_backup_$DATE.sql
```

**File Backup:**
```bash
#!/bin/bash
tar -czf /backups/files_$DATE.tar.gz /opt/hireops/uploads
```

#### Disaster Recovery

**Recovery Procedure:**
1. Stop application services
2. Restore database from backup
3. Restore uploaded files
4. Restart services
5. Verify data integrity
6. Test critical functions

**Recovery Testing:**
- Monthly backup restoration test
- Verify data completeness
- Test application functionality
- Document any issues found

---

## Troubleshooting

### Common Issues

#### Login Problems

**Issue**: Cannot log in with correct credentials
**Solutions:**
1. Check if account is active
2. Verify password reset if needed
3. Clear browser cache and cookies
4. Try incognito/private mode
5. Contact administrator for account status

**Issue**: Forgot password
**Solutions:**
1. Use "Forgot Password" link on login page
2. Check email (including spam folder)
3. Click reset link within 24 hours
4. Contact admin if email not received

#### Application Submission Issues

**Issue**: File upload fails
**Solutions:**
1. Check file size (max 10MB)
2. Verify file format (PDF, DOC, DOCX)
3. Try different browser
4. Disable browser extensions
5. Check internet connection

**Issue**: Application not saving
**Solutions:**
1. Fill all required fields
2. Check for validation errors
3. Save draft frequently
4. Try submitting in smaller sections

#### Performance Issues

**Issue**: Slow page loading
**Solutions:**
1. Check internet connection speed
2. Clear browser cache
3. Disable unnecessary browser extensions
4. Try different browser
5. Report to IT if issue persists

**Issue**: Search results timeout
**Solutions:**
1. Reduce search criteria
2. Use more specific filters
3. Limit date range
4. Contact administrator if persistent

### Error Messages

#### Common Error Codes

**401 Unauthorized**
- Solution: Log in again or contact admin

**403 Forbidden**
- Solution: Check permissions or request access

**404 Not Found**
- Solution: Verify URL or navigate from menu

**500 Internal Server Error**
- Solution: Refresh page or contact support

#### Getting Help

**In-App Support:**
- Click "Help" button (? icon)
- Submit support ticket
- Live chat (if available)
- FAQ section

**Contact Information:**
- Email: support@hireops.com
- Phone: +1-800-HIREOPS
- Emergency: +1-800-911-HIRE

---

## Best Practices

### For HR Managers

#### Job Posting Optimization
1. **Clear Job Titles**: Use industry-standard titles
2. **Detailed Descriptions**: Include day-to-day responsibilities
3. **Specific Requirements**: List must-have vs. nice-to-have skills
4. **Competitive Salary**: Research market rates
5. **Application Deadline**: Set realistic timeframes

#### Application Management
1. **Quick Response**: Acknowledge applications within 24 hours
2. **Regular Updates**: Keep candidates informed of status
3. **Consistent Process**: Follow same steps for similar roles
4. **Documentation**: Record all interactions and decisions
5. **Feedback Collection**: Gather feedback from interviewers promptly

#### Interview Best Practices
1. **Structured Process**: Use consistent interview format
2. **Prepared Questions**: Develop role-specific question sets
3. **Multiple Perspectives**: Include diverse interview panel
4. **Timely Feedback**: Submit feedback within 24 hours
5. **Candidate Experience**: Provide clear instructions and expectations

### For Hiring Managers

#### Requirement Setting
1. **Realistic Expectations**: Set achievable skill requirements
2. **Priority Ranking**: Distinguish must-haves from preferences
3. **Growth Potential**: Consider candidate development opportunity
4. **Team Fit**: Define cultural and team compatibility factors
5. **Timeline Planning**: Set realistic hiring timeline

#### Candidate Evaluation
1. **Objective Criteria**: Use standardized evaluation rubrics
2. **Bias Awareness**: Implement structured interview techniques
3. **Reference Checks**: Verify key qualifications and experience
4. **Team Input**: Gather feedback from potential teammates
5. **Decision Documentation**: Record reasoning for hiring decisions

### For Candidates

#### Application Strategy
1. **Tailored Applications**: Customize resume and cover letter
2. **Complete Profiles**: Fill all relevant sections thoroughly
3. **Professional Documents**: Use clean, error-free formatting
4. **Follow Instructions**: Adhere to application requirements
5. **Timely Responses**: Reply to communications promptly

#### Interview Preparation
1. **Research Company**: Understand company culture and values
2. **Practice Responses**: Prepare for common questions
3. **Technical Preparation**: Review relevant technical skills
4. **Question Preparation**: Prepare thoughtful questions to ask
5. **Professional Presentation**: Dress appropriately and test technology

### System Optimization

#### Performance Best Practices
1. **Regular Maintenance**: Schedule system updates and optimization
2. **Data Archiving**: Archive old applications to maintain speed
3. **User Training**: Provide comprehensive user training
4. **Workflow Optimization**: Regularly review and improve processes
5. **Feedback Integration**: Act on user feedback for improvements

#### Security Best Practices
1. **Regular Backups**: Maintain automated backup schedule
2. **Access Reviews**: Quarterly review of user access rights
3. **Security Updates**: Keep system and dependencies updated
4. **Audit Logging**: Monitor system access and changes
5. **Incident Response**: Have clear procedure for security incidents

---

## Support and Resources

### Documentation
- **API Reference**: `/docs` endpoint for interactive API documentation
- **Video Tutorials**: Available in the Help section
- **FAQ**: Frequently asked questions and solutions
- **Release Notes**: Updates and new feature announcements

### Training Resources
- **Onboarding Guides**: Step-by-step tutorials for new users
- **Webinar Schedule**: Regular training sessions
- **Best Practices Guide**: Industry recommendations
- **Use Case Examples**: Real-world implementation examples

### Community
- **User Forum**: Community discussion and support
- **Feature Requests**: Submit ideas for new features
- **Bug Reports**: Report issues and track fixes
- **User Groups**: Local meetups and events

### Professional Services
- **Implementation Support**: Assistance with setup and configuration
- **Custom Development**: Tailored features and integrations
- **Training Services**: On-site or virtual training programs
- **Consulting**: Process optimization and best practices

---

*This guide is regularly updated. For the latest version, visit your HireOps installation or check our documentation portal.*

**Version**: 1.0.0  
**Last Updated**: January 2024  
**Support**: support@hireops.com