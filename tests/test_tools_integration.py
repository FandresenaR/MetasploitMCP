#!/usr/bin/env python3
"""
Integration tests for MCP tools in MetasploitMCP.
These tests mock the Metasploit backend but test the full tool workflows.
"""

import pytest
import sys
import os
import asyncio
from unittest.mock import patch
from types import SimpleNamespace
from typing import Dict, Any

# Add the parent directory to the path to import MetasploitMCP
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Mock the dependencies that aren't available in test environment

# Use pure Python dummy classes instead of Mock for modules accessed synchronously
class DummyUvicorn:
    def __init__(self, *args, **kwargs):
        pass
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
sys.modules['uvicorn'] = DummyUvicorn()
sys.modules['fastapi'] = DummyFastAPI()
sys.modules['starlette.applications'] = DummyStarletteApplications()
sys.modules['starlette.routing'] = DummyStarletteRouting()

# Create a special mock for FastMCP that preserves the tool decorator behavior
class MockFastMCP:
    def __init__(self, *args, **kwargs):
        pass
    
    def tool(self):
        # Return a decorator that just returns the original function
        def decorator(func):
            return func
        return decorator

# Mock the MCP modules with our custom FastMCP
class DummyFastMcpModule:
    class FastMCP:
        def __init__(self, *args, **kwargs):
            pass
        def tool(self):
            def decorator(func):
                return func
            return decorator
sys.modules['mcp.server.fastmcp'] = DummyFastMcpModule()
class DummySse:
    class SseServerTransport:
        def __init__(self, *args, **kwargs):
            pass
sys.modules['mcp.server.sse'] = DummySse()
class DummySession:
    class ServerSession:
        def __init__(self, *args, **kwargs):
            pass
        @staticmethod
        def _received_request(*args, **kwargs):
            pass
sys.modules['mcp.server.session'] = DummySession()
sys.modules['mcp.server.sse'] = DummySse()
sys.modules['mcp.server.session'] = DummySession()

# Mock pymetasploit3 module
class DummyMsfrpc:
    pass
sys.modules['pymetasploit3.msfrpc'] = DummyMsfrpc()

# Create comprehensive mock classes
class MockMsfRpcClient:
    def __init__(self):
        class Core:
            def __init__(self):
                self.version = {'version': '6.3.0'}
        class Modules:
            def __init__(self):
                self.exploits = ['windows/smb/ms17_010_eternalblue', 'unix/ftp/vsftpd_234_backdoor']
                self.payloads = ['windows/meterpreter/reverse_tcp', 'linux/x86/shell/reverse_tcp']
        class Sessions:
            def __init__(self):
                self._list = {}
                self._side_effects = []
            def list(self):
                if self._side_effects:
                    return self._side_effects.pop(0)
                return self._list
            def session(self, session_id):
                return None
        class Jobs:
            def __init__(self):
                self._list = {}
                self._side_effects = []
                self._stop_called = []
            def list(self):
                if self._side_effects:
                    return self._side_effects.pop(0)
                return self._list
            def stop(self, job_id):
                self._stop_called.append(job_id)
                return "stopped"
        class Consoles:
            def __init__(self):
                self._consoles = {}
            def list(self):
                return self._consoles
        self.core = Core()
        self.modules = Modules()
        self.sessions = Sessions()
        self.jobs = Jobs()
        self.consoles = Consoles()

# Top-level mock module class
class MockMsfModule:
    def __init__(self, fullname):
        self.fullname = fullname
        self.options = {}
        self.runoptions = {}
        self.missing_required = []
    def __setitem__(self, key, value):
        self.options[key] = value
    def execute(self, payload=None):
        return {
            'job_id': 1234,
            'uuid': 'test-uuid-123',
            'error': False
        }
    def payload_generate(self):
        return b"test_payload_bytes"

