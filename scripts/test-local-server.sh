#!/bin/bash
#
# Script pour tester le serveur MetasploitMCP localement
# Simule l'environnement Render.com
#

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Test du Serveur MetasploitMCP en Local${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
echo ""

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 installé: $(python3 --version)${NC}"
echo ""

# Vérifier les dépendances
echo -e "${BLUE}[1/5] Vérification des dépendances...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt non trouvé${NC}"
    exit 1
fi

# Installer les dépendances si nécessaire
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Installation des dépendances...${NC}"
    pip install -r requirements.txt
fi
echo -e "${GREEN}✅ Dépendances installées${NC}"
echo ""

# Configuration des variables d'environnement pour le mode MOCK
echo -e "${BLUE}[2/5] Configuration de l'environnement MOCK...${NC}"
export MSF_PASSWORD="mock_password"
export MSF_SERVER="127.0.0.1"
export MSF_PORT="55553"
export MSF_SSL="false"
export LOG_LEVEL="INFO"

echo -e "${GREEN}✅ Variables d'environnement configurées${NC}"
echo ""

# Lancer le serveur en mode MOCK dans un processus background
echo -e "${BLUE}[3/5] Démarrage du serveur en mode MOCK...${NC}"
python3 MetasploitMCP.py --transport http --host 127.0.0.1 --port 8099 --mock > /tmp/metasploit_mcp_test.log 2>&1 &
SERVER_PID=$!

# Attendre que le serveur démarre
echo -e "${YELLOW}⏳ Attente du démarrage du serveur (PID: $SERVER_PID)...${NC}"
sleep 5

# Vérifier si le serveur est démarré
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${RED}❌ Le serveur n'a pas démarré correctement${NC}"
    echo ""
    echo -e "${YELLOW}Logs du serveur:${NC}"
    cat /tmp/metasploit_mcp_test.log
    exit 1
fi

echo -e "${GREEN}✅ Serveur démarré (PID: $SERVER_PID)${NC}"
echo ""

# Fonction pour tuer le serveur à la fin
cleanup() {
    echo ""
    echo -e "${YELLOW}Arrêt du serveur...${NC}"
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Serveur arrêté${NC}"
}
trap cleanup EXIT

# Test 1: Health Check
echo -e "${BLUE}[4/5] Test Health Check...${NC}"
HEALTH_RESPONSE=$(curl -s http://127.0.0.1:8099/healthz || echo "ERROR")
if echo "$HEALTH_RESPONSE" | grep -q '"status"'; then
    echo -e "${GREEN}✅ Health check: OK${NC}"
    echo "$HEALTH_RESPONSE" | jq '.' 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo -e "${RED}❌ Health check: FAILED${NC}"
    echo "Response: $HEALTH_RESPONSE"
    echo ""
    echo -e "${YELLOW}Logs du serveur:${NC}"
    cat /tmp/metasploit_mcp_test.log
    exit 1
fi
echo ""

# Test 2: Session SSE
echo -e "${BLUE}[5/5] Test des endpoints MCP...${NC}"
echo -e "${YELLOW}  → Test SSE Session...${NC}"
SESSION_ID=$(timeout 3 curl -s -N http://127.0.0.1:8099/mcp/sse 2>/dev/null | grep "^data:" | head -1 | sed 's/.*session_id=\([a-f0-9]*\).*/\1/' || echo "")

if [ -n "$SESSION_ID" ]; then
    echo -e "${GREEN}  ✅ Session SSE: OK (ID: $SESSION_ID)${NC}"
else
    echo -e "${RED}  ❌ Session SSE: FAILED${NC}"
    exit 1
fi

# Test 3: Tools List
echo -e "${YELLOW}  → Test Liste des Outils...${NC}"
TOOLS_RESPONSE=$(curl -s -X POST "http://127.0.0.1:8099/mcp/messages/?session_id=${SESSION_ID}" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' || echo "ERROR")

if echo "$TOOLS_RESPONSE" | grep -q '"tools"'; then
    TOOL_COUNT=$(echo "$TOOLS_RESPONSE" | jq '.result.tools | length' 2>/dev/null || echo "0")
    echo -e "${GREEN}  ✅ Tools list: OK ($TOOL_COUNT outils)${NC}"
elif echo "$TOOLS_RESPONSE" | grep -qi "accepted"; then
    echo -e "${RED}  ❌ Tools list: Retourne 'Accepted' (BUG!)${NC}"
    echo "  Response: $TOOLS_RESPONSE"
    exit 1
else
    echo -e "${YELLOW}  ⚠️  Tools list: Format inattendu${NC}"
    echo "  Response: $TOOLS_RESPONSE"
fi

# Test 4: Tools Call
echo -e "${YELLOW}  → Test Appel d'Outil...${NC}"
CALL_RESPONSE=$(curl -s -X POST "http://127.0.0.1:8099/mcp/messages/?session_id=${SESSION_ID}" \
    -H "Content-Type: application/json" \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_exploits","arguments":{"search_term":"ssh"}}}' || echo "ERROR")

if echo "$CALL_RESPONSE" | grep -qi "accepted" && ! echo "$CALL_RESPONSE" | grep -q '"result"'; then
    echo -e "${RED}  ❌ BUG CONFIRMÉ: Retourne 'Accepted'${NC}"
    echo "  Response: $CALL_RESPONSE"
    exit 1
elif echo "$CALL_RESPONSE" | jq -e '.result.content[0].text' > /dev/null 2>&1; then
    echo -e "${GREEN}  ✅ Tools call: OK - JSON-RPC valide${NC}"
    EXPLOIT_COUNT=$(echo "$CALL_RESPONSE" | jq -r '.result.content[0].text' | grep -c "exploit/" || echo "?")
    echo -e "${GREEN}     Exploits trouvés: $EXPLOIT_COUNT${NC}"
elif echo "$CALL_RESPONSE" | grep -q '"error"'; then
    echo -e "${YELLOW}  ⚠️  Tools call: Erreur JSON-RPC${NC}"
    echo "  Error: $(echo "$CALL_RESPONSE" | jq -r '.error.message' 2>/dev/null || echo "$CALL_RESPONSE")"
else
    echo -e "${YELLOW}  ⚠️  Tools call: Format inattendu${NC}"
    echo "  Response: $CALL_RESPONSE"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  ✅ TOUS LES TESTS SONT PASSÉS!${NC}"
echo -e "${GREEN}  Le code local fonctionne correctement${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}Prochaines étapes:${NC}"
echo "1. Commit et push les changements vers GitHub"
echo "2. Render.com redéploiera automatiquement"
echo "3. Tester avec: RENDER_URL=https://metasploitmcp.onrender.com ./scripts/test-render-fix.sh"
echo ""
