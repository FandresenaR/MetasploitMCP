#!/bin/bash
# MetasploitMCP Service Management Script
# Manages both remote msfrpcd and local MCP server

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOTE_HOST="metasploit-mcp"
MCP_LOG="/tmp/metasploitmcp.log"
MSFRPCD_LOG="/tmp/msfrpcd.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load environment variables
if [ -f "$SCRIPT_DIR/.env.local" ]; then
    source "$SCRIPT_DIR/.env.local"
else
    echo -e "${RED}Error: .env.local not found${NC}"
    exit 1
fi

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if msfrpcd is running on remote server
check_msfrpcd() {
    print_status "Checking msfrpcd on $REMOTE_HOST..."
    if ssh $REMOTE_HOST "pgrep -f 'msfrpcd'" > /dev/null 2>&1; then
        PID=$(ssh $REMOTE_HOST "pgrep -f 'msfrpcd' | head -1")
        print_success "msfrpcd is running (PID: $PID)"
        return 0
    else
        print_error "msfrpcd is not running"
        return 1
    fi
}

# Start msfrpcd on remote server
start_msfrpcd() {
    print_status "Starting msfrpcd on $REMOTE_HOST..."
    
    if check_msfrpcd > /dev/null 2>&1; then
        print_warning "msfrpcd is already running"
        return 0
    fi
    
    ssh $REMOTE_HOST "nohup msfrpcd -P '$MSF_PASSWORD' -a 0.0.0.0 -p $MSF_PORT > $MSFRPCD_LOG 2>&1 &"
    sleep 3
    
    if check_msfrpcd > /dev/null 2>&1; then
        print_success "msfrpcd started successfully"
        return 0
    else
        print_error "Failed to start msfrpcd"
        print_status "Check logs: ssh $REMOTE_HOST 'cat $MSFRPCD_LOG'"
        return 1
    fi
}

# Stop msfrpcd on remote server
stop_msfrpcd() {
    print_status "Stopping msfrpcd on $REMOTE_HOST..."
    
    if ! check_msfrpcd > /dev/null 2>&1; then
        print_warning "msfrpcd is not running"
        return 0
    fi
    
    ssh $REMOTE_HOST "sudo pkill -f 'msfrpcd'"
    sleep 2
    
    if ! check_msfrpcd > /dev/null 2>&1; then
        print_success "msfrpcd stopped successfully"
        return 0
    else
        print_error "Failed to stop msfrpcd"
        return 1
    fi
}

# Restart msfrpcd
restart_msfrpcd() {
    stop_msfrpcd
    sleep 2
    start_msfrpcd
}

# Check if MCP server is running
check_mcp() {
    print_status "Checking MetasploitMCP server..."
    if pgrep -f "MetasploitMCP.py" > /dev/null 2>&1; then
        PID=$(pgrep -f "MetasploitMCP.py")
        print_success "MetasploitMCP is running (PID: $PID)"
        return 0
    else
        print_error "MetasploitMCP is not running"
        return 1
    fi
}

# Start MCP server
start_mcp() {
    print_status "Starting MetasploitMCP server..."
    
    if check_mcp > /dev/null 2>&1; then
        print_warning "MetasploitMCP is already running"
        return 0
    fi
    
    cd "$SCRIPT_DIR"
    source venv/bin/activate
    nohup python3 MetasploitMCP.py --transport http --host 0.0.0.0 --port 8085 > "$MCP_LOG" 2>&1 &
    sleep 3
    
    if check_mcp > /dev/null 2>&1; then
        print_success "MetasploitMCP started successfully"
        print_status "API Docs: http://localhost:8085/docs"
        print_status "SSE Endpoint: http://localhost:8085/sse"
        return 0
    else
        print_error "Failed to start MetasploitMCP"
        print_status "Check logs: tail -f $MCP_LOG"
        return 1
    fi
}

