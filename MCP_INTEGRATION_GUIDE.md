# 🤖 Making MetasploitMCP Available for All AI Projects

Complete guide to integrating MetasploitMCP with various AI assistants and making it discoverable across different platforms.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [MCP Server Distribution Methods](#mcp-server-distribution-methods)
3. [Integration with Popular AI Assistants](#integration-with-popular-ai-assistants)
4. [Publishing to MCP Registry](#publishing-to-mcp-registry)
5. [NPM Package Distribution](#npm-package-distribution)
6. [Docker Distribution](#docker-distribution)
7. [Public API Deployment](#public-api-deployment)
8. [Configuration Templates](#configuration-templates)
9. [Security Considerations](#security-considerations)
10. [Best Practices](#best-practices)

---

## Overview

The Model Context Protocol (MCP) is an open standard that enables AI assistants to securely connect to external data sources and tools. To make MetasploitMCP available for all AI projects, you can:

1. **Publish to MCP Registry** - Official MCP server directory
2. **NPM Package** - Distributable package for Node.js environments
3. **Docker Image** - Containerized deployment
4. **Public API** - HTTP/SSE endpoint (your current Fly.io deployment)
5. **GitHub Repository** - Open source with clear documentation

### Current Status

✅ **Repository**: Public on GitHub  
✅ **Documentation**: Comprehensive guides (README, TOOLS.md, BEGINNER_GUIDE.md)  
✅ **API Deployment**: Live at https://metasploit-mcp.fly.dev/  
⚠️ **MCP Registry**: Not yet published  
⚠️ **NPM Package**: Not yet created  
✅ **Docker Support**: Dockerfile available  

---

## MCP Server Distribution Methods

### 1. GitHub Repository (✅ Current Method)

**Status**: Already available  
**URL**: https://github.com/FandresenaR/MetasploitMCP

**How AI Projects Can Use It**:

```json
{
  "mcpServers": {
    "metasploit": {
      "command": "python",
      "args": [
        "/path/to/MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "your.metasploit.server",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "your_password",
        "MSF_SSL": "true"
      }
    }
  }
}
```

**Pros**:
- ✅ Already working
- ✅ Full control over updates
- ✅ Clear documentation

**Cons**:
- ❌ Users must clone and setup manually
- ❌ Requires Python environment
- ❌ Not discoverable in MCP registry

---

### 2. MCP Registry (Recommended)

The official MCP server registry makes your server discoverable to all MCP-compatible AI assistants.

**Steps to Publish**:

#### a. Create `mcp.json` Manifest

Create a file at the root of your repository:

```json
{
  "name": "metasploit-mcp",
  "version": "1.0.0",
  "description": "Model Context Protocol server for Metasploit Framework integration",
  "author": "FandresenaR",
  "homepage": "https://github.com/FandresenaR/MetasploitMCP",
  "license": "Apache-2.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/FandresenaR/MetasploitMCP.git"
  },
  "capabilities": {
    "tools": [
      "list_exploits",
      "list_payloads",
      "run_exploit",
      "run_auxiliary_module",
      "run_post_module",
      "generate_payload",
      "list_active_sessions",
      "send_session_command",
      "terminate_session",
      "list_listeners",
      "start_listener",
      "stop_job",
      "analyze_exploit_with_ai",
      "generate_metasploit_commands_with_ai",
      "analyze_vulnerability_with_ai"
    ],
    "resources": [],
    "prompts": []
  },
  "transport": ["stdio", "http"],
  "runtime": {
    "python": ">=3.10"
  },
  "configuration": {
    "required": ["MSF_SERVER", "MSF_PASSWORD"],
    "optional": ["MSF_PORT", "MSF_SSL", "OPENROUTER_API_KEY", "PAYLOAD_SAVE_DIR"]
  },
  "keywords": [
    "metasploit",
    "security",
    "penetration-testing",
    "exploit",
    "cybersecurity",
    "mcp",
    "ai-tools"
  ]
}
```

#### b. Submit to MCP Registry

1. Visit: https://github.com/modelcontextprotocol/registry
2. Fork the repository
3. Add your server to `servers.json`:

```json
{
  "metasploit-mcp": {
    "name": "Metasploit MCP Server",
    "description": "Bridge between AI assistants and Metasploit Framework for penetration testing workflows",
    "repository": "https://github.com/FandresenaR/MetasploitMCP",
    "documentation": "https://github.com/FandresenaR/MetasploitMCP#readme",
    "transport": ["stdio", "http"],
    "category": "security",
    "tags": ["metasploit", "penetration-testing", "security", "exploit"],
    "featured": false
  }
}
```

4. Create pull request
5. Wait for review and approval

**After Publishing**:
- AI assistants can discover your server in the MCP registry
- Users can install with simple commands
- Automatic updates notifications

---

### 3. NPM Package (For JavaScript/TypeScript Environments)

Many MCP clients prefer npm packages for easy installation.

**Create Package Structure**:

```
metasploit-mcp/
├── package.json
├── index.js (wrapper script)
├── bin/
│   └── metasploit-mcp (executable)
└── python/
    └── MetasploitMCP.py (your existing code)
```

**package.json**:

```json
{
  "name": "@fandresenar/metasploit-mcp",
  "version": "1.0.0",
  "description": "MCP server for Metasploit Framework integration",
  "main": "index.js",
  "bin": {
    "metasploit-mcp": "./bin/metasploit-mcp"
  },
  "scripts": {
    "start": "python python/MetasploitMCP.py"
  },
  "keywords": [
    "mcp",
    "metasploit",
    "security",
    "ai",
    "model-context-protocol"
  ],
  "author": "FandresenaR",
  "license": "Apache-2.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/FandresenaR/MetasploitMCP.git"
  },
  "engines": {
    "node": ">=18.0.0"
  },
  "peerDependencies": {
    "python": ">=3.10"
  },
  "files": [
    "python/",
    "bin/",
    "index.js",
    "README.md"
  ]
}
```

**bin/metasploit-mcp** (executable wrapper):

```bash
#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const pythonScript = path.join(__dirname, '..', 'python', 'MetasploitMCP.py');

const args = process.argv.slice(2);
const python = spawn('python3', [pythonScript, ...args], {
  stdio: 'inherit',
  env: process.env
});

python.on('exit', (code) => {
  process.exit(code);
});
```

**Publish to NPM**:

```bash
# Login to npm
npm login

# Publish package
npm publish --access public
```

**Users Can Install**:

```bash
npm install -g @fandresenar/metasploit-mcp

# Then use in config
{
  "mcpServers": {
    "metasploit": {
      "command": "metasploit-mcp",
      "args": ["--transport", "stdio"]
    }
  }
}
```

---

### 4. Docker Hub Distribution

Make your Docker image publicly available.

**Build and Tag**:

```bash
# Build image
docker build -t fandresenar/metasploit-mcp:latest .
docker build -t fandresenar/metasploit-mcp:1.0.0 .

# Login to Docker Hub
docker login

# Push images
docker push fandresenar/metasploit-mcp:latest
docker push fandresenar/metasploit-mcp:1.0.0
```

**Create Docker Compose Template**:

```yaml
# docker-compose.yml
version: '3.8'

services:
  metasploit-mcp:
    image: fandresenar/metasploit-mcp:latest
    ports:
      - "8085:8085"
    environment:
      - MSF_SERVER=${MSF_SERVER}
      - MSF_PORT=${MSF_PORT:-55553}
      - MSF_PASSWORD=${MSF_PASSWORD}
      - MSF_SSL=${MSF_SSL:-true}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    restart: unless-stopped
```

**Users Can Deploy**:

```bash
# Pull and run
docker pull fandresenar/metasploit-mcp:latest
docker run -d \
  -p 8085:8085 \
  -e MSF_SERVER=your.server \
  -e MSF_PASSWORD=your_password \
  fandresenar/metasploit-mcp:latest

# Or with docker-compose
docker-compose up -d
```

---

### 5. Public HTTP/SSE API (✅ Already Deployed)

**Current Deployment**: https://metasploit-mcp.fly.dev/

**How AI Projects Can Use It**:

```python
# Python example
import requests

# Connect to SSE endpoint
response = requests.get('https://metasploit-mcp.fly.dev/sse', stream=True)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

```javascript
// JavaScript example
const eventSource = new EventSource('https://metasploit-mcp.fly.dev/sse');

eventSource.onmessage = (event) => {
  console.log('Message:', event.data);
};

eventSource.onerror = (error) => {
  console.error('Error:', error);
};
```

**Client Configuration**:

```json
{
  "mcpServers": {
    "metasploit": {
      "url": "https://metasploit-mcp.fly.dev/sse",
      "transport": "http"
    }
  }
}
```

**Advantages**:
- ✅ No installation required
- ✅ Works from anywhere
- ✅ Centralized updates

**Limitations**:
- ⚠️ Shared infrastructure
- ⚠️ Network latency
- ⚠️ Need authentication for production

---

## Integration with Popular AI Assistants

### 1. Claude Desktop

**Config Location**:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Configuration**:

```json
{
  "mcpServers": {
    "metasploit": {
      "command": "python",
      "args": [
        "/path/to/MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "168.110.55.210",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "your_password",
        "MSF_SSL": "true",
        "OPENROUTER_API_KEY": "your_openrouter_key"
      }
    }
  }
}
```

**Verification**:
1. Restart Claude Desktop
2. Look for 🔌 icon indicating MCP connection
3. Try: "List available exploits for Windows"

---

### 2. GitHub Copilot Chat (VS Code)

**Installation**:

```bash
# Install MCP extension for VS Code
code --install-extension modelcontextprotocol.mcp
```

**Configuration** (`.vscode/mcp.json`):

```json
{
  "servers": {
    "metasploit": {
      "command": "python",
      "args": [
        "${workspaceFolder}/MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "168.110.55.210",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "${env:MSF_PASSWORD}",
        "MSF_SSL": "true"
      }
    }
  }
}
```

---

### 3. OpenAI Custom GPTs

**Create Custom GPT**:

1. Go to https://chat.openai.com/gpts/editor
2. Create new GPT
3. Add custom action:

```yaml
openapi: 3.0.0
info:
  title: Metasploit MCP API
  version: 1.0.0
  description: Access Metasploit Framework through MCP
servers:
  - url: https://metasploit-mcp.fly.dev
paths:
  /sse:
    get:
      summary: MCP Server-Sent Events endpoint
      description: Connect to Metasploit MCP via SSE
      responses:
        '200':
          description: SSE stream
          content:
            text/event-stream:
              schema:
                type: string
```

4. Add instructions for using tools
5. Test and publish

---

### 4. LangChain Integration

**Python Example**:

```python
from langchain.tools import Tool
from langchain.agents import initialize_agent
import requests

class MetasploitMCPTool:
    def __init__(self, base_url="https://metasploit-mcp.fly.dev"):
        self.base_url = base_url
    
    def list_exploits(self, search_term=""):
        # Connect to MCP and call tool
        response = requests.post(
            f"{self.base_url}/tools/list_exploits",
            json={"search_term": search_term}
        )
        return response.json()

# Create LangChain tool
metasploit_tool = Tool(
    name="Metasploit Exploit Search",
    func=MetasploitMCPTool().list_exploits,
    description="Search for Metasploit exploits"
)

# Add to agent
agent = initialize_agent(
    tools=[metasploit_tool],
    llm=your_llm,
    agent="zero-shot-react-description"
)
```

---

### 5. AutoGPT / BabyAGI

**Plugin Configuration** (`plugins/metasploit_mcp.py`):

```python
class MetasploitMCPPlugin:
    """Plugin to integrate Metasploit MCP with AutoGPT"""
    
    def __init__(self):
        self.name = "metasploit_mcp"
        self.description = "Access Metasploit Framework tools"
        self.mcp_url = "https://metasploit-mcp.fly.dev/sse"
    
    def execute(self, command, args):
        # Connect to MCP and execute tool
        pass
```

---

### 6. ChatGPT Plugins (Deprecated, but for reference)

**plugin.json**:

```json
{
  "schema_version": "v1",
  "name_for_human": "Metasploit MCP",
  "name_for_model": "metasploit_mcp",
  "description_for_human": "Access Metasploit Framework for penetration testing",
  "description_for_model": "Provides access to 2,565+ exploits, 1,675+ payloads, and complete Metasploit functionality through natural language",
  "auth": {
    "type": "none"
  },
  "api": {
    "type": "openapi",
    "url": "https://metasploit-mcp.fly.dev/docs"
  },
  "logo_url": "https://metasploit-mcp.fly.dev/logo.png",
  "contact_email": "your-email@example.com",
  "legal_info_url": "https://github.com/FandresenaR/MetasploitMCP/blob/main/LICENSE"
}
```

---

## Publishing to MCP Registry

### Step-by-Step Guide

#### 1. Prepare Your Repository

**Required Files**:
- ✅ `README.md` - Clear documentation
- ✅ `LICENSE` - Apache 2.0
- ✅ `requirements.txt` - Dependencies
- ➕ `mcp.json` - MCP manifest (create this)
- ➕ `SECURITY.md` - Security policy (create this)
- ✅ `CHANGELOG.md` - Version history

#### 2. Create `mcp.json`

Already provided above in the MCP Registry section.

#### 3. Create `SECURITY.md`

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

Please report security vulnerabilities to: security@your-domain.com

**Do not** open public GitHub issues for security vulnerabilities.

## Security Considerations

- Always use SSL for production (MSF_SSL=true)
- Rotate passwords regularly
- Run in isolated networks
- Only use with authorized systems
- Review audit logs regularly
```

#### 4. Add Usage Examples to README

Add a dedicated "Quick Start" section:

```markdown
## Quick Start for AI Assistants

### Claude Desktop

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure Claude Desktop (`claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "metasploit": {
         "command": "python",
         "args": ["/path/to/MetasploitMCP.py", "--transport", "stdio"],
         "env": {
           "MSF_SERVER": "your.server",
           "MSF_PASSWORD": "your_password"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

4. Try: "List exploits for Windows SMB"
```

#### 5. Submit to Registry

```bash
# 1. Fork the MCP registry
gh repo fork modelcontextprotocol/registry

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/registry.git
cd registry

# 3. Add your server to servers.json
# (edit the file)

# 4. Commit and push
git add servers.json
git commit -m "Add Metasploit MCP Server"
git push origin main

# 5. Create pull request
gh pr create --title "Add Metasploit MCP Server" \
  --body "Adds Metasploit Framework integration server with 13 tools for penetration testing workflows"
```

---

## Configuration Templates

### Universal Configuration Template

Create `config-template.json`:

```json
{
  "_comment": "MetasploitMCP Configuration Template",
  "_instructions": "Copy this file and fill in your values",
  
  "mcpServers": {
    "metasploit": {
      "command": "python",
      "args": [
        "/FULL/PATH/TO/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "YOUR_METASPLOIT_SERVER_IP",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "YOUR_MSFRPCD_PASSWORD",
        "MSF_SSL": "true",
        "OPENROUTER_API_KEY": "YOUR_OPENROUTER_KEY_OPTIONAL",
        "PAYLOAD_SAVE_DIR": "/path/to/save/payloads"
      }
    }
  },
  
  "_examples": {
    "local_metasploit": {
      "MSF_SERVER": "127.0.0.1",
      "MSF_SSL": "false"
    },
    "remote_metasploit_oracle_cloud": {
      "MSF_SERVER": "168.110.55.210",
      "MSF_PORT": "55553",
      "MSF_SSL": "true"
    },
    "public_api": {
      "_comment": "Use public HTTP API instead of local installation",
      "url": "https://metasploit-mcp.fly.dev/sse",
      "transport": "http"
    }
  }
}
```

---

## Security Considerations

### Authentication & Authorization

**Current Status**: No authentication on public API ⚠️

**Recommendations for Production**:

#### 1. Add API Key Authentication

```python
# In MetasploitMCP.py
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = os.getenv("MCP_API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.get("/sse")
async def sse_endpoint(api_key: str = Depends(verify_api_key)):
    # ... existing code
```

#### 2. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/sse")
@limiter.limit("10/minute")
async def sse_endpoint(request: Request):
    # ... existing code
```

#### 3. IP Whitelisting

```python
ALLOWED_IPS = os.getenv("ALLOWED_IPS", "").split(",")

@app.middleware("http")
async def ip_whitelist_middleware(request: Request, call_next):
    client_ip = request.client.host
    if ALLOWED_IPS and client_ip not in ALLOWED_IPS:
        return JSONResponse(
            status_code=403,
            content={"detail": "IP not authorized"}
        )
    return await call_next(request)
```

### Network Security

**Recommendations**:
1. **Always use SSL** in production (`MSF_SSL=true`)
2. **Isolate testing networks** from production
3. **VPN access** for remote connections
4. **Firewall rules** to restrict access
5. **Regular password rotation**

### Deployment Security

**For Public API**:
- ✅ HTTPS enabled (Fly.io provides this)
- ⚠️ Add authentication
- ⚠️ Add rate limiting
- ⚠️ Add audit logging
- ⚠️ Add IP whitelisting

**For Private Deployment**:
- Use VPN or SSH tunneling
- Network isolation
- Strong passwords
- Regular updates

---

## Best Practices

### 1. Versioning

Follow Semantic Versioning:

```
MAJOR.MINOR.PATCH

1.0.0 → Initial release
1.1.0 → New features (backward compatible)
1.1.1 → Bug fixes
2.0.0 → Breaking changes
```

### 2. Documentation

Keep docs updated:
- ✅ README.md - Overview and quick start
- ✅ TOOLS.md - Complete tool reference
- ✅ BEGINNER_GUIDE.md - Step-by-step guide
- ✅ CHANGELOG.md - Version history
- ➕ API_REFERENCE.md - HTTP API docs
- ➕ SECURITY.md - Security policy

### 3. Testing

Maintain test coverage:
```bash
# Run tests before publishing
python run_tests.py --all --coverage

# Ensure >80% coverage
make coverage-html
```

### 4. Continuous Integration

Add GitHub Actions (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements-test.txt
      - run: python run_tests.py --all --coverage
```

### 5. Release Process

```bash
# 1. Update version in all files
# 2. Update CHANGELOG.md
# 3. Run tests
python run_tests.py --all

# 4. Commit and tag
git add .
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin main --tags

# 5. Create GitHub release
gh release create v1.1.0 \
  --title "Version 1.1.0" \
  --notes "See CHANGELOG.md for details"

# 6. Update deployments
flyctl deploy  # Fly.io
docker build -t fandresenar/metasploit-mcp:1.1.0 .
docker push fandresenar/metasploit-mcp:1.1.0
```

---

## Complete Integration Checklist

### Phase 1: Immediate (Can Do Now)

- [x] Public GitHub repository
- [x] Comprehensive documentation
- [x] Docker support
- [x] Public API (Fly.io)
- [ ] Create `mcp.json` manifest
- [ ] Create `SECURITY.md`
- [ ] Add authentication to public API
- [ ] Add usage examples to README

### Phase 2: Registry & Distribution

- [ ] Submit to MCP Registry
- [ ] Create NPM package
- [ ] Publish to Docker Hub
- [ ] Create integration examples
- [ ] Add CI/CD pipeline

### Phase 3: Enhanced Features

- [ ] Add API key authentication
- [ ] Implement rate limiting
- [ ] Add audit logging
- [ ] Create web dashboard
- [ ] Add webhook support

### Phase 4: Community & Maintenance

- [ ] Create Discord/Slack community
- [ ] Setup issue templates
- [ ] Create contribution guidelines
- [ ] Add more usage examples
- [ ] Record demo videos

---

## Next Steps

### To Make MetasploitMCP Available for All AI Projects:

1. **Create `mcp.json`** (provided in this guide)
2. **Create `SECURITY.md`** (template provided)
3. **Submit to MCP Registry**:
   ```bash
   gh repo fork modelcontextprotocol/registry
   # Add your server to servers.json
   gh pr create
   ```
4. **Publish NPM Package** (optional but recommended):
   ```bash
   npm publish --access public
   ```
5. **Publish Docker Image**:
   ```bash
   docker push fandresenar/metasploit-mcp:latest
   ```
6. **Add Security Features** to public API
7. **Create Tutorial Videos** for different AI platforms
8. **Promote** on:
   - MCP Discord
   - Reddit (r/LocalLLaMA, r/netsec)
   - Twitter/X
   - Dev.to / Medium

---

## Support & Community

### Getting Help

- **Documentation**: See README.md, TOOLS.md, BEGINNER_GUIDE.md
- **Issues**: https://github.com/FandresenaR/MetasploitMCP/issues
- **Discussions**: https://github.com/FandresenaR/MetasploitMCP/discussions

### Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

### License

Apache 2.0 - See LICENSE file

---

*Last Updated: October 18, 2025*  
*MetasploitMCP Version: 1.0.0*
