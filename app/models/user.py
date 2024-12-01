# app/models/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class UserSettings(BaseModel):
    """User settings and preferences"""
    max_context_length: int = 5
    response_temperature: float = 0.7
    thread_enabled: bool = True
    notification_enabled: bool = True

class User(BaseModel):
    """User model"""
    id: str
    slack_id: str
    email: Optional[EmailStr] = None
    settings: UserSettings = UserSettings()
    workspace_id: str
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = {}

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }