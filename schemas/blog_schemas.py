from datetime import datetime
from pydantic import BaseModel


class BlogBase(BaseModel):
    """Base schemas for blogs"""
    name: str
    text: str


class BlogCreate(BlogBase):
    """Schemas for create blog"""
    pass


class BlogUpdate(BlogBase):
    """Schemas for update blog"""
    updated_at: datetime = datetime.now()