"""
Database Schemas for Baby Development Tracker

Each Pydantic model represents a collection in your database.
Collection name is the lowercase of the class name by default.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date

class Baby(BaseModel):
    """Baby profile schema (collection: "baby")"""
    name: str = Field(..., description="Baby's name")
    gender: Optional[Literal["male", "female"]] = Field(None, description="Gender")
    birth_date: Optional[date] = Field(None, description="Birth date (YYYY-MM-DD)")
    notes: Optional[str] = Field(None, description="Additional notes")

class Milestone(BaseModel):
    """Milestone entry schema (collection: "milestone")"""
    baby_id: str = Field(..., description="Associated baby ID as string")
    title: str = Field(..., description="Milestone title, e.g., 'First Crawl'")
    date_achieved: Optional[date] = Field(None, description="Date achieved")
    description: Optional[str] = Field(None, description="Details about the milestone")

class Growthrecord(BaseModel):
    """Growth record schema (collection: "growthrecord")"""
    baby_id: str = Field(..., description="Associated baby ID as string")
    date_recorded: Optional[date] = Field(None, description="Date recorded")
    weight_kg: Optional[float] = Field(None, ge=0, description="Weight in kilograms")
    height_cm: Optional[float] = Field(None, ge=0, description="Height in centimeters")
    head_circumference_cm: Optional[float] = Field(None, ge=0, description="Head circumference in centimeters")
