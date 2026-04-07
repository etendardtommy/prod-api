from pydantic import BaseModel
from datetime import datetime


class VisitCreate(BaseModel):
    path: str


class PageViewResponse(BaseModel):
    id: int
    site_id: int
    path: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalyticsSummary(BaseModel):
    total_views: int
    unique_paths: int
    top_pages: list[dict]