# Stop MCP server
stop_mcp() {
    print_status "Stopping MetasploitMCP server..."
    
    if ! check_mcp > /dev/null 2>&1; then
        print_warning "MetasploitMCP is not running"
        return 0
    fi
    
    pkill -f "MetasploitMCP.py"
    sleep 2
    
    if ! check_mcp > /dev/null 2>&1; then
        print_success "MetasploitMCP stopped successfully"
        return 0
    else
        print_error "Failed to stop MetasploitMCP"
        return 1
    fi
}

# Restart MCP server
restart_mcp() {
    stop_mcp
    sleep 2
    start_mcp
}

# Check both services
status() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  MetasploitMCP Service Status"
    echo "═══════════════════════════════════════════"
    echo ""
    
    check_msfrpcd || true
    echo ""
    check_mcp || true
    echo ""
    
    # Test connectivity
    print_status "Testing connectivity to msfrpcd..."
    if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$MSF_SERVER/$MSF_PORT" 2>/dev/null; then
        print_success "Port $MSF_PORT is accessible on $MSF_SERVER"
    else
        print_error "Cannot connect to $MSF_SERVER:$MSF_PORT"
    fi
    echo ""
    
    # Show logs location
    print_status "Log files:"
    echo "  - Remote msfrpcd: ssh $REMOTE_HOST 'tail -f $MSFRPCD_LOG'"
    echo "  - Local MCP: tail -f $MCP_LOG"
    echo ""
}

# Start all services
start_all() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  Starting All Services"
    echo "═══════════════════════════════════════════"
    echo ""
    
    start_msfrpcd
    echo ""
    start_mcp
    echo ""
    status
}

# Stop all services
stop_all() {
    echo ""
    echo "═══════════════════════════════════════════"
    echo "  Stopping All Services"
    echo "═══════════════════════════════════════════"
    echo ""
    
    stop_mcp
    echo ""
    stop_msfrpcd
    echo ""
}

# Restart all services
restart_all() {
    stop_all
    sleep 2
    start_all
}

# Show usage
usage() {
    cat << EOF
MetasploitMCP Service Management

Usage: $0 {command} [options]

Commands:
  status              Show status of all services
  start               Start all services (msfrpcd + MCP)
  stop                Stop all services
  restart             Restart all services
  
  msfrpcd-start       Start only msfrpcd on remote server
  msfrpcd-stop        Stop only msfrpcd on remote server
  msfrpcd-restart     Restart msfrpcd
  msfrpcd-status      Check msfrpcd status
  msfrpcd-logs        Show msfrpcd logs
  
  mcp-start           Start only MCP server
  mcp-stop            Stop only MCP server
  mcp-restart         Restart MCP server
  mcp-status          Check MCP server status
  mcp-logs            Show MCP server logs
  
  test                Test connection to msfrpcd
  ssh                 SSH to remote server

Examples:
  $0 status           # Check all services
  $0 start            # Start everything
  $0 restart          # Restart everything
  $0 mcp-logs         # View MCP logs

EOF
}

# Main command handler
case "${1:-}" in
    status)
        status
        ;;
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    restart)
        restart_all
        ;;
    msfrpcd-start)
        start_msfrpcd
        ;;
    msfrpcd-stop)
        stop_msfrpcd
        ;;
    msfrpcd-restart)
        restart_msfrpcd
        ;;
    msfrpcd-status)
        check_msfrpcd
        ;;
    msfrpcd-logs)
        ssh $REMOTE_HOST "tail -f $MSFRPCD_LOG"
        ;;
    mcp-start)
        start_mcp
        ;;
    mcp-stop)
        stop_mcp
        ;;
    mcp-restart)
        restart_mcp
        ;;
    mcp-status)
        check_mcp
        ;;
    mcp-logs)
        tail -f "$MCP_LOG"
        ;;
    test)
        print_status "Testing connection to $MSF_SERVER:$MSF_PORT..."
        if timeout 5 bash -c "cat < /dev/null > /dev/tcp/$MSF_SERVER/$MSF_PORT" 2>/dev/null; then
            print_success "Connection successful"
        else
            print_error "Connection failed"
            exit 1
        fi
        ;;
    ssh)
        ssh $REMOTE_HOST
        ;;
    *)
        usage
        exit 1
        ;;
esac
