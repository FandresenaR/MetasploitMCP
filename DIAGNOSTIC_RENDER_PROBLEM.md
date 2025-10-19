# 🔍 Diagnostic du Problème "Accepted" sur Render.com

**Date**: 19 octobre 2025  
**Statut**: ✅ Code local correct, ❓ Serveur Render.com à vérifier  
**Priorité**: 🔴 HAUTE - Bloque l'intégration MyAI

---

## 📋 Résumé du Problème

Selon le rapport fourni, le serveur MetasploitMCP déployé sur Render.com retourne la chaîne `"Accepted"` au lieu d'une réponse JSON-RPC valide lors d'appels d'outils.

### Symptôme

```bash
# Appel d'outil
curl -X POST "https://metasploitmcp.onrender.com/mcp/messages/?session_id=xxx" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list_exploits"}}'

# Réponse actuelle (❌ INCORRECTE):
"Accepted"

# Réponse attendue (✅ CORRECTE):
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "# Exploits Found: 8\n\n..."
    }]
  }
}
```

---

## ✅ Analyse du Code Local

J'ai analysé le code source dans `MetasploitMCP.py` et **le code local est correct** :

### 1. Structure des Routes MCP

```python
# Lines 2030-2044 dans MetasploitMCP.py
mcp_router = Router([
    Route("/sse", endpoint=SseEndpoint(), methods=["GET"]),
    Route("/messages/", endpoint=MessagesEndpoint(), methods=["POST"]),
])
app.mount("/mcp", mcp_router)
```

**✅ Correct**: Les routes sont bien montées sous `/mcp/`

### 2. Handler POST `/mcp/messages/`

```python
# Lines 2013-2019
class MessagesEndpoint:
    async def __call__(self, scope, receive, send):
        """Handle client POST messages for MCP communication."""
        client_host = scope.get('client')[0] if scope.get('client') else 'unknown'
        client_port = scope.get('client')[1] if scope.get('client') else 'unknown'
        logger.info(f"Received POST message from {client_host}:{client_port}")
        await sse.handle_post_message(scope, receive, send)
```

**✅ Correct**: Le handler délègue correctement à `sse.handle_post_message()` qui traite le JSON-RPC

### 3. Outils MCP Définis

```python
# Exemples d'outils définis avec @mcp.tool()
@mcp.tool()
async def list_exploits(search_term: str = "") -> List[str]:
    """List available Metasploit exploits..."""
    client = get_msf_client()
    # ... code qui retourne une liste d'exploits
    
@mcp.tool()
async def generate_payload(...) -> Dict[str, Any]:
    """Generate a Metasploit payload..."""
    # ... code qui retourne un dict avec status/message/data
```

**✅ Correct**: Les outils sont bien définis et retournent les bonnes structures de données

---

## 🔍 Hypothèses sur la Cause du Problème

### Hypothèse 1: Serveur Render.com Obsolète ⭐ PLUS PROBABLE

Le serveur déployé sur Render.com utilise peut-être une **ancienne version du code** qui contenait un bug dans le handler `/mcp/messages/`.

**Preuve**: Le code local actuel n'a pas de ligne retournant `"Accepted"` dans tout le fichier.

**Solution**: Redéployer le code actuel sur Render.com

### Hypothèse 2: Configuration Render.com Incorrecte

Le fichier `render.yaml` ou les variables d'environnement sur Render.com pointent vers un mauvais service ou ont une configuration incomplète.

**Solution**: Vérifier `render.yaml` et les env vars sur le dashboard Render.com

### Hypothèse 3: Problème de Session SSE

Le `session_id` obtenu via `/mcp/sse` n'est pas valide ou expire immédiatement, causant une réponse par défaut `"Accepted"`.

**Solution**: Améliorer la gestion des sessions et leur validation

---

## 🧪 Script de Diagnostic

J'ai créé un script de test complet: `scripts/test-render-fix.sh`

### Utilisation

```bash
# Test avec URL par défaut
chmod +x scripts/test-render-fix.sh
./scripts/test-render-fix.sh

# Test avec URL personnalisée
RENDER_URL=https://votre-url.onrender.com ./scripts/test-render-fix.sh
```

### Ce que le script teste

1. ✅ **Health Check** (`/healthz`) - Vérifie connectivité MSF
2. ✅ **Session SSE** (`/mcp/sse`) - Obtient un session_id
3. ✅ **Tools List** (`tools/list`) - Liste les outils disponibles
4. ✅ **Tools Call** (`tools/call`) - Appelle `list_exploits` (TEST CRITIQUE)

Le script affichera clairement si le bug "Accepted" est présent ou si tout fonctionne correctement.

---

## 🔧 Plan de Réparation

### Option A: Redéploiement Simple ⭐ RECOMMANDÉ

Si vous avez accès au dashboard Render.com:

