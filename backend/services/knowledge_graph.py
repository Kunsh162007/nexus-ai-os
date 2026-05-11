"""
Knowledge Graph Service - Organizational Memory Layer
Manages the Neo4j graph database for collective intelligence
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from loguru import logger
import json

from core.database import get_neo4j_session


class KnowledgeGraphService:
    """Service for managing organizational knowledge graph"""
    
    def __init__(self):
        self.session = None
    
    async def create_agent_node(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[str],
        metadata: Dict[str, Any]
    ):
        """Create agent node in knowledge graph"""
        try:
            query = """
            MERGE (a:Agent {id: $agent_id})
            SET a.type = $agent_type,
                a.capabilities = $capabilities,
                a.metadata = $metadata,
                a.created_at = datetime(),
                a.updated_at = datetime()
            RETURN a
            """
            
            with next(get_neo4j_session()) as session:
                session.run(
                    query,
                    agent_id=agent_id,
                    agent_type=agent_type,
                    capabilities=capabilities,
                    metadata=json.dumps(metadata)
                )
            
            logger.info(f"Created agent node: {agent_id}")
            
        except Exception as e:
            logger.error(f"Error creating agent node: {e}")
            raise
    
    async def create_task_assignment(
        self,
        agent_id: str,
        task_id: str,
        task_type: str
    ):
        """Create task assignment relationship"""
        try:
            query = """
            MATCH (a:Agent {id: $agent_id})
            MERGE (t:Task {id: $task_id})
            SET t.type = $task_type,
                t.created_at = datetime()
            MERGE (a)-[r:ASSIGNED_TO]->(t)
            SET r.assigned_at = datetime()
            RETURN a, t, r
            """
            
            with next(get_neo4j_session()) as session:
                session.run(
                    query,
                    agent_id=agent_id,
                    task_id=task_id,
                    task_type=task_type
                )
            
        except Exception as e:
            logger.error(f"Error creating task assignment: {e}")
            raise
    
    async def create_collaboration(
        self,
        collaboration_id: str,
        agent_ids: List[str],
        task_id: str
    ):
        """Create collaboration session in graph"""
        try:
            query = """
            MERGE (c:Collaboration {id: $collaboration_id})
            SET c.created_at = datetime()
            WITH c
            MATCH (t:Task {id: $task_id})
            MERGE (c)-[:FOR_TASK]->(t)
            WITH c
            UNWIND $agent_ids AS agent_id
            MATCH (a:Agent {id: agent_id})
            MERGE (a)-[:PARTICIPATES_IN]->(c)
            RETURN c
            """
            
            with next(get_neo4j_session()) as session:
                session.run(
                    query,
                    collaboration_id=collaboration_id,
                    agent_ids=agent_ids,
                    task_id=task_id
                )
            
        except Exception as e:
            logger.error(f"Error creating collaboration: {e}")
            raise
    
    async def store_task_result(
        self,
        task_id: str,
        agent_id: str,
        result: Dict[str, Any],
        execution_time: float
    ):
        """Store task result and create knowledge relationships"""
        try:
            query = """
            MATCH (t:Task {id: $task_id})
            MATCH (a:Agent {id: $agent_id})
            SET t.completed_at = datetime(),
                t.result = $result,
                t.execution_time = $execution_time,
                t.status = 'completed'
            MERGE (a)-[r:COMPLETED]->(t)
            SET r.completed_at = datetime(),
                r.execution_time = $execution_time
            
            // Extract and link entities from result
            WITH t, a
            UNWIND keys($result) AS key
            WITH t, a, key, $result[key] AS value
            WHERE value IS NOT NULL
            MERGE (e:Entity {key: key, value: toString(value)})
            MERGE (t)-[:PRODUCED]->(e)
            
            RETURN t, a
            """
            
            with next(get_neo4j_session()) as session:
                session.run(
                    query,
                    task_id=task_id,
                    agent_id=agent_id,
                    result=json.dumps(result),
                    execution_time=execution_time
                )
            
        except Exception as e:
            logger.error(f"Error storing task result: {e}")
            raise
    
    async def get_relevant_context(
        self,
        agent_id: str,
        task_type: str,
        query: str,
        limit: int = 10
    ) -> Dict[str, Any]:
        """Get relevant context from knowledge graph"""
        try:
            # Get similar past tasks
            cypher_query = """
            MATCH (a:Agent {id: $agent_id})-[:COMPLETED]->(t:Task)
            WHERE t.type = $task_type AND t.status = 'completed'
            WITH t
            ORDER BY t.completed_at DESC
            LIMIT $limit
            OPTIONAL MATCH (t)-[:PRODUCED]->(e:Entity)
            RETURN t.id AS task_id,
                   t.type AS task_type,
                   t.result AS result,
                   t.execution_time AS execution_time,
                   collect(DISTINCT {key: e.key, value: e.value}) AS entities
            """
            
            with next(get_neo4j_session()) as session:
                result = session.run(
                    cypher_query,
                    agent_id=agent_id,
                    task_type=task_type,
                    limit=limit
                )
                
                past_tasks = []
                for record in result:
                    past_tasks.append({
                        "task_id": record["task_id"],
                        "task_type": record["task_type"],
                        "result": json.loads(record["result"]) if record["result"] else {},
                        "execution_time": record["execution_time"],
                        "entities": record["entities"]
                    })
            
            # Get related agents' insights
            related_query = """
            MATCH (a:Agent {id: $agent_id})-[:PARTICIPATES_IN]->(c:Collaboration)
                  <-[:PARTICIPATES_IN]-(other:Agent)
            WHERE other.id <> $agent_id
            MATCH (other)-[:COMPLETED]->(t:Task {type: $task_type})
            WITH other, t
            ORDER BY t.completed_at DESC
            LIMIT 5
            RETURN other.id AS agent_id,
                   other.type AS agent_type,
                   collect({
                       task_id: t.id,
                       result: t.result
                   }) AS insights
            """
            
            with next(get_neo4j_session()) as session:
                result = session.run(
                    related_query,
                    agent_id=agent_id,
                    task_type=task_type
                )
                
                related_insights = []
                for record in result:
                    insights = []
                    for insight in record["insights"]:
                        if insight["result"]:
                            insights.append({
                                "task_id": insight["task_id"],
                                "result": json.loads(insight["result"])
                            })
                    
                    related_insights.append({
                        "agent_id": record["agent_id"],
                        "agent_type": record["agent_type"],
                        "insights": insights
                    })
            
            return {
                "past_tasks": past_tasks,
                "related_insights": related_insights,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error getting relevant context: {e}")
            return {"past_tasks": [], "related_insights": [], "query": query}
    
    async def update_agent_performance(
        self,
        agent_id: str,
        performance_score: float,
        specialization_scores: Dict[str, float]
    ):
        """Update agent performance metrics in graph"""
        try:
            query = """
            MATCH (a:Agent {id: $agent_id})
            SET a.performance_score = $performance_score,
                a.specialization_scores = $specialization_scores,
                a.updated_at = datetime()
            RETURN a
            """
            
            with next(get_neo4j_session()) as session:
                session.run(
                    query,
                    agent_id=agent_id,
                    performance_score=performance_score,
                    specialization_scores=json.dumps(specialization_scores)
                )
            
        except Exception as e:
            logger.error(f"Error updating agent performance: {e}")
            raise
    
    async def get_decision_history(
        self,
        decision_type: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get history of similar decisions (Time Travel feature)"""
        try:
            query = """
            MATCH (t:Task)
            WHERE t.type CONTAINS $decision_type AND t.status = 'completed'
            OPTIONAL MATCH (a:Agent)-[:COMPLETED]->(t)
            OPTIONAL MATCH (t)-[:PRODUCED]->(e:Entity)
            WITH t, a, collect(DISTINCT {key: e.key, value: e.value}) AS entities
            ORDER BY t.completed_at DESC
            LIMIT $limit
            RETURN t.id AS task_id,
                   t.type AS task_type,
                   t.result AS result,
                   t.completed_at AS completed_at,
                   a.id AS agent_id,
                   a.type AS agent_type,
                   entities
            """
            
            with next(get_neo4j_session()) as session:
                result = session.run(
                    query,
                    decision_type=decision_type,
                    limit=limit
                )
                
                history = []
                for record in result:
                    history.append({
                        "task_id": record["task_id"],
                        "task_type": record["task_type"],
                        "result": json.loads(record["result"]) if record["result"] else {},
                        "completed_at": record["completed_at"],
                        "agent_id": record["agent_id"],
                        "agent_type": record["agent_type"],
                        "entities": record["entities"]
                    })
                
                return history
            
        except Exception as e:
            logger.error(f"Error getting decision history: {e}")
            return []
    
    async def get_knowledge_graph_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge graph"""
        try:
            query = """
            MATCH (a:Agent)
            WITH count(a) AS agent_count
            MATCH (t:Task)
            WITH agent_count, count(t) AS task_count
            MATCH (c:Collaboration)
            WITH agent_count, task_count, count(c) AS collaboration_count
            MATCH (e:Entity)
            RETURN agent_count, task_count, collaboration_count, count(e) AS entity_count
            """
            
            with next(get_neo4j_session()) as session:
                result = session.run(query)
                record = result.single()
                
                return {
                    "agents": record["agent_count"],
                    "tasks": record["task_count"],
                    "collaborations": record["collaboration_count"],
                    "entities": record["entity_count"]
                }
            
        except Exception as e:
            logger.error(f"Error getting graph stats: {e}")
            return {"agents": 0, "tasks": 0, "collaborations": 0, "entities": 0}
    
    async def get_agent_network(
        self,
        agent_id: str,
        depth: int = 2
    ) -> Dict[str, Any]:
        """Get agent's collaboration network"""
        try:
            query = """
            MATCH path = (a:Agent {id: $agent_id})-[:PARTICIPATES_IN*1..$depth]-(other:Agent)
            WHERE other.id <> $agent_id
            WITH other, length(path) AS distance
            ORDER BY distance
            RETURN other.id AS agent_id,
                   other.type AS agent_type,
                   min(distance) AS distance,
                   count(*) AS collaboration_count
            """
            
            with next(get_neo4j_session()) as session:
                result = session.run(
                    query,
                    agent_id=agent_id,
                    depth=depth
                )
                
                network = []
                for record in result:
                    network.append({
                        "agent_id": record["agent_id"],
                        "agent_type": record["agent_type"],
                        "distance": record["distance"],
                        "collaboration_count": record["collaboration_count"]
                    })
                
                return {
                    "agent_id": agent_id,
                    "network": network
                }
            
        except Exception as e:
            logger.error(f"Error getting agent network: {e}")
            return {"agent_id": agent_id, "network": []}


# Global service instance
_knowledge_graph_service = None

def get_knowledge_graph_service() -> KnowledgeGraphService:
    """Get knowledge graph service instance"""
    global _knowledge_graph_service
    if _knowledge_graph_service is None:
        _knowledge_graph_service = KnowledgeGraphService()
    return _knowledge_graph_service

# Made with Bob
