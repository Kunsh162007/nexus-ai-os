"""
Agent API routes for Nexus AI OS
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid

from core.database import get_db
from models.agent import (
    Agent,
    AgentCreate,
    AgentUpdate,
    AgentResponse,
    AgentMetrics,
    AgentTask,
    AgentTaskResult,
    AgentType,
    AgentStatus
)
from services.agent_orchestrator import get_orchestrator
from loguru import logger


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    db: Session = Depends(get_db)
):
    """Create a new agent"""
    try:
        # Generate agent ID
        agent_id = f"agent_{agent_data.type.value}_{uuid.uuid4().hex[:8]}"
        
        # Create agent in database
        db_agent = Agent(
            id=agent_id,
            name=agent_data.name,
            type=agent_data.type,
            description=agent_data.description,
            capabilities=agent_data.capabilities,
            configuration=agent_data.configuration,
            metadata=agent_data.metadata,
            status=AgentStatus.IDLE
        )
        
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        
        # Register in orchestrator
        orchestrator = get_orchestrator()
        await orchestrator.register_agent(
            agent_id=agent_id,
            agent_type=agent_data.type,
            capabilities=agent_data.capabilities,
            metadata=agent_data.metadata
        )
        
        logger.info(f"Created agent: {agent_id}")
        return db_agent
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )


@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    agent_type: Optional[AgentType] = None,
    status_filter: Optional[AgentStatus] = None,
    db: Session = Depends(get_db)
):
    """List all agents with optional filters"""
    try:
        query = db.query(Agent)
        
        if agent_type:
            query = query.filter(Agent.type == agent_type)
        
        if status_filter:
            query = query.filter(Agent.status == status_filter)
        
        agents = query.offset(skip).limit(limit).all()
        return agents
        
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {str(e)}"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent by ID"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        return agent
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {str(e)}"
        )


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        # Update fields
        update_data = agent_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        db.commit()
        db.refresh(agent)
        
        logger.info(f"Updated agent: {agent_id}")
        return agent
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update agent: {str(e)}"
        )


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Delete agent"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        db.delete(agent)
        db.commit()
        
        logger.info(f"Deleted agent: {agent_id}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete agent: {str(e)}"
        )


@router.get("/{agent_id}/metrics", response_model=AgentMetrics)
async def get_agent_metrics(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent performance metrics"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        # Calculate uptime percentage
        uptime_percentage = 95.0  # Placeholder - calculate from heartbeats
        
        return AgentMetrics(
            agent_id=agent_id,
            tasks_completed=agent.tasks_completed,
            tasks_failed=agent.tasks_failed,
            average_response_time=agent.average_response_time,
            success_rate=agent.success_rate,
            uptime_percentage=uptime_percentage,
            last_24h_tasks=0,  # Placeholder
            last_7d_tasks=0    # Placeholder
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting agent metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent metrics: {str(e)}"
        )


@router.post("/{agent_id}/tasks", response_model=AgentTaskResult)
async def assign_task_to_agent(
    agent_id: str,
    task: AgentTask,
    db: Session = Depends(get_db)
):
    """Assign a task directly to a specific agent"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        if agent.status == AgentStatus.OFFLINE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Agent {agent_id} is offline"
            )
        
        # Execute task
        orchestrator = get_orchestrator()
        result = await orchestrator.execute_task(agent_id, task)
        
        # Update agent stats
        if result.status == "completed":
            agent.tasks_completed += 1
        else:
            agent.tasks_failed += 1
        
        agent.success_rate = int(
            (agent.tasks_completed / (agent.tasks_completed + agent.tasks_failed)) * 100
        )
        
        db.commit()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to assign task: {str(e)}"
        )


@router.post("/{agent_id}/heartbeat")
async def agent_heartbeat(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Update agent heartbeat"""
    try:
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        from datetime import datetime
        agent.last_active_at = datetime.utcnow()
        db.commit()
        
        # Update in orchestrator
        orchestrator = get_orchestrator()
        await orchestrator.heartbeat(agent_id)
        
        return {"status": "ok", "agent_id": agent_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating heartbeat: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update heartbeat: {str(e)}"
        )

# Made with Bob
