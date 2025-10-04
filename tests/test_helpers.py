#!/usr/bin/env python3
"""
Unit tests for helper functions in MetasploitMCP.
"""

import pytest
import sys
import os
import asyncio
from unittest.mock import patch
from typing import Dict, Any

# Add the parent directory to the path to import MetasploitMCP
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# Use pure Python dummy classes for all sys.modules mocks
class DummyUvicorn: pass
class DummyFastAPI:
    class FastAPI:
        def __init__(self, *args, **kwargs):
            self.routes = []
        def get(self, *args, **kwargs):
            def decorator(func):
                return func
            return decorator
    class HTTPException(Exception):
        pass
    class Request:
        pass
    class Response:
        pass
sys.modules['fastapi'] = DummyFastAPI()
class DummyFastMcp:
    class FastMCP:
        def __init__(self, *args, **kwargs):
            pass
        def tool(self):
            def decorator(func):
                return func
            return decorator
sys.modules['mcp.server.fastmcp'] = DummyFastMcp()
class DummySse:
    class SseServerTransport:
        def __init__(self, *args, **kwargs):
            pass
sys.modules['mcp.server.sse'] = DummySse()
class DummyMsfrpc: pass
class DummyStarletteApplications:
    class Starlette:
        def __init__(self, *args, **kwargs):
            pass
sys.modules['starlette.applications'] = DummyStarletteApplications()
class DummyStarletteRouting:
    class Mount:
        def __init__(self, *args, **kwargs):
            pass
    class Route:
        def __init__(self, *args, **kwargs):
            pass
    class Router:
        def __init__(self, *args, **kwargs):
            pass
sys.modules['starlette.routing'] = DummyStarletteRouting()
class DummySession:
    class ServerSession:
        def __init__(self, *args, **kwargs):
            pass
        @staticmethod
        def _received_request(*args, **kwargs):
            pass
sys.modules['mcp.server.session'] = DummySession()
sys.modules['uvicorn'] = DummyUvicorn()
sys.modules['fastapi'] = DummyFastAPI()
sys.modules['mcp.server.fastmcp'] = DummyFastMcp()
sys.modules['mcp.server.sse'] = DummySse()
sys.modules['pymetasploit3.msfrpc'] = DummyMsfrpc()
sys.modules['starlette.applications'] = DummyStarletteApplications()
sys.modules['starlette.routing'] = DummyStarletteRouting()
sys.modules['mcp.server.session'] = DummySession()

# Create mock classes for MSF objects
class Modules:
    pass
class Core:
    pass
class Sessions:
    pass
class Jobs:
    pass
class Consoles:
    pass
class MockMsfRpcClient:
    def __init__(self):
        self.modules = Modules()
        self.core = Core()
        self.sessions = Sessions()
        self.jobs = Jobs()
        self.consoles = Consoles()

class MockMsfConsole:
    def __init__(self, cid='test-console-id'):
        self.cid = cid
        
    def read(self):
        return {'data': 'test output', 'prompt': 'msf6 > ', 'busy': False}
        
    def write(self, command):
        return True

class MockMsfRpcError(Exception):
    pass

# Patch the MSF modules
sys.modules['pymetasploit3.msfrpc'].MsfRpcClient = MockMsfRpcClient
sys.modules['pymetasploit3.msfrpc'].MsfConsole = MockMsfConsole  
sys.modules['pymetasploit3.msfrpc'].MsfRpcError = MockMsfRpcError

# Import after mocking
from MetasploitMCP import (
    _get_module_object, _set_module_options, initialize_msf_client, 
    get_msf_client, get_msf_console, run_command_safely,
    find_available_port
)


