from pydantic import BaseModel
from datetime import datetime


class GalleryItemBase(BaseModel):
    type: str = "photo"
    category: str | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    tags: str | None = None
    published: bool = True
    sort_order: int = 0


class GalleryItemCreate(GalleryItemBase):
    site_id: int


class GalleryItemUpdate(BaseModel):
    type: str | None = None
    category: str | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    tags: str | None = None
    published: bool | None = None
    sort_order: int | None = None


class GalleryItemResponse(GalleryItemBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class GalleryItemPublic(BaseModel):
    id: int
    type: str
    category: str | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None
    video_url: str | None = None
    tags: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
