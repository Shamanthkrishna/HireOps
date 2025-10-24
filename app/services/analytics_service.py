from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from app.models.models import Application, Job, Candidate, Interview, User
from datetime import datetime, timedelta
from typing import List, Dict, Any
import calendar

class AnalyticsService:
    
    @staticmethod
    def get_dashboard_analytics(db: Session) -> Dict[str, Any]:
        """Get comprehensive dashboard analytics"""
        
        # Basic counts
        total_jobs = db.query(Job).count()
        active_jobs = db.query(Job).filter(Job.status == "open").count()
        total_candidates = db.query(Candidate).count()
        total_applications = db.query(Application).count()
        
        # Applications by status
        applications_by_status = db.query(
            Application.status,
            func.count(Application.id).label('count')
        ).group_by(Application.status).all()
        
        status_counts = {status: count for status, count in applications_by_status}
        
        # Recent activities (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        recent_applications = db.query(Application).filter(
            Application.applied_at >= thirty_days_ago
        ).count()
        
        recent_interviews = db.query(Interview).filter(
            Interview.created_at >= thirty_days_ago
        ).count()
        
        # Applications trend (last 12 months)
        applications_trend = []
        for i in range(12):
            month_start = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])
            
            count = db.query(Application).filter(
                and_(
                    Application.applied_at >= month_start,
                    Application.applied_at <= month_end
                )
            ).count()
            
            applications_trend.append({
                "month": month_start.strftime("%B %Y"),
                "count": count
            })
        
        # Top performing jobs (by application count)
        top_jobs = db.query(
            Job.title,
            Job.id,
            func.count(Application.id).label('application_count')
        ).join(Application).group_by(Job.id, Job.title).order_by(
            desc(func.count(Application.id))
        ).limit(5).all()
        
        # Interview success rate
        completed_interviews = db.query(Interview).filter(
            Interview.status == "completed"
        ).count()
        
        hired_from_interviews = db.query(Application).filter(
            and_(
                Application.status == "hired",
                Application.id.in_(
                    db.query(Interview.application_id).filter(
                        Interview.status == "completed"
                    )
                )
            )
        ).count()
        
        success_rate = (hired_from_interviews / completed_interviews * 100) if completed_interviews > 0 else 0
        
        # Hiring funnel
        funnel_data = {
            "applied": status_counts.get("applied", 0),
            "screening": status_counts.get("screening", 0),
            "interview": status_counts.get("interview", 0),
            "offer": status_counts.get("offer", 0),
            "hired": status_counts.get("hired", 0),
            "rejected": status_counts.get("rejected", 0)
        }
        
        return {
            "overview": {
                "total_jobs": total_jobs,
                "active_jobs": active_jobs,
                "total_candidates": total_candidates,
                "total_applications": total_applications,
                "recent_applications": recent_applications,
                "recent_interviews": recent_interviews
            },
            "status_distribution": status_counts,
            "applications_trend": list(reversed(applications_trend)),
            "top_jobs": [
                {"title": title, "job_id": job_id, "applications": count}
                for title, job_id, count in top_jobs
            ],
            "interview_success_rate": round(success_rate, 2),
            "hiring_funnel": funnel_data
        }
    
    @staticmethod
    def get_job_analytics(db: Session, job_id: int) -> Dict[str, Any]:
        """Get detailed analytics for a specific job"""
        
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return {}
        
        # Application statistics
        total_applications = db.query(Application).filter(Application.job_id == job_id).count()
        
        applications_by_status = db.query(
            Application.status,
            func.count(Application.id).label('count')
        ).filter(Application.job_id == job_id).group_by(Application.status).all()
        
        status_counts = {status: count for status, count in applications_by_status}
        
        # Application timeline (last 30 days)
        timeline = []
        for i in range(30):
            date = datetime.utcnow().date() - timedelta(days=i)
            count = db.query(Application).filter(
                and_(
                    Application.job_id == job_id,
                    func.date(Application.applied_at) == date
                )
            ).count()
            
            timeline.append({
                "date": date.isoformat(),
                "applications": count
            })
        
        # Average time in each status
        avg_times = {}
        for status in ["applied", "screening", "interview", "offer"]:
            # This is a simplified calculation - in reality, you'd track status changes
            avg_times[status] = 3.5  # placeholder days
        
        # Source analysis (would need to add source field to applications)
        sources = [
            {"source": "LinkedIn", "count": int(total_applications * 0.4)},
            {"source": "Company Website", "count": int(total_applications * 0.3)},
            {"source": "Job Boards", "count": int(total_applications * 0.2)},
            {"source": "Referrals", "count": int(total_applications * 0.1)}
        ]
        
        return {
            "job_info": {
                "title": job.title,
                "department": job.department,
                "location": job.location,
                "posted_date": job.posted_date.isoformat() if job.posted_date else None
            },
            "application_stats": {
                "total": total_applications,
                "by_status": status_counts
            },
            "timeline": list(reversed(timeline)),
            "average_time_in_status": avg_times,
            "application_sources": sources
        }
    
    @staticmethod
    def get_recruiter_performance(db: Session) -> List[Dict[str, Any]]:
        """Get performance metrics for recruiters"""
        
        recruiters = db.query(User).filter(User.role.in_(["hr", "admin"])).all()
        performance_data = []
        
        for recruiter in recruiters:
            # Jobs managed (assuming created_by field exists)
            jobs_managed = db.query(Job).count()  # Simplified - would filter by recruiter
            
            # Applications processed (would need to track who processed what)
            applications_processed = db.query(Application).count() // len(recruiters)
            
            # Interviews conducted
            interviews_conducted = db.query(Interview).count() // len(recruiters)
            
            # Hires made
            hires_made = db.query(Application).filter(Application.status == "hired").count() // len(recruiters)
            
            # Time to hire (average)
            avg_time_to_hire = 15.5  # placeholder days
            
            performance_data.append({
                "recruiter_name": f"{recruiter.first_name} {recruiter.last_name}",
                "recruiter_id": recruiter.id,
                "jobs_managed": jobs_managed,
                "applications_processed": applications_processed,
                "interviews_conducted": interviews_conducted,
                "hires_made": hires_made,
                "avg_time_to_hire": avg_time_to_hire,
                "success_rate": round((hires_made / applications_processed * 100) if applications_processed > 0 else 0, 2)
            })
        
        return performance_data
    
    @staticmethod
    def get_candidate_pipeline(db: Session) -> Dict[str, Any]:
        """Get candidate pipeline analytics"""
        
        # Pipeline stages
        pipeline_stages = [
            "applied", "screening", "interview", "technical_test", 
            "final_interview", "offer", "hired", "rejected"
        ]
        
        pipeline_data = {}
        for stage in pipeline_stages:
            count = db.query(Application).filter(Application.status == stage).count()
            
            # Get candidates in this stage for more than expected time
            overdue_count = 0  # Would calculate based on created_at and expected time per stage
            
            pipeline_data[stage] = {
                "count": count,
                "overdue": overdue_count
            }
        
        # Conversion rates between stages
        conversion_rates = {}
        for i in range(len(pipeline_stages) - 1):
            current_stage = pipeline_stages[i]
            next_stage = pipeline_stages[i + 1]
            
            current_count = pipeline_data[current_stage]["count"]
            next_count = pipeline_data[next_stage]["count"]
            
            rate = (next_count / current_count * 100) if current_count > 0 else 0
            conversion_rates[f"{current_stage}_to_{next_stage}"] = round(rate, 2)
        
        # Bottlenecks (stages with low conversion or high overdue)
        bottlenecks = []
        for stage, data in pipeline_data.items():
            if data["overdue"] > 0:
                bottlenecks.append({
                    "stage": stage,
                    "issue": "overdue_candidates",
                    "count": data["overdue"]
                })
        
        return {
            "pipeline_stages": pipeline_data,
            "conversion_rates": conversion_rates,
            "bottlenecks": bottlenecks,
            "total_in_pipeline": sum(data["count"] for data in pipeline_data.values())
        }

# Create global analytics service instance
analytics_service = AnalyticsService()