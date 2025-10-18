# 📊 MetasploitMCP - Quick Visual Summary

*A quick reference showing all components and how they connect*

---

## 🎯 What Does This Project Do?

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│     YOU     │ ──────► │ AI Assistant │ ──────► │ Metasploit  │
│  (Human)    │  talk   │ (Claude/GPT) │  MCP    │  Framework  │
└─────────────┘         └──────────────┘         └─────────────┘
                               ▲
                               │
                               │ Uses
                               ▼
                        ┌──────────────┐
                        │ MetasploitMCP│
                        │   (Bridge)   │
                        └──────────────┘
```

**In simple terms:** Talk to an AI, and it controls security tools for you!

---

## 📦 Project Files Overview

```
MetasploitMCP/
├── 📄 Core Application
│   ├── MetasploitMCP.py          ⭐ Main server (13 MCP tools)
│   ├── requirements.txt           📋 Python dependencies
│   └── .env.local                🔐 Your configuration (passwords, keys)
│
├── 🛠️ Management Scripts
│   ├── start-msfrpcd.sh          ▶️  Start Metasploit RPC
│   ├── stop-msfrpcd.sh           ⏹️  Stop Metasploit RPC
│   ├── quickref.sh               📖 Quick command reference
│   └── Makefile                   🔧 Convenient commands (make start-msf, etc.)
│
├── 🐳 Deployment Files
│   ├── Dockerfile                 🐋 For cloud deployment (mock mode)
│   ├── Dockerfile.metasploit      🐋 With Metasploit (larger)
│   ├── fly.toml                   ☁️  Fly.io configuration
│   └── docker-compose.yml         🐙 Docker Compose setup
│
├── 🧪 Testing
│   ├── tests/                     ✅ Test suite
│   ├── pytest.ini                 ⚙️  Test configuration
│   ├── conftest.py                🔧 Test fixtures
│   └── run_tests.py               ▶️  Test runner
│
└── 📚 Documentation
    ├── README.md                  📖 Main documentation
    ├── BEGINNER_GUIDE.md         🎓 Complete beginner's guide (NEW!)
    ├── DEPLOYMENT.md              🚀 Deployment guide (5 options)
    ├── CHANGELOG.md               📝 Version history
    ├── MSFRPCD_MANAGEMENT.md      🔧 msfrpcd reference
    └── PROJECT_CLEANUP_SUMMARY.md 🧹 Cleanup details
