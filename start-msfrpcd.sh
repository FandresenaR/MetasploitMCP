#!/bin/bash
# Start msfrpcd with configuration from .env.local

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Metasploit RPC Daemon${NC}"

# Load environment variables from .env.local
if [ -f .env.local ]; then
    echo -e "${GREEN}✅ Loading configuration from .env.local${NC}"
    export $(grep -v '^#' .env.local | xargs)
else
    echo -e "${RED}❌ Error: .env.local file not found${NC}"
    echo -e "${YELLOW}Please create .env.local from .env.example${NC}"
    exit 1
fi

# Check if password is set
if [ -z "$MSF_PASSWORD" ]; then
    echo -e "${RED}❌ Error: MSF_PASSWORD not set in .env.local${NC}"
    exit 1
fi

# Use environment variables or defaults
MSF_HOST="${MSF_SERVER:-127.0.0.1}"
MSF_RPC_PORT="${MSF_PORT:-55553}"

# Check if msfrpcd is already running
if pgrep -x "msfrpcd" > /dev/null; then
    echo -e "${YELLOW}⚠️  msfrpcd is already running${NC}"
    echo -e "${YELLOW}Kill it with: pkill msfrpcd${NC}"
    exit 1
fi

echo -e "${GREEN}📡 Starting msfrpcd...${NC}"
echo -e "   Host: ${MSF_HOST}"
echo -e "   Port: ${MSF_RPC_PORT}"
echo -e "   SSL: ${MSF_SSL:-false}"

# Start msfrpcd
msfrpcd -P "$MSF_PASSWORD" -S -a "$MSF_HOST" -p "$MSF_RPC_PORT"

# Check if it started successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ msfrpcd started successfully${NC}"
else
    echo -e "${RED}❌ Failed to start msfrpcd${NC}"
    exit 1
fi