class TestMsfClientFunctions:
    """Test MSF client initialization and management functions."""

    @patch('MetasploitMCP.MSF_PASSWORD', 'test-password')
    @patch('MetasploitMCP.MSF_SERVER', '127.0.0.1')
    @patch('MetasploitMCP.MSF_PORT_STR', '55553')
    @patch('MetasploitMCP.MSF_SSL_STR', 'false')
    def test_initialize_msf_client_success(self):
        """Test successful MSF client initialization."""
        with patch('MetasploitMCP._msf_client_instance', None):
            class DummyClient:
                def __init__(self):
                    class Core:
                        def __init__(self):
                            self.version = {'version': '6.3.0'}
                    self.core = Core()
            dummy_client = DummyClient()
            with patch('MetasploitMCP.MsfRpcClient', return_value=dummy_client) as mock_client_class:
                result = initialize_msf_client()
                assert result is dummy_client
                mock_client_class.assert_called_once_with(
                    password='test-password',
                    server='127.0.0.1',
                    port=55553,
                    ssl=False
                )

    @patch('MetasploitMCP.MSF_PORT_STR', 'invalid-port')
    def test_initialize_msf_client_invalid_port(self):
        """Test MSF client initialization with invalid port."""
        with patch('MetasploitMCP._msf_client_instance', None):
            with pytest.raises(ValueError, match="Invalid MSF connection parameters"):
                initialize_msf_client()

    def test_get_msf_client_not_initialized(self):
        """Test get_msf_client when client not initialized."""
        with patch('MetasploitMCP._msf_client_instance', None):
            with pytest.raises(ConnectionError, match="not been initialized"):
                get_msf_client()

    def test_get_msf_client_initialized(self):
        """Test get_msf_client when client is initialized."""
        class DummyClient:
            pass
        mock_client = DummyClient()
        with patch('MetasploitMCP._msf_client_instance', mock_client):
            result = get_msf_client()
            assert result is mock_client


class TestGetModuleObject:
    """Test the _get_module_object helper function."""

    @pytest.fixture
    def mock_client(self):
        """Fixture providing a dummy MSF client with nested modules.use and call tracking/side_effect support."""
        class DummyUse:
            def __init__(self):
                self._side_effect = None
                self._calls = []
                self._return_value = None
            def __call__(self, module_type, module_name):
                self._calls.append((module_type, module_name))
                if self._side_effect:
                    raise self._side_effect
                return self._return_value
            def set_side_effect(self, exc):
                self._side_effect = exc
            def set_return_value(self, val):
                self._return_value = val
            def assert_called_once_with(self, module_type, module_name):
                assert len(self._calls) == 1
                assert self._calls[0] == (module_type, module_name)
        class DummyModules:
            def __init__(self):
                self.use = DummyUse()
        class DummyClient:
            def __init__(self):
                self.modules = DummyModules()
        client = DummyClient()
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            yield client

    @pytest.mark.asyncio
    async def test_get_module_object_success(self, mock_client):
        """Test successful module object retrieval."""
        class DummyModule:
            pass
        mock_module = DummyModule()
        mock_client.modules.use.set_return_value(mock_module)
        result = await _get_module_object('exploit', 'windows/smb/ms17_010_eternalblue')
        assert result is mock_module
        mock_client.modules.use.assert_called_once_with('exploit', 'windows/smb/ms17_010_eternalblue')

    @pytest.mark.asyncio
    async def test_get_module_object_full_path(self, mock_client):
        """Test module object retrieval with full path."""
        class DummyModule:
            pass
        mock_module = DummyModule()
        mock_client.modules.use.set_return_value(mock_module)
        result = await _get_module_object('exploit', 'exploit/windows/smb/ms17_010_eternalblue')
        assert result is mock_module
        # Should strip the module type prefix
        mock_client.modules.use.assert_called_once_with('exploit', 'windows/smb/ms17_010_eternalblue')

    @pytest.mark.asyncio
    async def test_get_module_object_not_found(self, mock_client):
        """Test module object retrieval when module not found."""
        mock_client.modules.use.set_side_effect(KeyError("Module not found"))
        with pytest.raises(ValueError, match="not found"):
            await _get_module_object('exploit', 'nonexistent/module')

    @pytest.mark.asyncio
    async def test_get_module_object_msf_error(self, mock_client):
        """Test module object retrieval with MSF RPC error."""
        mock_client.modules.use.set_side_effect(MockMsfRpcError("RPC Error"))
        with pytest.raises(MockMsfRpcError, match="RPC Error"):
            await _get_module_object('exploit', 'test/module')