# Top-level mock console class
class MockMsfConsole:
    def __init__(self, cid='test-console-id'):
        self.cid = cid
        self._command_history = []
    def read(self):
        return {'data': 'msf6 > ', 'prompt': '\x01\x02msf6\x01\x02 \x01\x02> \x01\x02', 'busy': False}
    def write(self, command):
        self._command_history.append(command.strip())
        return True

class MockMsfRpcError(Exception):
    pass

# Apply mocks
sys.modules['pymetasploit3.msfrpc'].MsfRpcClient = MockMsfRpcClient
sys.modules['pymetasploit3.msfrpc'].MsfConsole = MockMsfConsole  
sys.modules['pymetasploit3.msfrpc'].MsfRpcError = MockMsfRpcError

# Import the module and then get the actual functions
import MetasploitMCP

# Get the actual functions (not mocked)
list_exploits = MetasploitMCP.list_exploits
list_payloads = MetasploitMCP.list_payloads
generate_payload = MetasploitMCP.generate_payload
run_exploit = MetasploitMCP.run_exploit
run_post_module = MetasploitMCP.run_post_module
run_auxiliary_module = MetasploitMCP.run_auxiliary_module
list_active_sessions = MetasploitMCP.list_active_sessions
send_session_command = MetasploitMCP.send_session_command
start_listener = MetasploitMCP.start_listener
stop_job = MetasploitMCP.stop_job
terminate_session = MetasploitMCP.terminate_session


class TestExploitListingTools:
    """Test tools for listing exploits and payloads."""

    @pytest.fixture
    def mock_client(self):
        """Fixture providing a mock MSF client."""
        client = MockMsfRpcClient()
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            yield client

    @pytest.mark.asyncio
    async def test_list_exploits_no_filter(self, mock_client):
        """Test listing exploits without filter."""
        class Modules:
            exploits = [
                'windows/smb/ms17_010_eternalblue',
                'unix/ftp/vsftpd_234_backdoor',
                'windows/http/iis_webdav_upload_asp'
            ]
            payloads = mock_client.modules.payloads
        mock_client.modules = Modules()
        result = await list_exploits()
        assert isinstance(result, list)
        assert len(result) == 3
        assert 'windows/smb/ms17_010_eternalblue' in result

    @pytest.mark.asyncio
    async def test_list_exploits_with_filter(self, mock_client):
        """Test listing exploits with search term."""
        class Modules:
            exploits = [
                'windows/smb/ms17_010_eternalblue',
                'unix/ftp/vsftpd_234_backdoor',
                'windows/smb/ms08_067_netapi'
            ]
            payloads = mock_client.modules.payloads
        mock_client.modules = Modules()
        result = await list_exploits("smb")
        assert isinstance(result, list)
        assert len(result) == 2
        assert all('smb' in exploit.lower() for exploit in result)

    @pytest.mark.asyncio
    async def test_list_exploits_error(self, mock_client):
        """Test listing exploits with MSF error."""
        class ExploitError:
            @property
            def exploits(self):
                raise MockMsfRpcError("Connection failed")
            payloads = mock_client.modules.payloads
        mock_client.modules = ExploitError()
        result = await list_exploits()
        assert isinstance(result, list)
        assert len(result) == 1
        assert "Error" in result[0]

    @pytest.mark.asyncio
    async def test_list_exploits_timeout(self, mock_client):
        """Test listing exploits with timeout."""
        import time
        class SlowExploits:
            @property
            def exploits(self):
                time.sleep(35)
                return ['exploit1', 'exploit2']
            payloads = mock_client.modules.payloads
        mock_client.modules = SlowExploits()
        result = await list_exploits()
        assert isinstance(result, list)
        assert len(result) == 1
        assert "Timeout" in result[0]
        assert "30" in result[0]  # Should mention the timeout duration

    @pytest.mark.asyncio
    async def test_list_payloads_no_filter(self, mock_client):
        """Test listing payloads without filter."""
        class Modules:
            exploits = mock_client.modules.exploits
            payloads = [
                'windows/meterpreter/reverse_tcp',
                'linux/x86/shell/reverse_tcp',
                'windows/shell/reverse_tcp'
            ]
        mock_client.modules = Modules()
        result = await list_payloads()
        assert isinstance(result, list)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_list_payloads_with_platform_filter(self, mock_client):
        """Test listing payloads with platform filter."""
        class Modules:
            exploits = mock_client.modules.exploits
            payloads = [
                'windows/meterpreter/reverse_tcp',
                'linux/x86/shell/reverse_tcp',
                'windows/shell/reverse_tcp'
            ]
        mock_client.modules = Modules()
        result = await list_payloads(platform="windows")
        assert isinstance(result, list)
        assert len(result) == 2
        assert all('windows' in payload.lower() for payload in result)

    @pytest.mark.asyncio
    async def test_list_payloads_with_arch_filter(self, mock_client):
        """Test listing payloads with architecture filter."""
        class Modules:
            exploits = mock_client.modules.exploits
            payloads = [
                'windows/meterpreter/reverse_tcp',
                'linux/x86/shell/reverse_tcp',
                'windows/x64/meterpreter/reverse_tcp'
            ]
        mock_client.modules = Modules()
        result = await list_payloads(arch="x86")
        assert isinstance(result, list)
        assert len(result) == 1
        assert 'x86' in result[0]


