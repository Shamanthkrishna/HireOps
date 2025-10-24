import os
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", 1025))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@hireops.local")
        self.enabled = os.getenv("ENVIRONMENT", "development") == "production"

    def send_email(self, to_emails: List[str], subject: str, body: str, html_body: Optional[str] = None) -> bool:
        """Send email notification"""
        try:
            if not self.enabled:
                logger.info(f"Email not sent (dev mode): {subject} to {to_emails}")
                return True

            msg = MimeMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject

            # Add plain text part
            text_part = MimeText(body, 'plain')
            msg.attach(text_part)

            # Add HTML part if provided
            if html_body:
                html_part = MimeText(html_body, 'html')
                msg.attach(html_part)

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_username and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                
                server.send_message(msg)
            
            logger.info(f"Email sent successfully: {subject} to {to_emails}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_application_status_update(self, candidate_email: str, candidate_name: str, 
                                     job_title: str, old_status: str, new_status: str) -> bool:
        """Send application status update notification"""
        subject = f"Application Status Update - {job_title}"
        
        body = f"""
Dear {candidate_name},

Your application status for the position "{job_title}" has been updated.

Previous Status: {old_status}
New Status: {new_status}

Thank you for your interest in our company.

Best regards,
HireOps Team
        """
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #4f46e5; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .status-update {{ background: #f8fafc; border-left: 4px solid #4f46e5; padding: 15px; margin: 20px 0; }}
        .footer {{ background: #f1f5f9; padding: 15px; text-align: center; color: #64748b; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Application Status Update</h2>
    </div>
    <div class="content">
        <p>Dear {candidate_name},</p>
        <p>Your application status for the position "<strong>{job_title}</strong>" has been updated.</p>
        
        <div class="status-update">
            <p><strong>Previous Status:</strong> {old_status}</p>
            <p><strong>New Status:</strong> {new_status}</p>
        </div>
        
        <p>Thank you for your interest in our company. We appreciate your patience throughout this process.</p>
        
        <p>Best regards,<br>HireOps Team</p>
    </div>
    <div class="footer">
        <p>This is an automated message from HireOps Recruitment System</p>
    </div>
</body>
</html>
        """
        
        return self.send_email([candidate_email], subject, body, html_body)

    def send_interview_schedule(self, candidate_email: str, candidate_name: str,
                              job_title: str, interview_date: str, interview_type: str,
                              interviewer: str, location: Optional[str] = None) -> bool:
        """Send interview schedule notification"""
        subject = f"Interview Schedule - {job_title}"
        
        location_text = f"\nLocation: {location}" if location else "\nLocation: Virtual/Online"
        
        body = f"""
Dear {candidate_name},

You have been scheduled for an interview for the position "{job_title}".

Interview Details:
Date & Time: {interview_date}
Type: {interview_type}
Interviewer: {interviewer}{location_text}

Please confirm your attendance by replying to this email.

Best regards,
HireOps Team
        """
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #059669; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .interview-details {{ background: #f0fdf4; border: 1px solid #059669; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .footer {{ background: #f1f5f9; padding: 15px; text-align: center; color: #64748b; }}
        .confirm-btn {{ background: #059669; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>Interview Schedule</h2>
    </div>
    <div class="content">
        <p>Dear {candidate_name},</p>
        <p>You have been scheduled for an interview for the position "<strong>{job_title}</strong>".</p>
        
        <div class="interview-details">
            <h3>Interview Details:</h3>
            <p><strong>Date & Time:</strong> {interview_date}</p>
            <p><strong>Type:</strong> {interview_type}</p>
            <p><strong>Interviewer:</strong> {interviewer}</p>
            <p><strong>Location:</strong> {location or "Virtual/Online"}</p>
        </div>
        
        <p>Please confirm your attendance by replying to this email.</p>
        <p>We look forward to meeting with you!</p>
        
        <p>Best regards,<br>HireOps Team</p>
    </div>
    <div class="footer">
        <p>This is an automated message from HireOps Recruitment System</p>
    </div>
</body>
</html>
        """
        
        return self.send_email([candidate_email], subject, body, html_body)

    def send_new_application_alert(self, hr_emails: List[str], candidate_name: str,
                                 job_title: str, application_id: int) -> bool:
        """Send new application alert to HR team"""
        subject = f"New Application Received - {job_title}"
        
        body = f"""
New Application Alert

Candidate: {candidate_name}
Position: {job_title}
Application ID: {application_id}

Please review the application in the HireOps system.

Best regards,
HireOps System
        """
        
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .alert {{ background: #fef2f2; border: 1px solid #dc2626; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .footer {{ background: #f1f5f9; padding: 15px; text-align: center; color: #64748b; }}
    </style>
</head>
<body>
    <div class="header">
        <h2>🚨 New Application Alert</h2>
    </div>
    <div class="content">
        <div class="alert">
            <h3>New Application Received</h3>
            <p><strong>Candidate:</strong> {candidate_name}</p>
            <p><strong>Position:</strong> {job_title}</p>
            <p><strong>Application ID:</strong> #{application_id}</p>
        </div>
        
        <p>A new application has been submitted. Please review it in the HireOps system.</p>
        
        <p>Best regards,<br>HireOps System</p>
    </div>
    <div class="footer">
        <p>This is an automated alert from HireOps Recruitment System</p>
    </div>
</body>
</html>
        """
        
        return self.send_email(hr_emails, subject, body, html_body)

# Create global email service instance
email_service = EmailService()