class TestSetModuleOptions:
    """Test the _set_module_options helper function."""

    @pytest.fixture
    def mock_module(self):
        """Fixture providing a dummy module object with call tracking and error simulation."""
        class DummySetItem:
            def __init__(self):
                self.calls = []
                self._side_effect = None
            def __call__(self, key, value):
                if self._side_effect:
                    raise self._side_effect
                self.calls.append((key, value))
            def set_side_effect(self, exc):
                self._side_effect = exc
            @property
            def call_count(self):
                return len(self.calls)
            def assert_any_call(self, key, value):
                assert (key, value) in self.calls
            @property
            def call_args_list(self):
                return [(k, v) for k, v in self.calls]
        class DummyModule:
            pass
        module = DummyModule()
        module.fullname = 'exploit/test/module'
        module.__setitem__ = DummySetItem()
        return module

    @pytest.mark.asyncio
    async def test_set_module_options_basic(self, mock_module):
        """Test basic option setting."""
        options = {'RHOSTS': '192.168.1.1', 'RPORT': '80'}
        await _set_module_options(mock_module, options)
        # Should be called twice, once for each option
        assert mock_module.__setitem__.call_count == 2
        mock_module.__setitem__.assert_any_call('RHOSTS', '192.168.1.1')
        mock_module.__setitem__.assert_any_call('RPORT', 80)  # Type conversion: '80' -> 80

    @pytest.mark.asyncio
    async def test_set_module_options_type_conversion(self, mock_module):
        """Test option setting with type conversion."""
        options = {
            'RPORT': '80',  # String number -> int
            'SSL': 'true',  # String boolean -> bool
            'VERBOSE': 'false',  # String boolean -> bool
            'THREADS': '10'  # String number -> int
        }
        await _set_module_options(mock_module, options)
        # Verify type conversions
        calls = mock_module.__setitem__.call_args_list
        call_dict = {calls[i][0]: calls[i][1] for i in range(len(calls))}
        assert call_dict['RPORT'] == 80
        assert call_dict['SSL'] is True
        assert call_dict['VERBOSE'] is False
        assert call_dict['THREADS'] == 10

    @pytest.mark.asyncio
    async def test_set_module_options_error(self, mock_module):
        """Test option setting with error."""
        mock_module.__setitem__.set_side_effect(KeyError("Invalid option"))
        options = {'INVALID_OPT': 'value'}
        with pytest.raises(ValueError, match="Failed to set option"):
            await _set_module_options(mock_module, options)


class TestGetMsfConsole:
    """Test the get_msf_console context manager."""

    @pytest.fixture
    def mock_client(self):
        """Fixture providing a dummy MSF client with consoles.console/destroy and call tracking/side_effect support."""
        class DummyConsoleMethod:
            def __init__(self):
                self._side_effect = None
                self._return_value = None
                self._calls = []
            def __call__(self, *args, **kwargs):
                self._calls.append((args, kwargs))
                if self._side_effect:
                    raise self._side_effect
                return self._return_value
            def set_side_effect(self, exc):
                self._side_effect = exc
            def set_return_value(self, val):
                self._return_value = val
            def assert_called_once_with(self, *args, **kwargs):
                assert len(self._calls) == 1
                assert self._calls[0] == (args, kwargs)
        class DummyConsoles:
            def __init__(self):
                self.console = DummyConsoleMethod()
                self.destroy = DummyConsoleMethod()
        class DummyClient:
            def __init__(self):
                self.consoles = DummyConsoles()
        client = DummyClient()
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            yield client

    @pytest.mark.asyncio
    async def test_get_msf_console_success(self, mock_client):
        """Test successful console creation and cleanup."""
        mock_console = MockMsfConsole('test-console-123')
        mock_client.consoles.console.set_return_value(mock_console)
        mock_client.consoles.destroy.set_return_value('destroyed')
        # Mock the global client instance for cleanup
        with patch('MetasploitMCP._msf_client_instance', mock_client):
            async with get_msf_console() as console:
                assert console is mock_console
                assert console.cid == 'test-console-123'
            # Verify cleanup was called
            # The destroy method should have been called once with the console id
            assert len(mock_client.consoles.destroy._calls) == 1
            assert mock_client.consoles.destroy._calls[0][0][0] == 'test-console-123'

    @pytest.mark.asyncio
    async def test_get_msf_console_creation_error(self, mock_client):
        """Test console creation error handling."""
        mock_client.consoles.console.set_side_effect(MockMsfRpcError("Console creation failed"))
        with pytest.raises(MockMsfRpcError, match="Console creation failed"):
            async with get_msf_console() as console:
                pass

    @pytest.mark.asyncio 
    async def test_get_msf_console_cleanup_error(self, mock_client):
        """Test that cleanup errors don't propagate."""
        mock_console = MockMsfConsole('test-console-123')
        mock_client.consoles.console.set_return_value(mock_console)
        mock_client.consoles.destroy.set_side_effect(Exception("Cleanup failed"))
        # Should not raise exception even if cleanup fails
        async with get_msf_console() as console:
            assert console is mock_console