class TestPayloadGeneration:
    """Test payload generation functionality."""

    @pytest.fixture
    def mock_client_and_module(self):
        """Fixture providing mocked client and module."""
        client = MockMsfRpcClient()
        module = MockMsfModule('payload/windows/meterpreter/reverse_tcp')
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            with patch('MetasploitMCP._get_module_object', return_value=module):
                with patch('MetasploitMCP.PAYLOAD_SAVE_DIR', '/tmp/test'):
                    with patch('os.makedirs'):
                        class DummyFile:
                            def write(self, data):
                                pass
                            def __enter__(self):
                                return self
                            def __exit__(self, exc_type, exc_val, exc_tb):
                                pass
                        with patch('builtins.open', create=True, side_effect=lambda *a, **kw: DummyFile()):
                            yield client, module

    @pytest.mark.asyncio
    async def test_generate_payload_dict_options(self, mock_client_and_module):
        """Test payload generation with dictionary options."""
        client, module = mock_client_and_module
        
        options = {"LHOST": "192.168.1.100", "LPORT": 4444}
        result = await generate_payload(
            payload_type="windows/meterpreter/reverse_tcp",
            format_type="exe",
            options=options
        )
        
        assert result["status"] == "success"
        assert "server_save_path" in result
        assert result["payload_size"] == len(b"test_payload_bytes")

    @pytest.mark.asyncio
    async def test_generate_payload_string_options(self, mock_client_and_module):
        """Test payload generation with string options."""
        client, module = mock_client_and_module
        
        options = "LHOST=192.168.1.100,LPORT=4444"
        result = await generate_payload(
            payload_type="windows/meterpreter/reverse_tcp",
            format_type="exe",
            options=options
        )
        
        assert result["status"] == "success"
        # Verify the options were parsed correctly
        assert module.options["LHOST"] == "192.168.1.100"
        assert module.options["LPORT"] == 4444

    @pytest.mark.asyncio
    async def test_generate_payload_empty_options(self, mock_client_and_module):
        """Test payload generation with empty options."""
        client, module = mock_client_and_module
        
        result = await generate_payload(
            payload_type="windows/meterpreter/reverse_tcp",
            format_type="exe",
            options={}
        )
        
        assert result["status"] == "error"
        assert "required" in result["message"]

    @pytest.mark.asyncio
    async def test_generate_payload_invalid_string_options(self, mock_client_and_module):
        """Test payload generation with invalid string options."""
        client, module = mock_client_and_module
        
        result = await generate_payload(
            payload_type="windows/meterpreter/reverse_tcp",
            format_type="exe",
            options="LHOST192.168.1.100"  # Missing equals
        )
        
        assert result["status"] == "error"
        assert "Invalid options format" in result["message"]


