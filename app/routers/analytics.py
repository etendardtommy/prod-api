from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.analytics import PageView
from app.models.user import User
from app.schemas.analytics import VisitCreate, AnalyticsSummary

router = APIRouter()


# --- Public ---

@router.post("/visit", status_code=201)
async def track_visit(
    data: VisitCreate,
    request: Request,
    x_site_id: int = Header(default=1, alias="x-site-id"),
    db: Session = Depends(get_db),
):
    view = PageView(
        site_id=x_site_id,
        path=data.path,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )
    db.add(view)
    db.commit()
    return {"status": "ok"}


# --- Admin ---

@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    site_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(PageView)
    if site_id is not None:
        query = query.filter(PageView.site_id == site_id)

    total_views = query.count()
    unique_paths = query.with_entities(PageView.path).distinct().count()

    top_pages_query = (
        query.with_entities(PageView.path, func.count(PageView.id).label("views"))
        .group_by(PageView.path)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )
    top_pages = [{"path": p, "views": v} for p, v in top_pages_query]

    return AnalyticsSummary(
        total_views=total_views,
        unique_paths=unique_paths,
        top_pages=top_pages,
    )