class TestRunCommandSafely:
    """Test the run_command_safely function."""

    @pytest.fixture
    def mock_console(self):
        """Fixture providing a dummy console with call tracking and error simulation."""
        class DummyMethod:
            def __init__(self):
                self._side_effect = None
                self._return_value = None
                self._calls = []
            def __call__(self, *args, **kwargs):
                self._calls.append((args, kwargs))
                if self._side_effect:
                    raise self._side_effect
                return self._return_value
            def set_side_effect(self, exc):
                self._side_effect = exc
            def set_return_value(self, val):
                self._return_value = val
            def assert_called_once_with(self, *args, **kwargs):
                assert len(self._calls) == 1
                assert self._calls[0] == (args, kwargs)
        class DummyConsole:
            def __init__(self):
                self.write = DummyMethod()
                self.read = DummyMethod()
        return DummyConsole()

    @pytest.mark.asyncio
    async def test_run_command_safely_basic(self, mock_console):
        """Test basic command execution."""
        # Mock console read to return prompt immediately
        mock_console.read.set_return_value({
            'data': 'command output\n',
            'prompt': '\x01\x02msf6\x01\x02 \x01\x02> \x01\x02',
            'busy': False
        })
        result = await run_command_safely(mock_console, 'help')
        mock_console.write.assert_called_once_with('help\n')
        assert 'command output' in result

    @pytest.mark.asyncio
    async def test_run_command_safely_invalid_console(self, mock_console):
        """Test command execution with invalid console."""
        # Remove required methods
        delattr(mock_console, 'write')
        with pytest.raises(TypeError, match="Unsupported console object"):
            await run_command_safely(mock_console, 'help')

    @pytest.mark.asyncio
    async def test_run_command_safely_read_error(self, mock_console):
        """Test command execution with read error - should timeout gracefully."""
        mock_console.read.set_side_effect(Exception("Read failed"))
        # Should not raise exception, but timeout and return empty result
        result = await run_command_safely(mock_console, 'help')
        # Should return empty string after timeout
        assert isinstance(result, str)
        assert result == ""  # Empty result after timeout


class TestFindAvailablePort:
    """Test the find_available_port utility function."""

    def test_find_available_port_success(self):
        """Test finding an available port."""
        # This should succeed as it tests real socket binding
        port = find_available_port(8080, max_attempts=5)
        assert isinstance(port, int)
        assert 8080 <= port < 8085

    @patch('socket.socket')
    def test_find_available_port_all_busy(self, mock_socket_class):
        """Test when all ports in range are busy."""
        class DummySocket:
            def __init__(self):
                self._bind_side_effect = None
            def bind(self, *args, **kwargs):
                if self._bind_side_effect:
                    raise self._bind_side_effect
            def getsockname(self):
                return ('127.0.0.1', 12345)
            def close(self):
                pass
        mock_socket = DummySocket()
        mock_socket._bind_side_effect = OSError("Port in use")
        mock_socket_class.return_value.__enter__.return_value = mock_socket
        # Should return the start port as fallback
        port = find_available_port(8080, max_attempts=3)
        assert port == 8080

    @patch('socket.socket')
    def test_find_available_port_second_attempt(self, mock_socket_class):
        """Test finding port on second attempt."""
        class DummySocket:
            def __init__(self):
                self._bind_side_effects = [OSError("Port in use"), None]
                self._bind_call = 0
            def bind(self, *args, **kwargs):
                if self._bind_call < len(self._bind_side_effects):
                    effect = self._bind_side_effects[self._bind_call]
                    self._bind_call += 1
                    if effect:
                        raise effect
            def getsockname(self):
                return ('127.0.0.1', 12345)
            def close(self):
                pass
        mock_socket = DummySocket()
        mock_socket_class.return_value.__enter__.return_value = mock_socket
        port = find_available_port(8080, max_attempts=3)
        assert port == 8081


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
