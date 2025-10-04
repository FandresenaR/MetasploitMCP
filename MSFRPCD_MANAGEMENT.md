# 🔧 Metasploit RPC Daemon Management

This directory contains scripts to easily manage the Metasploit RPC daemon with configuration loaded from `.env.local`.

## 📋 Prerequisites

1. **Metasploit Framework** installed
2. **`.env.local`** file configured (copy from `.env.example`)

## 🚀 Quick Start

### 1. Configure Environment

Make sure your `.env.local` file has the Metasploit configuration:

```bash
MSF_PASSWORD=your_secure_password_here
MSF_SERVER=127.0.0.1
MSF_PORT=55553
MSF_SSL=false
```

### 2. Start msfrpcd

**Option A: Using the script directly**
```bash
./start-msfrpcd.sh
```

**Option B: Using Make**
```bash
make start-msf
```

### 3. Stop msfrpcd

**Option A: Using the script directly**
```bash
./stop-msfrpcd.sh
```

**Option B: Using Make**
```bash
make stop-msf
```

### 4. Restart msfrpcd

```bash
make restart-msf
```

## 📝 Scripts Included

### `start-msfrpcd.sh`
- Loads configuration from `.env.local`
- Starts msfrpcd with the configured password, host, and port
- Checks if msfrpcd is already running
- Validates that MSF_PASSWORD is set

### `stop-msfrpcd.sh`
- Gracefully stops the msfrpcd daemon
- Falls back to force kill if needed
- Provides status feedback

## 🔍 Troubleshooting

### msfrpcd won't start

1. **Check if already running:**
   ```bash
   pgrep msfrpcd
   ```

2. **Kill existing instance:**
   ```bash
   ./stop-msfrpcd.sh
   # or
   pkill msfrpcd
   ```

3. **Check password in .env.local:**
   ```bash
   grep MSF_PASSWORD .env.local
   ```

### Can't connect to msfrpcd

1. **Verify it's running:**
   ```bash
   pgrep msfrpcd
   ```

2. **Check the port:**
   ```bash
   netstat -tuln | grep 55553
   # or
   lsof -i :55553
   ```

3. **Test connection:**
   ```bash
   telnet 127.0.0.1 55553
   ```

## 🔐 Security Notes

- **Never commit `.env.local`** - It contains your password
- Use a **strong password** (32+ characters recommended)
- Bind to `127.0.0.1` for local-only access
- Use `0.0.0.0` only if you need external access (and use a firewall!)

## 📚 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MSF_PASSWORD` | RPC daemon password | - | ✅ Yes |
| `MSF_SERVER` | Host to bind to | `127.0.0.1` | No |
| `MSF_PORT` | Port to listen on | `55553` | No |
| `MSF_SSL` | Enable SSL (deprecated) | `false` | No |

## 🎯 Integration with MCP Server

The MCP server will automatically use the same environment variables:

1. Start msfrpcd:
   ```bash
   make start-msf
   ```

2. Start the MCP server:
   ```bash
   python MetasploitMCP.py --transport http
   ```

Both will use the same password and connection details from `.env.local`!
