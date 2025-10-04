#!/bin/bash
# Quick reference for MetasploitMCP commands

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════╗
║          MetasploitMCP - Quick Reference Guide                   ║
╚══════════════════════════════════════════════════════════════════╝

🔧 MSFRPCD MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  make start-msf       Start msfrpcd (loads from .env.local)
  make stop-msf        Stop msfrpcd
  make restart-msf     Restart msfrpcd

  ./start-msfrpcd.sh   Direct script to start
  ./stop-msfrpcd.sh    Direct script to stop

🧪 TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  make test            Run all tests
  make test-unit       Run unit tests only
  make test-integration Run integration tests only
  make coverage        Run with coverage report
  make coverage-html   Generate HTML coverage report

🚀 DEVELOPMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  make install-deps    Install test dependencies
  make lint            Run code linting
  make format          Format code
  make clean           Clean generated files

☁️  DEPLOYMENT (FLY.IO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ./deploy-fly.sh      Automated deployment script
  flyctl deploy        Deploy to Fly.io
  flyctl logs          View deployment logs
  flyctl status        Check app status
  flyctl scale count 1 Scale to 1 machine
  flyctl open          Open app in browser

🌐 RUN MCP SERVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # HTTP/SSE mode (default)
  python MetasploitMCP.py --transport http

  # STDIO mode
  python MetasploitMCP.py --transport stdio

  # Mock mode (no Metasploit)
  python MetasploitMCP.py --transport http --mock

  # Custom port
  python MetasploitMCP.py --transport http --port 8085

🔍 DEBUGGING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # Check if msfrpcd is running
  ps aux | grep msfrpcd

  # Check port 55553
  netstat -tuln | grep 55553

  # Test msfrpcd connection
  telnet 127.0.0.1 55553

  # View environment config
  cat .env.local

📁 IMPORTANT FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  .env.local           Local environment configuration
  .env.example         Example environment file
  MetasploitMCP.py     Main MCP server
  Dockerfile           Docker configuration
  fly.toml             Fly.io deployment config
  DEPLOYMENT.md        Full deployment guide

🔐 SECURITY NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⚠️  Never commit .env.local (contains passwords)
  ✅  Use strong passwords (32+ characters)
  ✅  Bind to 127.0.0.1 for local-only access
  ✅  Use firewalls for production deployments

📚 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  README.md                Main documentation
  DEPLOYMENT.md            Deployment guide
  DEPLOYMENT_SUCCESS.md    Successful deployment info
  MSFRPCD_MANAGEMENT.md    msfrpcd management guide

EOF
