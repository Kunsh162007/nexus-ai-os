"""
Logging configuration for Nexus AI OS
"""
import sys
from loguru import logger
from .config import settings


def setup_logging():
    """Configure application logging"""
    
    # Remove default handler
    logger.remove()
    
    # Add console handler with custom format
    logger.add(
        sys.stdout,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler for errors
    logger.add(
        "logs/error.log",
        format=settings.LOG_FORMAT,
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler for all logs
    logger.add(
        "logs/app.log",
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        rotation="50 MB",
        retention="7 days",
        compression="zip"
    )
    
    logger.info(f"Logging configured - Level: {settings.LOG_LEVEL}")
    
    return logger

# Made with Bob
