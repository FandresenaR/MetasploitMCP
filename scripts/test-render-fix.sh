#!/bin/bash
#
# Script de diagnostic pour tester le serveur MetasploitMCP sur Render.com
# Date: 19 octobre 2025
#

set -e

# Couleurs pour l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# URL du serveur Render.com
RENDER_URL="${RENDER_URL:-https://metasploitmcp.onrender.com}"

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test de Diagnostic du Serveur MetasploitMCP${NC}"
echo -e "${BLUE}  URL: $RENDER_URL${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Test 1: Health Check
echo -e "${BLUE}[1/4] Test Health Check...${NC}"
HEALTH_RESPONSE=$(curl -s "${RENDER_URL}/healthz" || echo "ERROR")
if echo "$HEALTH_RESPONSE" | grep -q '"status"'; then
    echo -e "${GREEN}✅ Health check: OK${NC}"
    echo "$HEALTH_RESPONSE" | jq '.' || echo "$HEALTH_RESPONSE"
else
    echo -e "${RED}❌ Health check: FAILED${NC}"
    echo "Response: $HEALTH_RESPONSE"
    exit 1
fi
echo ""

# Test 2: Session SSE
echo -e "${BLUE}[2/4] Test Session SSE...${NC}"
SESSION_ID=$(timeout 5 curl -s -N "${RENDER_URL}/mcp/sse" 2>/dev/null | grep "^data:" | head -1 | sed 's/.*session_id=\([a-f0-9]*\).*/\1/' || echo "")

if [ -n "$SESSION_ID" ]; then
    echo -e "${GREEN}✅ Session SSE: OK${NC}"
    echo "Session ID obtenu: $SESSION_ID"
else
    echo -e "${RED}❌ Session SSE: FAILED${NC}"
    echo "Impossible d'obtenir un session ID"
    exit 1
fi
echo ""

# Test 3: Tools List
echo -e "${BLUE}[3/4] Test Liste des Outils...${NC}"
TOOLS_RESPONSE=$(curl -s -X POST "${RENDER_URL}/mcp/messages/?session_id=${SESSION_ID}" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' || echo "ERROR")

if echo "$TOOLS_RESPONSE" | grep -q '"tools"'; then
    echo -e "${GREEN}✅ Tools list: OK${NC}"
    TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | jq '.result.tools | length' 2>/dev/null || echo "0")
    echo "Nombre d'outils disponibles: $TOOL_COUNT"
    echo "$TOOLS_RESPONSE" | jq '.result.tools[].name' 2>/dev/null | head -5 || echo "Format inattendu"
elif echo "$TOOLS_RESPONSE" | grep -qi "accepted"; then
    echo -e "${RED}❌ Tools list: Retourne 'Accepted' (BUG CONFIRMÉ)${NC}"
    echo "Response: $TOOLS_RESPONSE"
else
    echo -e "${YELLOW}⚠️  Tools list: Format inattendu${NC}"
    echo "Response: $TOOLS_RESPONSE"
fi
echo ""

# Test 4: Tools Call (le test critique)
echo -e "${BLUE}[4/4] Test Appel d'Outil (list_exploits)...${NC}"
CALL_RESPONSE=$(curl -s -X POST "${RENDER_URL}/mcp/messages/?session_id=${SESSION_ID}" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_exploits","arguments":{"search_term":"ssh"}}}' || echo "ERROR")

if echo "$CALL_RESPONSE" | grep -qi "accepted" && ! echo "$CALL_RESPONSE" | grep -q '"result"'; then
    echo -e "${RED}❌ PROBLÈME CONFIRMÉ: Le serveur retourne 'Accepted' au lieu de JSON-RPC${NC}"
    echo ""
    echo -e "${YELLOW}Response reçue:${NC}"
    echo "$CALL_RESPONSE"
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}  BUG DÉTECTÉ: Handler /mcp/messages/ mal implémenté${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}Actions recommandées:${NC}"
    echo "1. Vérifier le code du serveur sur Render.com"
    echo "2. S'assurer que /mcp/messages/ retourne du JSON-RPC valide"
    echo "3. Voir GUIDE-REPARATION-RENDER.md pour les étapes détaillées"
    exit 1
elif echo "$CALL_RESPONSE" | jq -e '.result.content[0].text' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Tools call: OK - JSON-RPC valide reçu${NC}"
    echo ""
    echo -e "${GREEN}Contenu des exploits (premiers 15 caractères):${NC}"
    echo "$CALL_RESPONSE" | jq -r '.result.content[0].text' | head -20
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✅ SUCCÈS: Le serveur fonctionne correctement!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    exit 0
elif echo "$CALL_RESPONSE" | grep -q '"error"'; then
    echo -e "${YELLOW}⚠️  Tools call: Erreur JSON-RPC${NC}"
    echo "Error message:"
    echo "$CALL_RESPONSE" | jq '.error' || echo "$CALL_RESPONSE"
    exit 1
else
    echo -e "${YELLOW}⚠️  Tools call: Format inattendu${NC}"
    echo "Response:"
    echo "$CALL_RESPONSE"
    exit 1
fi
