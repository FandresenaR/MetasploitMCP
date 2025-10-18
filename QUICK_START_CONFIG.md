# Quick Start Configuration Examples

## Claude Desktop

### Windows
Location: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "metasploit": {
      "command": "python",
      "args": [
        "C:\\Users\\YourUsername\\MetasploitMCP\\MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "127.0.0.1",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "your_password_here",
        "MSF_SSL": "false",
        "OPENROUTER_API_KEY": "your_openrouter_key_optional"
      }
    }
  }
}
```

### macOS
Location: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "metasploit": {
      "command": "python3",
      "args": [
        "/Users/yourusername/MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "127.0.0.1",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "your_password_here",
        "MSF_SSL": "false"
      }
    }
  }
}
```

### Linux
Location: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "metasploit": {
      "command": "python3",
      "args": [
        "/home/yourusername/MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "127.0.0.1",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "your_password_here",
        "MSF_SSL": "false"
      }
    }
  }
}
```

## Remote Metasploit Server

If your Metasploit is on a remote server (like Oracle Cloud):

```json
{
  "mcpServers": {
    "metasploit": {
      "command": "python3",
      "args": [
        "/path/to/MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "your.server.ip.address",
        "MSF_PORT": "55553",
        "MSF_PASSWORD": "your_password_here",
        "MSF_SSL": "true"
      }
    }
  }
}
```

## Using Public HTTP API

Connect to the public MetasploitMCP instance:

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

## VS Code with MCP Extension

Create `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "metasploit": {
      "command": "python3",
      "args": [
        "${workspaceFolder}/../MetasploitMCP/MetasploitMCP.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "MSF_SERVER": "${env:MSF_SERVER}",
        "MSF_PASSWORD": "${env:MSF_PASSWORD}",
        "MSF_PORT": "55553",
        "MSF_SSL": "false"
      }
    }
  }
}
```

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/FandresenaR/MetasploitMCP.git
cd MetasploitMCP
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Setup Metasploit

```bash
# Start msfrpcd
msfrpcd -P yourpassword -S -a 127.0.0.1 -p 55553
```

### 4. Configure Environment

```bash
# Copy example config
cp .env.example .env.local

# Edit with your values
nano .env.local
```

### 5. Test Connection

```bash
# Test with Python
python3 -c "
from dotenv import load_dotenv
load_dotenv('.env.local')
from pymetasploit3.msfrpc import MsfRpcClient
import os
client = MsfRpcClient(
    password=os.getenv('MSF_PASSWORD'),
    server=os.getenv('MSF_SERVER'),
    port=int(os.getenv('MSF_PORT', 55553)),
    ssl=os.getenv('MSF_SSL', 'false').lower() == 'true'
)
print('Connected:', client.core.version)
"
```

### 6. Configure AI Assistant

Add the configuration to your AI assistant's config file (examples above).

### 7. Restart & Test

```bash
# Restart Claude Desktop or your AI assistant
# Try: "List exploits for Windows"
```

## Verification

After configuration, verify the MCP connection:

1. **Look for MCP indicator** in your AI assistant
2. **Try a command**: "List available exploits"
3. **Check tools**: Should show 13 Metasploit tools available
4. **Test a tool**: "Show me exploits for SMB"

## Troubleshooting

### Connection Failed

```bash
# Check msfrpcd is running
pgrep -f msfrpcd

# Check port is accessible
nc -zv 127.0.0.1 55553

# Check credentials
cat .env.local | grep MSF_
```

### Authentication Failed

```bash
# Restart msfrpcd with correct password
pkill msfrpcd
msfrpcd -P yourpassword -S -a 127.0.0.1 -p 55553
```

### Python Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## Next Steps

- Read [TOOLS.md](TOOLS.md) for complete tool reference
- Check [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) for detailed walkthrough
- See [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md) for advanced integration

## Support

- **Issues**: https://github.com/FandresenaR/MetasploitMCP/issues
- **Documentation**: See repository README and guides
- **Examples**: Check TOOLS.md for usage examples