class TestExploitExecution:
    @pytest.fixture
    def mock_exploit_environment(self):
        """Fixture providing mocked exploit environment with pure Python classes."""
        class DummyConsole:
            def __init__(self):
                self._called = False
            async def __call__(self, *args, **kwargs):
                self._called = True
                return {
                    "status": "success",
                    "message": "Exploit completed",
                    "module_output": "session opened"
                }
            def assert_called_once(self):
                assert self._called, "Console was not called"
            def assert_not_called(self):
                assert not self._called, "Console was called but shouldn't be"
        class DummyRpc:
            def __init__(self):
                self._called = False
                self.call_args = None
            async def __call__(self, *args, **kwargs):
                self._called = True
                self.call_args = (args, kwargs)
                return {
                    "status": "success",
                    "job_id": 1234,
                    "message": "Listener started"
                }
            def assert_called_once(self):
                assert self._called, "RPC was not called"
            def assert_not_called(self):
                assert not self._called, "RPC was called but shouldn't be"
        class DummyJobs:
            def __init__(self):
                self._jobs = {}
                self._stop_calls = []
            def list(self):
                return self._jobs
            def stop(self, job_id):
                self._stop_calls.append(job_id)
                return "stopped"
        class DummyModules:
            def __init__(self):
                self.exploits = [
                    'windows/smb/ms17_010_eternalblue',
                    'unix/ftp/vsftpd_234_backdoor',
                    'windows/http/iis_webdav_upload_asp'
                ]
                self.payloads = [
                    'windows/meterpreter/reverse_tcp',
                    'linux/x86/shell/reverse_tcp',
                    'windows/shell/reverse_tcp'
                ]
        class DummyMsfConsole:
            def __init__(self):
                self.cid = 'test-console-id'
            def read(self):
                return {'data': 'msf6 > ', 'prompt': 'msf6 > ', 'busy': False}
            def write(self, cmd):
                return True
        class DummyConsoles:
            def console(self):
                return DummyMsfConsole()
        class DummyClient:
            def __init__(self):
                self.modules = DummyModules()
                self.jobs = DummyJobs()
                self.consoles = DummyConsoles()
        client = DummyClient()
        mock_rpc = DummyRpc()
        mock_console = DummyConsole()
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            with patch('MetasploitMCP._execute_module_rpc', mock_rpc):
                with patch('MetasploitMCP._execute_module_console', mock_console):
                    yield client, mock_rpc, mock_console
    """Test exploit execution functionality."""

    @pytest.fixture
    def mock_job_environment(self):
        """Fixture providing mocked job management environment."""
        client = MockMsfRpcClient()
        class Jobs:
            def __init__(self):
                self._jobs = {}
                self._stop_calls = []
            def list(self):
                return self._jobs
            def stop(self, job_id):
                self._stop_calls.append(job_id)
                return "stopped"
        jobs = Jobs()
        client.jobs = jobs
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            with patch('MetasploitMCP._execute_module_rpc') as mock_rpc:
                mock_rpc.return_value = {
                    "status": "success",
                    "job_id": 1234,
                    "message": "Listener started"
                }
                # Provide a dummy mock_console for tests that expect it
                class DummyConsole:
                    def __init__(self):
                        self._called = False
                    def __call__(self, *args, **kwargs):
                        self._called = True
                    def assert_called_once(self):
                        assert self._called, "Console was not called"
                mock_console = DummyConsole()
                yield client, mock_rpc, mock_console

    @pytest.mark.asyncio
    async def test_run_exploit_dict_payload_options(self, mock_exploit_environment):
        """Test exploit execution with dictionary payload options."""
        client, mock_rpc, mock_console = mock_exploit_environment
        
        result = await run_exploit(
            module_name="windows/smb/ms17_010_eternalblue",
            options={"RHOSTS": "192.168.1.1"},
            payload_name="windows/meterpreter/reverse_tcp",
            payload_options={"LHOST": "192.168.1.100", "LPORT": 4444},
            run_as_job=True
        )
        
        assert result["status"] == "success"
        mock_rpc.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_exploit_string_payload_options(self, mock_exploit_environment):
        """Test exploit execution with string payload options."""
        client, mock_rpc, mock_console = mock_exploit_environment
        
        result = await run_exploit(
            module_name="windows/smb/ms17_010_eternalblue",
            options={"RHOSTS": "192.168.1.1"},
            payload_name="windows/meterpreter/reverse_tcp",
            payload_options="LHOST=192.168.1.100,LPORT=4444",
            run_as_job=True
        )
        
        assert result["status"] == "success"
        # Verify RPC was called with parsed options
        call_args = mock_rpc.call_args
        payload_spec = call_args[1]['payload_spec']
        assert payload_spec['options']['LHOST'] == "192.168.1.100"
        assert payload_spec['options']['LPORT'] == 4444

    @pytest.mark.asyncio
    async def test_run_exploit_invalid_payload_options(self, mock_exploit_environment):
        """Test exploit execution with invalid payload options."""
        client, mock_rpc, mock_console = mock_exploit_environment
        
        result = await run_exploit(
            module_name="windows/smb/ms17_010_eternalblue",
            options={"RHOSTS": "192.168.1.1"},
            payload_name="windows/meterpreter/reverse_tcp",
            payload_options="LHOST192.168.1.100",  # Invalid format
            run_as_job=True
        )
        
        assert result["status"] == "error"
        assert "Invalid payload_options format" in result["message"]

    @pytest.mark.asyncio
    async def test_run_exploit_console_mode(self, mock_exploit_environment):
        """Test exploit execution in console mode."""
        client, mock_rpc, mock_console = mock_exploit_environment
        
        result = await run_exploit(
            module_name="windows/smb/ms17_010_eternalblue",
            options={"RHOSTS": "192.168.1.1"},
            payload_name="windows/meterpreter/reverse_tcp",
            payload_options={"LHOST": "192.168.1.100", "LPORT": 4444},
            run_as_job=False  # Console mode
        )
        
        assert result["status"] == "success"
        mock_console.assert_called_once()
        mock_rpc.assert_not_called()


