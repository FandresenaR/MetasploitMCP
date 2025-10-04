#!/bin/bash
set -e

echo "🚀 Starting Metasploit MCP Server with Metasploit Framework"

# Start PostgreSQL for Metasploit database
echo "📦 Starting PostgreSQL..."
service postgresql start

# Wait for PostgreSQL to be ready
sleep 3

# Initialize Metasploit database if not already done
echo "🗄️  Initializing Metasploit database..."
msfdb reinit --no-interaction || msfdb init || true

# Generate a random password if not set
if [ -z "$MSFRPCD_PASSWORD" ]; then
    export MSFRPCD_PASSWORD=$(openssl rand -base64 32)
    echo "⚠️  Generated random MSFRPCD password: $MSFRPCD_PASSWORD"
    echo "   Set MSFRPCD_PASSWORD environment variable to use a custom password"
fi

# Start msfrpcd in the background
echo "🔧 Starting msfrpcd..."
msfrpcd -P "$MSFRPCD_PASSWORD" -S -a 127.0.0.1 -p "${MSFRPCD_PORT:-55553}" &

# Wait for msfrpcd to start
sleep 5

# Set environment variables for the MCP server
export MSFRPCD_HOST="${MSFRPCD_HOST:-127.0.0.1}"
export MSFRPCD_PORT="${MSFRPCD_PORT:-55553}"

echo "✅ msfrpcd started on ${MSFRPCD_HOST}:${MSFRPCD_PORT}"
echo "🌐 Starting MCP Server..."

# Start the MCP server (without --mock flag since Metasploit is available)
exec python3 MetasploitMCP.py --transport http --host 0.0.0.0 --port 8080