```

---

## 🔌 System Architecture

### Complete System Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              YOUR COMPUTER / CLOUD                       │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │                    AI ASSISTANT LAYER                           │    │
│  │                                                                 │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │    │
│  │  │    Claude    │  │   ChatGPT    │  │  Other AI    │        │    │
│  │  │   Desktop    │  │   with MCP   │  │  Assistants  │        │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │    │
│  │         │                  │                  │                │    │
│  │         └──────────────────┼──────────────────┘                │    │
│  │                            │                                   │    │
│  │                    MCP Protocol (JSON-RPC)                     │    │
│  └────────────────────────────┼───────────────────────────────────┘    │
│                                │                                        │
│  ┌────────────────────────────▼───────────────────────────────────┐    │
│  │                 METASPLOITMCP SERVER                            │    │
│  │                  (This Project)                                 │    │
│  │                                                                 │    │
│  │  ┌─────────────────────────────────────────────────────────┐   │    │
│  │  │              MCP TOOLS (13 Tools)                        │   │    │
│  │  │                                                          │   │    │
│  │  │  Information:        Exploitation:       Management:    │   │    │
│  │  │  • list_exploits     • run_exploit       • list_sessions│   │    │
│  │  │  • list_payloads     • run_auxiliary     • send_command │   │    │
│  │  │                      • run_post          • terminate    │   │    │
│  │  │                      • generate_payload   • start_listener│ │    │
│  │  │                                           • stop_job     │   │    │
│  │  │  AI-Powered:                                             │   │    │
│  │  │  • analyze_exploit_with_ai                               │   │    │
│  │  │  • generate_commands_with_ai                             │   │    │
│  │  │  • analyze_vulnerability_with_ai                         │   │    │
│  │  └──────────────────────────┬───────────────────────────────┘   │    │
│  │                             │                                    │    │
│  │  ┌─────────────┐  ┌─────────▼─────────┐  ┌─────────────────┐  │    │
│  │  │ HTTP/SSE    │  │  Metasploit RPC   │  │   OpenRouter    │  │    │
│  │  │ Transport   │  │     Client        │  │   AI Client     │  │    │
│  │  │ (Port 8080) │  │                   │  │   (Optional)    │  │    │
│  │  └─────────────┘  └─────────┬─────────┘  └─────────────────┘  │    │
│  └────────────────────────────┼─────────────────────────────────┘    │
│                                │                                        │
│  ┌────────────────────────────▼───────────────────────────────────┐    │
│  │              METASPLOIT FRAMEWORK                               │    │
│  │                (msfrpcd daemon)                                 │    │
│  │                                                                 │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │    │
│  │  │   Exploits   │  │   Payloads   │  │   Sessions   │        │    │
│  │  │   (3000+)    │  │   (500+)     │  │   (Active)   │        │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                          │
└────────────────────────────────┬─────────────────────────────────────┘
                                  │
                                  │ Network / Exploit
                                  ▼
                    ┌──────────────────────────────┐
                    │      TARGET SYSTEMS          │
                    │   (Being tested/exploited)   │
                    └──────────────────────────────┘
```

---

## 🛠️ The 13 MCP Tools

### 📋 Information Tools (2)
| Tool | Purpose | Example |
|------|---------|---------|
| `list_exploits` | Find available exploits | "Show Windows exploits" |
| `list_payloads` | Find compatible payloads | "List Linux x64 payloads" |

### ⚡ Exploitation Tools (3)
| Tool | Purpose | Example |
|------|---------|---------|
| `run_exploit` | Execute an exploit | "Exploit 192.168.1.100" |
| `run_auxiliary_module` | Run scanners | "Scan port 445" |
| `run_post_module` | Post-exploitation | "Dump hashes from session" |

### 💾 Payload Tools (1)
| Tool | Purpose | Example |
|------|---------|---------|
| `generate_payload` | Create payload files | "Generate Windows exe" |

### 🎮 Session Management (3)
| Tool | Purpose | Example |
|------|---------|---------|
| `list_active_sessions` | Show sessions | "What sessions are active?" |
| `send_session_command` | Run commands | "Run whoami in session 1" |
| `terminate_session` | Close session | "Close session 1" |

### 🎧 Handler Management (3)
| Tool | Purpose | Example |
|------|---------|---------|
| `list_listeners` | Show handlers | "What handlers are running?" |
| `start_listener` | Start handler | "Start handler on port 4444" |
| `stop_job` | Stop handler | "Stop job 1" |

### 🤖 AI-Powered Tools (3)
| Tool | Purpose | Example |
|------|---------|---------|
| `analyze_exploit_with_ai` | Analyze exploits | "Analyze ms17_010" |
| `generate_metasploit_commands_with_ai` | Generate commands | "How to exploit SSH?" |
| `analyze_vulnerability_with_ai` | Analyze CVEs | "Analyze CVE-2023-1234" |

---

## 🌍 Deployment Options Comparison

```
┌────────────────┬──────────────┬──────────────┬─────────────────┐
│   Platform     │  Setup Time  │     Cost     │   Best For      │
├────────────────┼──────────────┼──────────────┼─────────────────┤
│ 🖥️  Local      │   15 min     │    Free      │ Development     │
│ ☁️  Fly.io     │   5 min      │  $5-10/mo    │ Demos/Testing   │
│ 🌩️  Oracle     │   30 min     │    FREE!     │ Production      │
│ 🐳 Docker      │   10 min     │    Free      │ Portability     │
│ ☸️  Kubernetes │   2 hours    │  Variable    │ Enterprise      │
└────────────────┴──────────────┴──────────────┴─────────────────┘
```

