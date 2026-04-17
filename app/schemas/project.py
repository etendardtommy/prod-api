from pydantic import BaseModel
from datetime import datetime


class ProjectBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    content: str | None = None
    image_url: str | None = None
    technologies: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    published: bool = True
    featured: bool = False
    sort_order: int = 0
    banner_link: str | None = None
    banner_label: str | None = None


class ProjectCreate(ProjectBase):
    site_id: int = 1


class ProjectUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    content: str | None = None
    image_url: str | None = None
    technologies: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    published: bool | None = None
    featured: bool | None = None
    sort_order: int | None = None
    banner_link: str | None = None
    banner_label: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProjectPublic(BaseModel):
    id: int
    title: str
    slug: str
    description: str | None = None
    content: str | None = None
    image_url: str | None = None
    technologies: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    featured: bool
    banner_link: str | None = None
    banner_label: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
