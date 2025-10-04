#!/bin/bash
# Stop msfrpcd daemon

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🛑 Stopping Metasploit RPC Daemon${NC}"

# Check if msfrpcd is running
if pgrep -x "msfrpcd" > /dev/null; then
    pkill msfrpcd
    sleep 1
    
    # Verify it stopped
    if ! pgrep -x "msfrpcd" > /dev/null; then
        echo -e "${GREEN}✅ msfrpcd stopped successfully${NC}"
    else
        echo -e "${RED}❌ Failed to stop msfrpcd. Trying force kill...${NC}"
        pkill -9 msfrpcd
        echo -e "${GREEN}✅ msfrpcd force killed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  msfrpcd is not running${NC}"
fi
