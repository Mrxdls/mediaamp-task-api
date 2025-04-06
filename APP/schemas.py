from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserSchema(BaseModel):
    id: Optional[int] = Field(None, description="User ID")
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Password of the user")
    role: str = Field(..., description="Role of the user")

    class Config:
        from_attributes = True

class loginUserSchema(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

    class Config:
        from_attributes = True
    
class TaskManagerSchema(BaseModel):
    id: Optional[int] = Field(None, description="Task ID")
    task_name: str = Field(..., description="Name of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    is_active: bool = Field(..., description="Is the task active?")
    priority: str = Field(..., description="Priority of the task")
    created_at: Optional[datetime] = Field(None, description="Creation date of the task")
    assigned_user: Optional[int] = Field(None, description="ID of the assigned user")

    class Config:
        from_attributes = True
class TaskLoggerSchema(BaseModel):
    id: Optional[int] = Field(None, description="Log ID")
    task_id: int = Field(..., description="ID of the task being logged")
    logged_at: Optional[datetime] = Field(None, description="Date and time when the task was logged")

    class Config:
        from_attributes = True
class AuditLoggerSchema(BaseModel):
    id: Optional[int] = Field(None, description="Audit Log ID")
    task_id: int = Field(..., description="ID of the task being audited")
    previous_state: str = Field(..., description="Previous state of the task")
    current_state: str = Field(..., description="Current state of the task")
    action_by: str = Field(..., description="User who performed the action")
    timestamp: Optional[datetime] = Field(None, description="Timestamp of the action")

    class Config:
        from_attributes = True
