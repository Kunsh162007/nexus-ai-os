"""
Database connection management for Nexus AI OS
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from neo4j import GraphDatabase
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import redis.asyncio as aioredis
from typing import Generator, AsyncGenerator
from contextlib import asynccontextmanager
from loguru import logger

from .config import settings


# SQLAlchemy Setup
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=settings.POOL_RECYCLE,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development"
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Neo4j Setup
class Neo4jConnection:
    """Neo4j database connection manager"""
    
    def __init__(self):
        self._driver = None
    
    def connect(self):
        """Connect to Neo4j"""
        try:
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            logger.info("Connected to Neo4j")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    def close(self):
        """Close Neo4j connection"""
        if self._driver:
            self._driver.close()
            logger.info("Neo4j connection closed")
    
    def get_session(self):
        """Get Neo4j session"""
        if not self._driver:
            self.connect()
        return self._driver.session()
    
    def verify_connectivity(self):
        """Verify Neo4j connectivity"""
        try:
            with self._driver.session() as session:
                result = session.run("RETURN 1 as num")
                return result.single()["num"] == 1
        except Exception as e:
            logger.error(f"Neo4j connectivity check failed: {e}")
            return False


neo4j_connection = Neo4jConnection()


def get_neo4j_session():
    """Get Neo4j session"""
    session = neo4j_connection.get_session()
    try:
        yield session
    finally:
        session.close()


# Qdrant Setup
class QdrantConnection:
    """Qdrant vector database connection manager"""
    
    def __init__(self):
        self._client = None
    
    def connect(self):
        """Connect to Qdrant"""
        try:
            self._client = QdrantClient(url=settings.QDRANT_URL)
            self._ensure_collection()
            logger.info("Connected to Qdrant")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
    
    def _ensure_collection(self):
        """Ensure collection exists"""
        try:
            collections = self._client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if settings.QDRANT_COLLECTION not in collection_names:
                self._client.create_collection(
                    collection_name=settings.QDRANT_COLLECTION,
                    vectors_config=VectorParams(
                        size=settings.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {settings.QDRANT_COLLECTION}")
        except Exception as e:
            logger.error(f"Failed to ensure Qdrant collection: {e}")
            raise
    
    def get_client(self) -> QdrantClient:
        """Get Qdrant client"""
        if not self._client:
            self.connect()
        return self._client
    
    def close(self):
        """Close Qdrant connection"""
        if self._client:
            self._client.close()
            logger.info("Qdrant connection closed")


qdrant_connection = QdrantConnection()


def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client"""
    return qdrant_connection.get_client()


# Redis Setup
class RedisConnection:
    """Redis connection manager"""
    
    def __init__(self):
        self._pool = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self._pool = aioredis.ConnectionPool.from_url(
                settings.REDIS_URL,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
                decode_responses=True
            )
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def close(self):
        """Close Redis connection"""
        if self._pool:
            await self._pool.disconnect()
            logger.info("Redis connection closed")
    
    async def get_client(self) -> aioredis.Redis:
        """Get Redis client"""
        if not self._pool:
            await self.connect()
        return aioredis.Redis(connection_pool=self._pool)


redis_connection = RedisConnection()


@asynccontextmanager
async def get_redis_client() -> AsyncGenerator[aioredis.Redis, None]:
    """Get Redis client as async context manager"""
    client = await redis_connection.get_client()
    try:
        yield client
    finally:
        await client.close()


# Database initialization
async def init_databases():
    """Initialize all database connections"""
    logger.info("Initializing databases...")
    
    # Create PostgreSQL tables
    Base.metadata.create_all(bind=engine)
    logger.info("PostgreSQL tables created")
    
    # Connect to Neo4j
    neo4j_connection.connect()
    
    # Connect to Qdrant
    qdrant_connection.connect()
    
    # Connect to Redis
    await redis_connection.connect()
    
    logger.info("All databases initialized successfully")


async def close_databases():
    """Close all database connections"""
    logger.info("Closing database connections...")
    
    neo4j_connection.close()
    qdrant_connection.close()
    await redis_connection.close()
    
    logger.info("All database connections closed")

# Made with Bob
