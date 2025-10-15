"""
Application logging utility for Unwritten.

Provides structured logging with categories for better debugging and monitoring.
"""

import time
from datetime import datetime
from typing import Optional, Dict, Any

# Check if we're in debug mode (would be set via environment variable in production)
import os
DEBUG_MODE = os.getenv('UNWRITTEN_DEBUG', 'true').lower() == 'true'


class AppLogger:
    """Structured logging utility for Unwritten training pipeline"""
    
    @staticmethod
    def _format_data(data: Optional[Dict[str, Any]] = None) -> str:
        """Format data dictionary for logging"""
        if not data:
            return ""
        return f"- {data}"
    
    @staticmethod
    def info(message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log informational message.
        
        Args:
            message: Log message
            data: Optional structured data
        """
        if DEBUG_MODE:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[INFO] [{timestamp}] {message} {AppLogger._format_data(data)}')
    
    @staticmethod
    def performance(operation: str, duration: float, 
                   data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log performance metric.
        
        Args:
            operation: Operation being measured
            duration: Duration in seconds
            data: Optional additional metrics
        """
        duration_ms = duration * 1000
        if DEBUG_MODE and duration_ms > 16:  # Flag operations > 16ms
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            metric_data = {'duration_ms': f'{duration_ms:.1f}'}
            if data:
                metric_data.update(data)
            print(f'[PERF] [{timestamp}] {operation} {AppLogger._format_data(metric_data)}')
    
    @staticmethod
    def ai(event: str, metrics: Optional[Dict[str, Any]] = None) -> None:
        """
        Log AI/ML specific events.
        
        Args:
            event: AI event description
            metrics: Optional AI metrics
        """
        if DEBUG_MODE:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[AI] [{timestamp}] {event} {AppLogger._format_data(metrics)}')
    
    @staticmethod
    def error(message: str, error: Exception, 
             data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log error with stack trace.
        
        Args:
            message: Error message
            error: Exception object
            data: Optional additional context
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f'[ERROR] [{timestamp}] {message} - {error} {AppLogger._format_data(data)}')
        if DEBUG_MODE:
            import traceback
            traceback.print_exc()
    
    @staticmethod
    def success(message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log success message.
        
        Args:
            message: Success message
            data: Optional structured data
        """
        if DEBUG_MODE:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[SUCCESS] [{timestamp}] {message} {AppLogger._format_data(data)}')
    
    @staticmethod
    def warning(message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Log warning message.
        
        Args:
            message: Warning message
            data: Optional structured data
        """
        if DEBUG_MODE:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[WARNING] [{timestamp}] {message} {AppLogger._format_data(data)}')

