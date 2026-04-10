from pydantic import BaseModel
from datetime import datetime


class AboutBase(BaseModel):
    photo_url: str | None = None
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    cv_url: str | None = None
    published: bool = True


class AboutCreate(AboutBase):
    site_id: int = 1


class AboutUpdate(BaseModel):
    photo_url: str | None = None
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    cv_url: str | None = None
    published: bool | None = None


class AboutResponse(AboutBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AboutPublic(BaseModel):
    id: int
    photo_url: str | None = None
    bio: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    cv_url: str | None = None

    model_config = {"from_attributes": True}
