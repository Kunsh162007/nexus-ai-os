"""
Agent Orchestration Service - The Neural Mesh Core
Manages self-organizing agent swarms and task routing
"""
import asyncio
import uuid
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from loguru import logger
import json

from models.agent import AgentType, AgentStatus, AgentTask, AgentTaskResult
from services.gemini_service import get_gemini_service
from services.knowledge_graph import get_knowledge_graph_service
from core.database import get_redis_client


class AgentOrchestrator:
    """
    Core orchestration engine for the Neural Mesh
    Implements self-organizing agent swarms with emergent intelligence
    """
    
    def __init__(self):
        self.gemini = get_gemini_service()
        self.knowledge_graph = get_knowledge_graph_service()
        self.active_agents: Dict[str, Dict[str, Any]] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.collaboration_sessions: Dict[str, Dict[str, Any]] = {}
        
    async def register_agent(
        self,
        agent_id: str,
        agent_type: AgentType,
        capabilities: List[str],
        meta_data: Dict[str, Any]
    ) -> bool:
        """Register an agent in the neural mesh"""
        try:
            self.active_agents[agent_id] = {
                "id": agent_id,
                "type": agent_type,
                "capabilities": capabilities,
                "status": AgentStatus.IDLE,
                "meta_data": meta_data,
                "current_task": None,
                "performance_score": 1.0,
                "specialization_score": {},
                "last_heartbeat": datetime.utcnow()
            }
            
            # Register in knowledge graph
            await self.knowledge_graph.create_agent_node(
                agent_id=agent_id,
                agent_type=agent_type.value,
                capabilities=capabilities,
                meta_data=meta_data
            )
            
            logger.info(f"Agent {agent_id} ({agent_type.value}) registered in neural mesh")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent {agent_id}: {e}")
            return False
    
    async def route_task(
        self,
        task: AgentTask
    ) -> Optional[str]:
        """
        Intelligently route task to best-suited agent(s)
        Uses emergent specialization and performance history
        """
        try:
            # Analyze task requirements using Gemini
            task_analysis = await self._analyze_task_requirements(task)
            
            # Find suitable agents
            suitable_agents = await self._find_suitable_agents(
                task_analysis,
                task.task_type
            )
            
            if not suitable_agents:
                logger.warning(f"No suitable agents found for task {task.task_id}")
                return None
            
            # Check if task requires collaboration
            if task_analysis.get("requires_collaboration", False):
                return await self._initiate_collaboration(task, suitable_agents)
            
            # Select best single agent
            best_agent = await self._select_best_agent(suitable_agents, task_analysis)
            
            # Assign task
            await self._assign_task_to_agent(best_agent, task)
            
            return best_agent
            
        except Exception as e:
            logger.error(f"Error routing task {task.task_id}: {e}")
            return None
    
    async def _analyze_task_requirements(
        self,
        task: AgentTask
    ) -> Dict[str, Any]:
        """Analyze task using Gemini to understand requirements"""
        try:
            prompt = f"""
Analyze this task and determine:
1. Required agent capabilities
2. Complexity level (1-10)
3. Whether it requires multiple agents (collaboration)
4. Estimated time to complete (seconds)
5. Priority factors

Task Type: {task.task_type}
Description: {task.description}
Context: {json.dumps(task.context)}

Provide analysis as JSON.
"""
            
            analysis = await self.gemini.generate_structured_response(
                prompt=prompt,
                schema={
                    "required_capabilities": ["string"],
                    "complexity": "number",
                    "requires_collaboration": "boolean",
                    "estimated_time": "number",
                    "priority_factors": ["string"],
                    "suggested_agent_types": ["string"]
                },
                use_flash=True
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing task: {e}")
            return {
                "required_capabilities": [],
                "complexity": 5,
                "requires_collaboration": False,
                "estimated_time": 60,
                "priority_factors": [],
                "suggested_agent_types": []
            }
    
    async def _find_suitable_agents(
        self,
        task_analysis: Dict[str, Any],
        task_type: str
    ) -> List[str]:
        """Find agents suitable for the task"""
        suitable = []
        required_caps = set(task_analysis.get("required_capabilities", []))
        suggested_types = task_analysis.get("suggested_agent_types", [])
        
        for agent_id, agent_data in self.active_agents.items():
            # Check if agent is available
            if agent_data["status"] not in [AgentStatus.IDLE, AgentStatus.ACTIVE]:
                continue
            
            # Check capabilities match
            agent_caps = set(agent_data["capabilities"])
            if required_caps and not required_caps.intersection(agent_caps):
                continue
            
            # Check type match
            if suggested_types and agent_data["type"].value not in suggested_types:
                continue
            
            # Check specialization score for this task type
            spec_score = agent_data["specialization_score"].get(task_type, 0.5)
            if spec_score > 0.3:  # Minimum threshold
                suitable.append(agent_id)
        
        return suitable
    
    async def _select_best_agent(
        self,
        suitable_agents: List[str],
        task_analysis: Dict[str, Any]
    ) -> str:
        """Select the best agent based on performance and specialization"""
        if len(suitable_agents) == 1:
            return suitable_agents[0]
        
        # Score each agent
        scores = {}
        for agent_id in suitable_agents:
            agent = self.active_agents[agent_id]
            
            # Base performance score
            score = agent["performance_score"]
            
            # Specialization bonus
            task_type = task_analysis.get("task_type", "")
            spec_score = agent["specialization_score"].get(task_type, 0.5)
            score += spec_score * 0.5
            
            # Availability bonus (idle agents preferred)
            if agent["status"] == AgentStatus.IDLE:
                score += 0.3
            
            scores[agent_id] = score
        
        # Return agent with highest score
        return max(scores.items(), key=lambda x: x[1])[0]
    
    async def _assign_task_to_agent(
        self,
        agent_id: str,
        task: AgentTask
    ):
        """Assign task to specific agent"""
        try:
            agent = self.active_agents[agent_id]
            agent["status"] = AgentStatus.BUSY
            agent["current_task"] = task.task_id
            
            # Store task in Redis for tracking
            async with get_redis_client() as redis:
                await redis.setex(
                    f"task:{task.task_id}",
                    task.timeout,
                    json.dumps({
                        "agent_id": agent_id,
                        "task": task.dict(),
                        "assigned_at": datetime.utcnow().isoformat()
                    })
                )
            
            # Create relationship in knowledge graph
            await self.knowledge_graph.create_task_assignment(
                agent_id=agent_id,
                task_id=task.task_id,
                task_type=task.task_type
            )
            
            logger.info(f"Task {task.task_id} assigned to agent {agent_id}")
            
        except Exception as e:
            logger.error(f"Error assigning task: {e}")
            raise
    
    async def _initiate_collaboration(
        self,
        task: AgentTask,
        suitable_agents: List[str]
    ) -> str:
        """Initiate multi-agent collaboration"""
        try:
            collaboration_id = str(uuid.uuid4())
            
            # Select agents for collaboration (2-5 agents)
            num_agents = min(len(suitable_agents), 5)
            selected_agents = suitable_agents[:num_agents]
            
            # Create collaboration session
            self.collaboration_sessions[collaboration_id] = {
                "id": collaboration_id,
                "task": task,
                "agents": selected_agents,
                "status": "active",
                "shared_context": {},
                "messages": [],
                "created_at": datetime.utcnow()
            }
            
            # Assign to all agents
            for agent_id in selected_agents:
                await self._assign_task_to_agent(agent_id, task)
            
            # Create collaboration node in knowledge graph
            await self.knowledge_graph.create_collaboration(
                collaboration_id=collaboration_id,
                agent_ids=selected_agents,
                task_id=task.task_id
            )
            
            logger.info(f"Collaboration {collaboration_id} initiated with {num_agents} agents")
            return collaboration_id
            
        except Exception as e:
            logger.error(f"Error initiating collaboration: {e}")
            raise
    
    async def execute_task(
        self,
        agent_id: str,
        task: AgentTask
    ) -> AgentTaskResult:
        """Execute task using agent with Gemini"""
        start_time = datetime.utcnow()
        
        try:
            agent = self.active_agents[agent_id]
            
            # Get relevant context from knowledge graph
            context = await self.knowledge_graph.get_relevant_context(
                agent_id=agent_id,
                task_type=task.task_type,
                query=task.description
            )
            
            # Build prompt with context
            prompt = self._build_task_prompt(agent, task, context)
            
            # Execute with Gemini
            response = await self.gemini.generate_response(
                prompt=prompt,
                use_flash=(task.priority < 7),  # Use Flash for lower priority
                temperature=0.7
            )
            
            # Parse response
            result = await self._parse_task_response(response, task)
            
            # Update agent performance
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            await self._update_agent_performance(
                agent_id=agent_id,
                task_type=task.task_type,
                success=True,
                execution_time=execution_time
            )
            
            # Store result in knowledge graph
            await self.knowledge_graph.store_task_result(
                task_id=task.task_id,
                agent_id=agent_id,
                result=result,
                execution_time=execution_time
            )
            
            return AgentTaskResult(
                task_id=task.task_id,
                agent_id=agent_id,
                status="completed",
                result=result,
                error=None,
                execution_time=int(execution_time),
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error executing task {task.task_id}: {e}")
            
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            await self._update_agent_performance(
                agent_id=agent_id,
                task_type=task.task_type,
                success=False,
                execution_time=execution_time
            )
            
            return AgentTaskResult(
                task_id=task.task_id,
                agent_id=agent_id,
                status="failed",
                result=None,
                error=str(e),
                execution_time=int(execution_time),
                timestamp=datetime.utcnow()
            )
        
        finally:
            # Update agent status
            if agent_id in self.active_agents:
                self.active_agents[agent_id]["status"] = AgentStatus.IDLE
                self.active_agents[agent_id]["current_task"] = None
    
    def _build_task_prompt(
        self,
        agent: Dict[str, Any],
        task: AgentTask,
        context: Dict[str, Any]
    ) -> str:
        """Build comprehensive prompt for task execution"""
        return f"""
You are a {agent['type'].value} agent in the Nexus AI Operating System.

Your capabilities: {', '.join(agent['capabilities'])}

Task: {task.description}
Task Type: {task.task_type}
Priority: {task.priority}/10

Context from organizational knowledge:
{json.dumps(context, indent=2)}

Additional context:
{json.dumps(task.context, indent=2)}

Please complete this task thoroughly and provide a detailed response.
If you need information from other agents, indicate what you need.
"""
    
    async def _parse_task_response(
        self,
        response: str,
        task: AgentTask
    ) -> Dict[str, Any]:
        """Parse and structure task response"""
        try:
            # Try to extract structured data
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            
            # Return as text result
            return {
                "response": response,
                "task_type": task.task_type,
                "completed": True
            }
            
        except Exception as e:
            logger.warning(f"Could not parse structured response: {e}")
            return {"response": response}
    
    async def _update_agent_performance(
        self,
        agent_id: str,
        task_type: str,
        success: bool,
        execution_time: float
    ):
        """Update agent performance metrics and specialization"""
        try:
            agent = self.active_agents[agent_id]
            
            # Update overall performance score
            if success:
                agent["performance_score"] = min(1.0, agent["performance_score"] + 0.01)
            else:
                agent["performance_score"] = max(0.0, agent["performance_score"] - 0.05)
            
            # Update specialization score for this task type
            current_spec = agent["specialization_score"].get(task_type, 0.5)
            if success:
                agent["specialization_score"][task_type] = min(1.0, current_spec + 0.05)
            else:
                agent["specialization_score"][task_type] = max(0.0, current_spec - 0.03)
            
            # Update in knowledge graph
            await self.knowledge_graph.update_agent_performance(
                agent_id=agent_id,
                performance_score=agent["performance_score"],
                specialization_scores=agent["specialization_score"]
            )
            
        except Exception as e:
            logger.error(f"Error updating agent performance: {e}")
    
    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of an agent"""
        return self.active_agents.get(agent_id)
    
    async def get_active_agents(self) -> List[Dict[str, Any]]:
        """Get all active agents"""
        return list(self.active_agents.values())
    
    async def heartbeat(self, agent_id: str) -> bool:
        """Update agent heartbeat"""
        if agent_id in self.active_agents:
            self.active_agents[agent_id]["last_heartbeat"] = datetime.utcnow()
            return True
        return False


# Global orchestrator instance
_orchestrator = None

def get_orchestrator() -> AgentOrchestrator:
    """Get agent orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = AgentOrchestrator()
    return _orchestrator

# Made with Bob
