# app/models/metadata.py

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ProcessingStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    INDEXED = "indexed"

class DocumentMetadata(BaseModel):
    """Document metadata model"""
    id: str
    title: str
    source: str
    file_type: str
    file_size: int
    created_at: datetime
    updated_at: datetime
    processed_at: Optional[datetime]
    status: ProcessingStatus = ProcessingStatus.PENDING
    chunk_count: Optional[int]
    embedding_model: Optional[str]
    error: Optional[str]
    user_id: Optional[str]
    workspace_id: Optional[str]
    permissions: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def update_status(self, status: ProcessingStatus, error: Optional[str] = None):
        """Update processing status"""
        self.status = status
        if error:
            self.error = error
        self.updated_at = datetime.utcnow()
        if status == ProcessingStatus.COMPLETED:
            self.processed_at = datetime.utcnow()