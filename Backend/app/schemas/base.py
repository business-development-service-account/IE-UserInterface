from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BaseResponse(BaseModel):
    """Base response schema with common fields."""

    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Timestamp when the record was created")
    updated_at: datetime = Field(..., description="Timestamp when the record was last updated")
    is_active: bool = Field(True, description="Whether the record is active")

    class Config:
        from_attributes = True