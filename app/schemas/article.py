from pydantic import BaseModel
from datetime import datetime


class ArticleBase(BaseModel):
    title: str
    slug: str
    summary: str | None = None
    content: str | None = None
    image_url: str | None = None
    category: str | None = None
    tags: str | None = None
    published: bool = True


class ArticleCreate(ArticleBase):
    site_id: int


class ArticleUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    summary: str | None = None
    content: str | None = None
    image_url: str | None = None
    category: str | None = None
    tags: str | None = None
    published: bool | None = None


class ArticleResponse(ArticleBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ArticlePublic(BaseModel):
    id: int
    title: str
    slug: str
    summary: str | None = None
    content: str | None = None
    image_url: str | None = None
    category: str | None = None
    tags: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
