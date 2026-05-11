"""
Knowledge Graph API routes for Nexus AI OS
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from loguru import logger

from services.knowledge_graph import get_knowledge_graph_service


router = APIRouter(prefix="/knowledge", tags=["knowledge"])


@router.get("/stats")
async def get_knowledge_stats():
    """Get knowledge graph statistics"""
    try:
        kg_service = get_knowledge_graph_service()
        stats = await kg_service.get_knowledge_graph_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting knowledge stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get knowledge stats: {str(e)}"
        )


@router.get("/context/{agent_id}")
async def get_agent_context(
    agent_id: str,
    task_type: str = Query(..., description="Type of task"),
    query: str = Query(..., description="Query for context"),
    limit: int = Query(10, ge=1, le=50)
):
    """Get relevant context for an agent"""
    try:
        kg_service = get_knowledge_graph_service()
        context = await kg_service.get_relevant_context(
            agent_id=agent_id,
            task_type=task_type,
            query=query,
            limit=limit
        )
        return context
        
    except Exception as e:
        logger.error(f"Error getting agent context: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent context: {str(e)}"
        )


@router.get("/history/{decision_type}")
async def get_decision_history(
    decision_type: str,
    limit: int = Query(20, ge=1, le=100)
):
    """
    Get decision history (Time Travel feature)
    Shows how similar decisions were made in the past
    """
    try:
        kg_service = get_knowledge_graph_service()
        history = await kg_service.get_decision_history(
            decision_type=decision_type,
            limit=limit
        )
        return {
            "decision_type": decision_type,
            "history": history,
            "count": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error getting decision history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get decision history: {str(e)}"
        )


@router.get("/network/{agent_id}")
async def get_agent_network(
    agent_id: str,
    depth: int = Query(2, ge=1, le=5)
):
    """Get agent's collaboration network"""
    try:
        kg_service = get_knowledge_graph_service()
        network = await kg_service.get_agent_network(
            agent_id=agent_id,
            depth=depth
        )
        return network
        
    except Exception as e:
        logger.error(f"Error getting agent network: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent network: {str(e)}"
        )


@router.get("/insights")
async def get_organizational_insights():
    """Get high-level organizational insights from knowledge graph"""
    try:
        kg_service = get_knowledge_graph_service()
        
        # Get stats
        stats = await kg_service.get_knowledge_graph_stats()
        
        # Get recent decision patterns
        recent_decisions = await kg_service.get_decision_history(
            decision_type="",
            limit=10
        )
        
        return {
            "stats": stats,
            "recent_decisions": recent_decisions,
            "insights": {
                "total_knowledge_nodes": stats.get("entities", 0),
                "active_collaborations": stats.get("collaborations", 0),
                "agent_utilization": "85%",  # Placeholder
                "knowledge_growth_rate": "+12% this week"  # Placeholder
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting organizational insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get organizational insights: {str(e)}"
        )

# Made with Bob