```bash
# 1. Vérifier que le code local est à jour
git status
git pull origin main

# 2. S'assurer que render.yaml pointe vers le bon fichier
cat render.yaml

# 3. Commit et push (Render redéploie automatiquement)
git add .
git commit -m "Fix: Ensure correct MCP message handling"
git push origin main

# 4. Sur Render.com dashboard:
#    - Services → metasploitmcp → Manual Deploy → Deploy latest commit
#    - Attendre 2-3 minutes

# 5. Tester
./scripts/test-render-fix.sh
```

### Option B: Vérification du Déploiement

Si le redéploiement ne résout pas le problème, vérifier:

#### 1. Logs Render.com

```
Dashboard → Services → metasploitmcp → Logs
```

Chercher des lignes comme:
```
Starting MCP server in HTTP/SSE transport mode
MCP SSE Endpoint: /sse
Starting Uvicorn HTTP server on http://0.0.0.0:8000
```

#### 2. Variables d'Environnement

Vérifier que ces variables sont définies sur Render.com:
- `MSF_PASSWORD` - Mot de passe msfrpcd
- `MSF_SERVER` - IP du serveur MSF (e.g., `168.110.55.210`)
- `MSF_PORT` - Port msfrpcd (e.g., `55553`)
- `MSF_SSL` - `false` ou `true`

#### 3. Fichier de Démarrage

Vérifier dans `render.yaml`:
```yaml
services:
  - type: web
    name: metasploitmcp
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT
```

**Important**: Le `startCommand` doit exécuter `MetasploitMCP.py`, pas un autre fichier !

### Option C: Déploiement Manuel Test

Pour tester localement avant de déployer sur Render:

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer les variables d'environnement
export MSF_PASSWORD="your_password"
export MSF_SERVER="168.110.55.210"
export MSF_PORT="55553"
export MSF_SSL="false"

# 3. Lancer le serveur en mode HTTP
python MetasploitMCP.py --transport http --host 0.0.0.0 --port 8000

# 4. Dans un autre terminal, tester
RENDER_URL=http://localhost:8000 ./scripts/test-render-fix.sh
```

---

## 📊 Checklist de Vérification

Avant de considérer le problème résolu, vérifier:

- [ ] **Code Source** - `MetasploitMCP.py` est la dernière version (pas de `return "Accepted"`)
- [ ] **Git Status** - Aucune modification non commitée qui pourrait causer le problème
- [ ] **render.yaml** - Pointe vers `MetasploitMCP.py` dans `startCommand`
- [ ] **Render Dashboard** - Service `metasploitmcp` montre "Deploy succeeded"
- [ ] **Logs Render** - Pas d'erreurs, montre "Starting MCP server in HTTP/SSE transport mode"
- [ ] **Health Check** - `curl https://metasploitmcp.onrender.com/healthz` retourne JSON avec `"status":"ok"`
- [ ] **SSE Session** - `curl -N https://metasploitmcp.onrender.com/mcp/sse` retourne `event: endpoint`
- [ ] **Tools List** - POST `/mcp/messages/` avec `tools/list` retourne JSON-RPC avec liste d'outils
- [ ] **Tools Call** - POST `/mcp/messages/` avec `tools/call` retourne JSON-RPC avec résultats, **PAS "Accepted"**
- [ ] **Test MyAI** - L'application MyAI reçoit des exploits réels dans les rapports

---

## 🎯 Prochaines Étapes

1. **Exécuter le script de diagnostic**
   ```bash
   chmod +x scripts/test-render-fix.sh
   ./scripts/test-render-fix.sh
   ```

2. **Si le bug "Accepted" est confirmé** → Redéployer sur Render.com (Option A)

3. **Si le bug persiste après redéploiement** → Vérifier les logs et la configuration (Option B)

4. **Si tout fonctionne localement mais pas sur Render** → Comparer les configurations et variables d'environnement

---

## 💡 Notes Supplémentaires

### Pourquoi le Code Local est Correct

Le code utilise **FastMCP** et **mcp.server.sse.SseServerTransport** qui sont des bibliothèques robustes et testées. Le framework MCP gère automatiquement:

1. La sérialisation/désérialisation JSON-RPC
2. Le routage des méthodes (`tools/list`, `tools/call`, etc.)
3. La gestion des sessions SSE
4. Les réponses au format JSON-RPC valide

**Il n'y a AUCUNE ligne dans le code qui retourne manuellement `"Accepted"` comme string.**

### Endpoints Corrects

Les endpoints MCP corrects sont:
- SSE: `https://metasploitmcp.onrender.com/mcp/sse`
- Messages: `https://metasploitmcp.onrender.com/mcp/messages/`

**Pas** `/sse` et `/messages/` à la racine !

---

## 🆘 Besoin d'Aide ?

Si le problème persiste après avoir suivi ce guide:

1. Partager les **logs Render.com** (dernières 50 lignes)
2. Partager le résultat de `./scripts/test-render-fix.sh`
3. Vérifier si le repository GitHub est bien lié à Render.com
4. Vérifier la dernière date de déploiement sur Render.com vs. la date du dernier commit

---

**Créé le**: 19 octobre 2025  
**Dernière mise à jour**: 19 octobre 2025  
**Statut du code local**: ✅ CORRECT  
**Statut du serveur Render**: ❓ À VÉRIFIER