class TestSessionManagement:
    """Test session management functionality."""

    @pytest.fixture
    def mock_session_environment(self):
        """Fixture providing mocked session management environment."""
        client = MockMsfRpcClient()
        class DummySession:
            def __init__(self):
                self._output = "command output"
                self._data = "session data"
                self._write_called = False
                self._stop_called = False
            def run_with_output(self, cmd):
                self._run_with_output_called = cmd
                return self._output
            def read(self):
                return self._data
            def write(self, data):
                self._write_called = True
            def stop(self):
                self._stop_called = True
            def assert_called_once_with(self, cmd):
                assert getattr(self, '_run_with_output_called', None) == cmd, f"run_with_output not called with {cmd}"
            def assert_called_once(self):
                assert self._stop_called, "stop was not called"
        session = DummySession()
        class DummySessions:
            def __init__(self, session):
                self._session = session
                self._list = {
                    "1": {"type": "meterpreter", "info": "Windows session"},
                    "2": {"type": "shell", "info": "Linux session"}
                }
                self._side_effects = []
            def list(self):
                if self._side_effects:
                    return self._side_effects.pop(0)
                return self._list
            def session(self, session_id):
                return self._session
        dummy_sessions = DummySessions(session)
        client.sessions = dummy_sessions
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            yield client, session

    @pytest.mark.asyncio
    async def test_list_active_sessions(self, mock_session_environment):
        """Test listing active sessions."""
        client, session = mock_session_environment
        
        result = await list_active_sessions()
        
        assert result["status"] == "success"
        assert result["count"] == 2
        assert "1" in result["sessions"]
        assert "2" in result["sessions"]

    @pytest.mark.asyncio
    async def test_send_session_command_meterpreter(self, mock_session_environment):
        """Test sending command to Meterpreter session."""
        client, session = mock_session_environment
        
        result = await send_session_command(1, "sysinfo")
        
        assert result["status"] == "success"
        session.assert_called_once_with("sysinfo")

    @pytest.mark.asyncio
    async def test_send_session_command_nonexistent(self, mock_session_environment):
        """Test sending command to non-existent session."""
        client, session = mock_session_environment
        client.sessions._list = {}  # No sessions
        result = await send_session_command(999, "whoami")
        assert result["status"] == "error"
        assert "not found" in result["message"]

    @pytest.mark.asyncio
    async def test_terminate_session(self, mock_session_environment):
        """Test session termination."""
        client, session = mock_session_environment
        
        # Mock session disappearing after termination
        client.sessions._side_effects = [
            {"1": {"type": "meterpreter"}},  # Before termination
            {}  # After termination
        ]
        result = await terminate_session(1)
        assert result["status"] == "success"
        session.assert_called_once()


