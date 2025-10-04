#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures for MetasploitMCP tests.
"""

import pytest
import sys
import os
from unittest.mock import patch

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Dummy classes for external dependencies
    class Dummy:
        def __init__(self, *args, **kwargs):
            pass
    dummy_modules = [
        'uvicorn',
        'fastapi',
        'mcp.server.fastmcp',
        'mcp.server.sse',
        'pymetasploit3.msfrpc',
        'starlette.applications',
        'starlette.routing',
        'mcp.server.session'
    ]
    for module in dummy_modules:
        if module not in sys.modules:
            sys.modules[module] = Dummy()

def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add unit marker to test_options_parsing and test_helpers
        if "test_options_parsing" in item.nodeid or "test_helpers" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        
        # Add integration marker to integration tests
        if "test_tools_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Mark network tests
        if "network" in item.name.lower():
            item.add_marker(pytest.mark.network)
        
        # Mark slow tests
        if any(keyword in item.name.lower() for keyword in ["slow", "timeout", "long"]):
            item.add_marker(pytest.mark.slow)

@pytest.fixture(scope="session")
def mock_msf_environment():
    """Session-scoped fixture that provides a complete mock MSF environment."""
    
    class Modules:
        def __init__(self):
            self.exploits = []
            self.payloads = []
    class Core:
        def __init__(self):
            self.version = {'version': '6.3.0'}
    class Sessions:
        def __init__(self):
            self._list = {}
        def list(self):
            return self._list
    class Jobs:
        def __init__(self):
            self._list = {}
        def list(self):
            return self._list
    class Consoles:
        def __init__(self):
            pass
    class MockMsfRpcClient:
        def __init__(self):
            self.modules = Modules()
            self.core = Core()
            self.sessions = Sessions()
            self.jobs = Jobs()
            self.consoles = Consoles()
    
    class MockMsfConsole:
        def __init__(self, cid='test-console'):
            self.cid = cid
            
        def read(self):
            return {'data': '', 'prompt': 'msf6 > ', 'busy': False}
            
        def write(self, command):
            return True
    
    class MockMsfRpcError(Exception):
        pass
    
    # Apply dummy module
    class DummyMsfrpc:
        MsfRpcClient = MockMsfRpcClient
        MsfConsole = MockMsfConsole
        MsfRpcError = MockMsfRpcError
    with patch.dict('sys.modules', {'pymetasploit3.msfrpc': DummyMsfrpc}):
        yield {
            'client_class': MockMsfRpcClient,
            'console_class': MockMsfConsole,
            'error_class': MockMsfRpcError
        }

@pytest.fixture
def mock_logger():
    """Fixture providing a mock logger."""
    with patch('MetasploitMCP.logger') as mock_log:
        yield mock_log

@pytest.fixture 
def temp_payload_dir(tmp_path):
    """Fixture providing a temporary directory for payload saves."""
    payload_dir = tmp_path / "payloads"
    payload_dir.mkdir()
    
    with patch('MetasploitMCP.PAYLOAD_SAVE_DIR', str(payload_dir)):
        yield str(payload_dir)

@pytest.fixture
def mock_asyncio_to_thread():
    """Fixture to mock asyncio.to_thread for testing."""
    async def mock_to_thread(func, *args, **kwargs):
        return func(*args, **kwargs)
    
    with patch('asyncio.to_thread', side_effect=mock_to_thread):
        yield

@pytest.fixture
def capture_logs(caplog):
    """Fixture to capture and provide log output."""
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog

# Command line options
def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--run-slow", 
        action="store_true", 
        default=False, 
        help="Run slow tests"
    )
    parser.addoption(
        "--run-network",
        action="store_true",
        default=False,
        help="Run tests that require network access"
    )

def pytest_runtest_setup(item):
    """Setup hook to skip tests based on markers and options."""
    if "slow" in item.keywords and not item.config.getoption("--run-slow"):
        pytest.skip("Skipping slow test (use --run-slow to run)")
    
    if "network" in item.keywords and not item.config.getoption("--run-network"):
        pytest.skip("Skipping network test (use --run-network to run)")

# Test environment setup
@pytest.fixture(autouse=True)
def reset_msf_client():
    """Automatically reset the global MSF client between tests."""
    with patch('MetasploitMCP._msf_client_instance', None):
        yield