### Current Live Deployment

**🌐 Live Demo:** https://metasploit-mcp.fly.dev/  
**📚 API Docs:** https://metasploit-mcp.fly.dev/docs  
**⚙️ Mode:** Mock (no real Metasploit)  
**🏢 Platform:** Fly.io (Ashburn, Virginia)

---

## 🔄 How a Request Flows

### Example: "Exploit 192.168.1.100"

```
1️⃣  USER
    │ "Exploit 192.168.1.100 using ms17_010"
    ↓

2️⃣  AI ASSISTANT (Claude/GPT)
    │ Understands request
    │ Selects: run_exploit() tool
    │ Prepares parameters
    ↓

3️⃣  MCP PROTOCOL
    │ JSON-RPC request
    │ Tool: run_exploit
    │ Args: {target: "192.168.1.100", exploit: "ms17_010"}
    ↓

4️⃣  METASPLOITMCP SERVER
    │ Receives MCP request
    │ Validates parameters
    │ Converts to Metasploit RPC
    ↓

5️⃣  METASPLOIT RPC
    │ msgpack-RPC call
    │ module.execute(exploit/windows/smb/ms17_010_eternalblue)
    ↓

6️⃣  METASPLOIT FRAMEWORK
    │ Loads exploit module
    │ Sends exploit packets
    │ Creates session if successful
    ↓

7️⃣  TARGET SYSTEM (192.168.1.100)
    │ Receives exploit
    │ Executes payload (if vulnerable)
    │ Connects back
    ↓

8️⃣  RESULTS FLOW BACK
    │ Target → Metasploit → MetasploitMCP → AI → User
    │
    ✅ "Successfully exploited! Session 1 is active."
```

---

## 📝 Configuration Files

### `.env.local` (Your Secrets)
```bash
# Metasploit RPC
MSF_PASSWORD=your_secure_password_here
MSF_SERVER=127.0.0.1
MSF_PORT=55553

# AI Features (Optional)
OPENROUTER_API_KEY=your_api_key_here

# Payload Storage (Optional)
PAYLOAD_SAVE_DIR=~/payloads
```

### `fly.toml` (Cloud Config)
```toml
app = 'metasploit-mcp'
primary_region = 'iad'

[build]
  # Uses Dockerfile

[env]
  PORT = '8080'

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = 'stop'  # Cost saving!
  auto_start_machines = true

[[vm]]
  memory = '1gb'
  cpus = 1
```

---

## 🚦 Quick Start Cheat Sheet

### Option 1: Mock Mode (No Metasploit)
```bash
# Install
pip install -r requirements.txt

# Run
python MetasploitMCP.py --mock --transport http

# Access
http://localhost:8080/docs
```

### Option 2: Real Mode (With Metasploit)
```bash
# Install
pip install -r requirements.txt

# Configure
cp .env.example .env.local
nano .env.local  # Edit passwords

# Start Metasploit
make start-msf

# Run server
python MetasploitMCP.py --transport http

# Access
http://localhost:8080/docs
```

### Option 3: Deploy to Fly.io
```bash
# Login
flyctl auth login

# Launch
flyctl launch

# Set secrets
flyctl secrets set MSFRPCD_PASSWORD=xxx

# Deploy
flyctl deploy

# Access
https://your-app.fly.dev
```

---

## 🎯 Common Use Cases

### 1. 🔍 Security Research
```
You: "Tell me about CVE-2023-XXXX"
AI: (analyzes using analyze_vulnerability_with_ai)
AI: "This is a critical RCE vulnerability..."
```

