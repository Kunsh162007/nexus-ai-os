"""
Agent data models for Nexus AI OS
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from core.database import Base


class AgentType(str, Enum):
    """Agent type enumeration"""
    SALES = "sales"
    LEGAL = "legal"
    ENGINEERING = "engineering"
    FINANCE = "finance"
    SUPPORT = "support"
    MARKETING = "marketing"
    HR = "hr"
    OPERATIONS = "operations"
    CUSTOM = "custom"


class AgentStatus(str, Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class Agent(Base):
    """Agent database model"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(SQLEnum(AgentType), nullable=False)
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.IDLE)
    description = Column(Text)
    capabilities = Column(JSON, default=list)
    configuration = Column(JSON, default=dict)
    metadata = Column(JSON, default=dict)
    
    # Performance metrics
    tasks_completed = Column(Integer, default=0)
    tasks_failed = Column(Integer, default=0)
    average_response_time = Column(Integer, default=0)  # milliseconds
    success_rate = Column(Integer, default=100)  # percentage
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_active_at = Column(DateTime(timezone=True))
    
    # Flags
    is_active = Column(Boolean, default=True)
    is_learning = Column(Boolean, default=True)


# Pydantic Models for API
class AgentBase(BaseModel):
    """Base agent schema"""
    name: str = Field(..., min_length=1, max_length=100)
    type: AgentType
    description: Optional[str] = None
    capabilities: List[str] = Field(default_factory=list)
    configuration: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentCreate(AgentBase):
    """Agent creation schema"""
    pass


class AgentUpdate(BaseModel):
    """Agent update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    configuration: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[AgentStatus] = None
    is_active: Optional[bool] = None


class AgentResponse(AgentBase):
    """Agent response schema"""
    id: str
    status: AgentStatus
    tasks_completed: int
    tasks_failed: int
    average_response_time: int
    success_rate: int
    created_at: datetime
    updated_at: Optional[datetime]
    last_active_at: Optional[datetime]
    is_active: bool
    is_learning: bool
    
    class Config:
        from_attributes = True


class AgentMetrics(BaseModel):
    """Agent performance metrics"""
    agent_id: str
    tasks_completed: int
    tasks_failed: int
    average_response_time: int
    success_rate: int
    uptime_percentage: float
    last_24h_tasks: int
    last_7d_tasks: int


class AgentTask(BaseModel):
    """Agent task schema"""
    task_id: str
    agent_id: str
    task_type: str
    description: str
    priority: int = Field(default=5, ge=1, le=10)
    context: Dict[str, Any] = Field(default_factory=dict)
    dependencies: List[str] = Field(default_factory=list)
    timeout: int = Field(default=300, ge=1)  # seconds
    
    
class AgentTaskResult(BaseModel):
    """Agent task result schema"""
    task_id: str
    agent_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: int  # milliseconds
    timestamp: datetime


class AgentCollaboration(BaseModel):
    """Agent collaboration schema"""
    collaboration_id: str
    agents: List[str]
    task_description: str
    coordination_strategy: str
    shared_context: Dict[str, Any] = Field(default_factory=dict)
    status: str
    created_at: datetime

# Made with Bob