class TestListenerManagement:
    """Test listener and job management functionality."""

    @pytest.fixture
    def mock_job_environment(self):
        """Fixture providing mocked job management environment."""
        client = MockMsfRpcClient()
        
        class DummyJobs:
            def __init__(self):
                self._jobs = {}
                self._stop_called = []
                self._list_side_effects = []
            def list(self):
                if self._list_side_effects:
                    return self._list_side_effects.pop(0)
                return self._jobs
            def stop(self, job_id):
                self._stop_called.append(job_id)
                return "stopped"
            def assert_called_once_with(self, job_id):
                assert self._stop_called == [job_id], f"stop not called with {job_id}"
        jobs = DummyJobs()
        client.jobs = jobs
        with patch('MetasploitMCP.get_msf_client', return_value=client):
            with patch('MetasploitMCP._execute_module_rpc') as mock_rpc:
                mock_rpc.return_value = {
                    "status": "success",
                    "job_id": 1234,
                    "message": "Listener started"
                }
                yield client, mock_rpc

    @pytest.mark.asyncio
    async def test_start_listener_dict_options(self, mock_job_environment):
        """Test starting listener with dictionary additional options."""
        client, mock_rpc = mock_job_environment
        
        result = await start_listener(
            payload_type="windows/meterpreter/reverse_tcp",
            lhost="192.168.1.100",
            lport=4444,
            additional_options={"ExitOnSession": True}
        )
        
        assert result["status"] == "success"
        assert "job" in result["message"]

    @pytest.mark.asyncio
    async def test_start_listener_string_options(self, mock_job_environment):
        """Test starting listener with string additional options."""
        client, mock_rpc = mock_job_environment
        
        result = await start_listener(
            payload_type="windows/meterpreter/reverse_tcp",
            lhost="192.168.1.100", 
            lport=4444,
            additional_options="ExitOnSession=true,Verbose=false"
        )
        
        assert result["status"] == "success"
        # Verify RPC was called with parsed options
        call_args = mock_rpc.call_args
        payload_spec = call_args[1]['payload_spec']
        assert payload_spec['options']['ExitOnSession'] is True
        assert payload_spec['options']['Verbose'] is False

    @pytest.mark.asyncio
    async def test_start_listener_invalid_port(self, mock_job_environment):
        """Test starting listener with invalid port."""
        client, mock_rpc = mock_job_environment
        
        result = await start_listener(
            payload_type="windows/meterpreter/reverse_tcp",
            lhost="192.168.1.100",
            lport=99999  # Invalid port
        )
        
        assert result["status"] == "error"
        assert "Invalid LPORT" in result["message"]

    @pytest.mark.asyncio
    async def test_stop_job(self, mock_job_environment):
        """Test stopping a job."""
        client, mock_rpc = mock_job_environment
        
        # Mock job exists before stop, gone after stop
        client.jobs._list_side_effects = [
            {"1234": {"name": "Handler Job"}},  # Before stop
            {}  # After stop  
        ]
        result = await stop_job(1234)
        assert result["status"] == "success"
        assert client.jobs._stop_called == ["1234"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
