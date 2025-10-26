"""
Pytest configuration and shared fixtures.

This module contains pytest configuration and fixtures that are
shared across all test modules.
"""

import pytest
import logging
from unittest.mock import Mock


@pytest.fixture(scope="session")
def logger():
    """Provide a logger instance for tests."""
    test_logger = logging.getLogger("test_logger")
    test_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    test_logger.addHandler(handler)
    return test_logger


@pytest.fixture(scope="function")
def mock_database():
    """Provide a mock database connection."""
    db = Mock()
    db.connect.return_value = True
    db.disconnect.return_value = True
    db.query.return_value = []
    return db


@pytest.fixture(scope="function")
def sample_config():
    """Provide sample configuration for tests."""
    return {
        "app_name": "test_application",
        "version": "1.0.0",
        "debug": True,
        "log_level": "DEBUG",
        "max_connections": 10
    }


@pytest.fixture(autouse=True)
def reset_state():
    """Reset application state before each test."""
    yield
    pass
