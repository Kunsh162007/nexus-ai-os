"""
Task API routes for Nexus AI OS
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from loguru import logger

from models.agent import AgentTask, AgentTaskResult
from services.agent_orchestrator import get_orchestrator


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=AgentTaskResult)
async def create_task(task: AgentTask):
    """
    Create and route a task to the best-suited agent(s)
    The orchestrator will automatically select the optimal agent
    """
    try:
        orchestrator = get_orchestrator()
        
        # Route task to best agent
        assigned_agent = await orchestrator.route_task(task)
        
        if not assigned_agent:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No suitable agents available for this task"
            )
        
        # Execute task
        result = await orchestrator.execute_task(assigned_agent, task)
        
        logger.info(f"Task {task.task_id} completed by agent {assigned_agent}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.post("/batch", response_model=List[AgentTaskResult])
async def create_batch_tasks(tasks: List[AgentTask]):
    """Create multiple tasks and route them intelligently"""
    try:
        orchestrator = get_orchestrator()
        results = []
        
        for task in tasks:
            assigned_agent = await orchestrator.route_task(task)
            
            if assigned_agent:
                result = await orchestrator.execute_task(assigned_agent, task)
                results.append(result)
            else:
                results.append(
                    AgentTaskResult(
                        task_id=task.task_id,
                        agent_id="none",
                        status="failed",
                        result=None,
                        error="No suitable agent available",
                        execution_time=0,
                        timestamp=datetime.utcnow()
                    )
                )
        
        return results
        
    except Exception as e:
        logger.error(f"Error creating batch tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create batch tasks: {str(e)}"
        )


@router.get("/{task_id}", response_model=AgentTaskResult)
async def get_task_result(task_id: str):
    """Get task result by ID"""
    try:
        # Retrieve from Redis or database
        from core.database import get_redis_client
        import json
        
        async with get_redis_client() as redis:
            task_data = await redis.get(f"task:{task_id}")
            
            if not task_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task {task_id} not found"
                )
            
            return json.loads(task_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task result: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task result: {str(e)}"
        )

# Made with Bob
