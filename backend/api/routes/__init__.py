"""
API routes for Nexus AI OS
"""
from .agents import router as agents_router
from .tasks import router as tasks_router
from .knowledge import router as knowledge_router

__all__ = ["agents_router", "tasks_router", "knowledge_router"]

# Made with Bob
