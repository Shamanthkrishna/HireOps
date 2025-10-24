from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.auth.auth import get_current_user
from app.models.models import User
from app.services.analytics_service import analytics_service
from typing import Dict, Any, List

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get comprehensive dashboard analytics"""
    
    # Only HR and Admin can access analytics
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        analytics_data = analytics_service.get_dashboard_analytics(db)
        return {
            "success": True,
            "data": analytics_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")

@router.get("/job/{job_id}")
async def get_job_analytics(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get detailed analytics for a specific job"""
    
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        job_analytics = analytics_service.get_job_analytics(db, job_id)
        
        if not job_analytics:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {
            "success": True,
            "data": job_analytics
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch job analytics: {str(e)}")

@router.get("/recruiters/performance")
async def get_recruiter_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, List[Dict[str, Any]]]:
    """Get performance metrics for all recruiters"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        performance_data = analytics_service.get_recruiter_performance(db)
        return {
            "success": True,
            "data": performance_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recruiter performance: {str(e)}")

@router.get("/pipeline")
async def get_candidate_pipeline(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get candidate pipeline analytics"""
    
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        pipeline_data = analytics_service.get_candidate_pipeline(db)
        return {
            "success": True,
            "data": pipeline_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch pipeline analytics: {str(e)}")

@router.get("/export/dashboard")
async def export_dashboard_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export dashboard analytics as CSV/PDF report"""
    
    if current_user.role not in ["hr", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # This would generate and return a downloadable report
    # Implementation would depend on requirements (CSV, PDF, Excel)
    return {
        "success": True,
        "message": "Report export feature coming soon",
        "data": {
            "download_url": "/api/analytics/download/dashboard-report.pdf",
            "generated_at": "2024-01-01T12:00:00Z"
        }
    }