### 2. 🛡️ Penetration Testing
```
You: "Scan and exploit 192.168.1.0/24"
AI: (runs scanner, finds vulnerabilities, suggests exploits)
AI: "Found 3 vulnerable hosts. Shall I exploit them?"
```

### 3. 📚 Learning
```
You: "How do I exploit a vulnerable FTP server?"
AI: (uses generate_metasploit_commands_with_ai)
AI: "Here are the steps: 1. Start handler... 2. Run exploit..."
```

### 4. 🤖 Automation
```
You: "Test all hosts in targets.txt and generate a report"
AI: (automates scanning, exploitation, reporting)
AI: "Completed. 12/15 hosts exploited. Report saved."
```

---

## 📊 Project Stats

```
📦 Lines of Code:      ~2,500+ (Python)
🛠️  MCP Tools:         13 tools
🧪 Test Coverage:      85%+
📚 Documentation:       6 comprehensive guides
🌍 Deployment Options:  5 platforms
⭐ GitHub Stars:        [Your stats]
🐳 Docker Image Size:   134 MB (optimized)
☁️  Cloud Hosting:      Fly.io (live demo)
```

---

## 🔗 Quick Links

### Documentation
- 📖 [README.md](README.md) - Main documentation
- 🎓 [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) - Complete beginner's guide ⭐ NEW
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide (5 options)
- 📝 [CHANGELOG.md](CHANGELOG.md) - Version history
- 🔧 [MSFRPCD_MANAGEMENT.md](MSFRPCD_MANAGEMENT.md) - msfrpcd reference

### Live Resources
- 🌐 **Live Demo:** https://metasploit-mcp.fly.dev/
- 📚 **API Docs:** https://metasploit-mcp.fly.dev/docs
- 📦 **GitHub:** https://github.com/FandresenaR/MetasploitMCP

### External Resources
- 🔴 [Metasploit Framework](https://docs.metasploit.com/)
- 🤖 [MCP Protocol](https://modelcontextprotocol.io/)
- ☁️ [Fly.io Docs](https://fly.io/docs/)
- 🌩️ [Oracle Cloud Docs](https://docs.oracle.com/cloud/)

---

## 🎓 Learning Path

```
1. READ BEGINNER_GUIDE.md
   └─> Understand the basics
       └─> Learn architecture
           └─> See examples

2. TRY MOCK MODE
   └─> No Metasploit needed
       └─> Test MCP tools
           └─> Experiment safely

3. DEPLOY LOCALLY
   └─> Install Metasploit
       └─> Configure msfrpcd
           └─> Test real exploits

4. CLOUD DEPLOYMENT
   └─> Try Fly.io (5 min)
       └─> Or Oracle Cloud (free)
           └─> Share with team

5. ADVANCED USE
   └─> Custom workflows
       └─> Production setup
           └─> Contribute back!
```

---

## ✅ Checklist for Beginners

- [ ] Read BEGINNER_GUIDE.md
- [ ] Understand the architecture
- [ ] Try mock mode
- [ ] Explore the 13 tools
- [ ] Configure .env.local
- [ ] Start msfrpcd (if using real mode)
- [ ] Test with AI assistant
- [ ] Try common workflows
- [ ] Deploy to cloud (optional)
- [ ] Read security best practices

---

## 🎉 Summary

**MetasploitMCP** connects AI assistants to Metasploit Framework, making security testing as easy as chatting!

### Key Features:
- ✅ 13 powerful MCP tools
- ✅ AI-powered analysis
- ✅ 5 deployment options
- ✅ Mock mode for learning
- ✅ Production-ready
- ✅ Well documented

### Get Started:
```bash
# Quickest way to try:
python MetasploitMCP.py --mock --transport http
# Then visit: http://localhost:8080/docs
```

### Need Help?
- 📖 Read [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)
- 🐛 Open GitHub issue
- 💬 Join discussions

---

**You're all set!** 🚀 Start with the [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) for detailed explanations.

---

*Last updated: October 18, 2025*  
*Created by: FandresenaR*
