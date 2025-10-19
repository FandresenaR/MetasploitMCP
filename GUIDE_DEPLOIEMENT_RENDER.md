# 🚀 Guide de Déploiement et Réparation Render.com

**Date**: 19 octobre 2025  
**Objectif**: Résoudre le bug "Accepted" et déployer correctement sur Render.com  
**Durée estimée**: 10-15 minutes

---

## 📋 Pré-requis

- ✅ Accès au dashboard Render.com
- ✅ Repository GitHub `FandresenaR/MetasploitMCP` accessible
- ✅ Variables d'environnement Render.com configurées:
  - `MSF_SERVER` (IP du serveur Metasploit)
  - `MSF_PASSWORD` (mot de passe msfrpcd)
  - `MSF_PORT` (port msfrpcd, défaut: 55553)

---

## 🎯 Solution Rapide (5 minutes)

### Étape 1: Vérifier le Code Local

```bash
cd /home/twain/Project/MetasploitMCP

# Vérifier qu'il n'y a pas de modifications non sauvegardées
git status

# Vérifier la dernière version
git log --oneline -5
```

### Étape 2: Tester Localement (Recommandé)

```bash
# Rendre les scripts exécutables
chmod +x scripts/test-local-server.sh
chmod +x scripts/test-render-fix.sh

# Tester le serveur en local (mode MOCK)
./scripts/test-local-server.sh
```

**Résultat attendu**: Tous les tests doivent passer ✅

### Étape 3: Forcer le Redéploiement sur Render.com

Si le code local fonctionne, le problème vient du serveur Render.com qui utilise une ancienne version.

#### Option A: Via Dashboard Render.com (Recommandé)

1. Aller sur https://dashboard.render.com
2. Cliquer sur le service `metasploitmcp`
3. Onglet **"Manual Deploy"**
4. Cliquer sur **"Deploy latest commit"**
5. Attendre 2-3 minutes que le déploiement se termine

#### Option B: Via Git Push (Automatique)

```bash
# Faire un petit changement pour déclencher le redéploiement
echo "" >> README.md

# Commit et push
git add .
git commit -m "fix: Force redeploy to fix 'Accepted' bug"
git push origin main

# Render.com détectera le push et redéploiera automatiquement
```

### Étape 4: Vérifier le Déploiement

Attendre que Render.com montre "Deploy succeeded", puis:

```bash
# Tester le serveur Render.com
./scripts/test-render-fix.sh
```

**Résultat attendu**:
```
✅ Health check: OK
✅ Session SSE: OK
✅ Tools list: OK
✅ Tools call: OK - JSON-RPC valide reçu
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ SUCCÈS: Le serveur fonctionne correctement!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 Solution Détaillée (Si le Problème Persiste)

### Diagnostic Approfondi

#### 1. Consulter les Logs Render.com

```
Dashboard → Services → metasploitmcp → Logs
```

Chercher ces lignes de démarrage:
```
Starting MCP server in HTTP/SSE transport mode
MCP SSE Endpoint: /sse
Starting Uvicorn HTTP server on http://0.0.0.0:10000
```

**⚠️ Si ces lignes n'apparaissent pas**, le serveur ne démarre pas correctement.

Erreurs courantes:
```
# Erreur de connexion MSF (NORMAL en mode dégradé)
⚠️  Failed to initialize Metasploit client on startup: ...
Server will start anyway with degraded functionality

# Erreur de dépendances Python
ModuleNotFoundError: No module named 'fastapi'
→ Vérifier requirements.txt et buildCommand dans render.yaml

# Erreur de port
OSError: [Errno 98] Address already in use
→ Render.com gère automatiquement les ports, ceci ne devrait pas arriver
```

#### 2. Vérifier les Variables d'Environnement

```
Dashboard → Services → metasploitmcp → Environment
```

Variables **REQUISES**:
- `MSF_SERVER` = Adresse IP du serveur Metasploit (ex: `168.110.55.210`)
- `MSF_PASSWORD` = Mot de passe msfrpcd
- `MSF_PORT` = `55553` (par défaut)
- `MSF_SSL` = `false` (par défaut)

Variables **OPTIONNELLES**:
- `OPENROUTER_API_KEY` = Clé API pour les fonctionnalités AI
- `OPENROUTER_MODEL` = Modèle AI à utiliser
- `PAYLOAD_SAVE_DIR` = `/tmp/payloads` (par défaut)
- `LOG_LEVEL` = `INFO` ou `DEBUG`

#### 3. Vérifier la Configuration render.yaml

Le fichier `render.yaml` doit contenir:

```yaml
services:
  - type: web
    name: metasploitmcp
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT
    # ...
    healthCheckPath: /healthz
    autoDeploy: true
```

**Points critiques**:
- ✅ `startCommand` doit lancer `MetasploitMCP.py` (pas un autre fichier!)
- ✅ `--transport http` (pas stdio)
- ✅ `--host 0.0.0.0` (pour écouter sur toutes les interfaces)
- ✅ `--port $PORT` (Render.com injecte automatiquement le port)

#### 4. Vérifier la Branche Déployée

```
Dashboard → Services → metasploitmcp → Settings
```

Vérifier que:
- **Branch**: `main` (ou la branche contenant le code correct)
- **Auto-Deploy**: Activé

Si la branche déployée est incorrecte:
1. Changer la branche dans les Settings
2. Cliquer sur "Save Changes"
3. Forcer un redéploiement manuel

---

## 🧪 Tests de Validation Post-Déploiement

### Test 1: Endpoints Accessibles

```bash
# Health check (doit retourner JSON)
curl -s https://metasploitmcp.onrender.com/healthz | jq .

# SSE endpoint (doit retourner event: endpoint)
timeout 3 curl -s -N https://metasploitmcp.onrender.com/mcp/sse
```

### Test 2: Workflow Complet MCP

```bash
# Utiliser le script de test automatique
./scripts/test-render-fix.sh
```

### Test 3: Intégration MyAI

Si tous les tests précédents passent, tester depuis votre application MyAI:

```javascript
// Test depuis MyAI (Node.js)
const response = await fetch('https://metasploitmcp.onrender.com/mcp/sse');
const reader = response.body.getReader();
const decoder = new TextDecoder();

// Obtenir le session_id
const { value } = await reader.read();
const text = decoder.decode(value);
const sessionId = text.match(/session_id=([a-f0-9]+)/)?.[1];

// Appeler un outil
const toolResponse = await fetch(
  `https://metasploitmcp.onrender.com/mcp/messages/?session_id=${sessionId}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'tools/call',
      params: {
        name: 'list_exploits',
        arguments: { search_term: 'ssh' }
      }
    })
  }
);

const result = await toolResponse.json();
console.log('Résultat:', result);

// Doit afficher: { jsonrpc: '2.0', id: 1, result: { content: [...] } }
// PAS: "Accepted"
```

---

## 🐛 Dépannage des Problèmes Courants

### Problème: Le serveur retourne toujours "Accepted"

**Causes possibles**:
1. ❌ Le code déployé sur Render.com est une ancienne version
2. ❌ Render.com n'a pas redéployé après le push Git
3. ❌ La branche déployée est incorrecte

**Solutions**:
```bash
# 1. Vérifier que le code local est correct
grep -r "Accepted" MetasploitMCP.py
# Résultat attendu: Aucune correspondance (sauf dans les commentaires)

# 2. Forcer un redéploiement manuel sur Render.com
# Dashboard → Manual Deploy → Deploy latest commit

# 3. Vérifier les logs après redéploiement
# Dashboard → Logs → Chercher "Starting MCP server"
```

### Problème: "Session ID not found" ou "Invalid session"

**Cause**: Le `session_id` obtenu via SSE est expiré ou invalide

**Solutions**:
1. Vérifier que le serveur est bien démarré (`/healthz`)
2. Obtenir un nouveau `session_id` via `/mcp/sse`
3. Utiliser le `session_id` immédiatement (ne pas attendre)

### Problème: "Metasploit client not initialized"

**Cause**: Le serveur ne peut pas se connecter à msfrpcd

**Solutions**:
1. Vérifier que `MSF_SERVER`, `MSF_PORT`, `MSF_PASSWORD` sont corrects
2. Vérifier que msfrpcd est démarré sur le serveur distant:
   ```bash
   ssh user@168.110.55.210
   ps aux | grep msfrpcd
   # Doit montrer un processus msfrpcd actif
   ```
3. Vérifier la connectivité réseau:
   ```bash
   nc -zv 168.110.55.210 55553
   # Doit retourner "succeeded!"
   ```

### Problème: 503 Service Unavailable

**Cause**: Le serveur Render.com est en train de démarrer ou a planté

**Solutions**:
1. Attendre 2-3 minutes (démarrage initial)
2. Consulter les logs Render.com
3. Si le serveur a planté, redémarrer manuellement:
   ```
   Dashboard → Services → metasploitmcp → Manual Deploy → Restart
   ```

---

## ✅ Checklist Finale

Après avoir suivi ce guide, vérifier:

- [ ] ✅ `./scripts/test-local-server.sh` passe tous les tests
- [ ] ✅ Code pushé sur GitHub (branche `main`)
- [ ] ✅ Render.com montre "Deploy succeeded" (vert)
- [ ] ✅ Logs Render.com montrent "Starting MCP server in HTTP/SSE transport mode"
- [ ] ✅ `curl https://metasploitmcp.onrender.com/healthz` retourne `{"status":"ok"}`
- [ ] ✅ `./scripts/test-render-fix.sh` passe tous les tests
- [ ] ✅ MyAI reçoit des exploits réels (pas "Accepted")
- [ ] ✅ Les rapports MyAI contiennent des exploits Metasploit

---

## 🎉 Succès !

Si tous les tests passent, le problème "Accepted" est résolu ! 🎊

Le serveur MetasploitMCP sur Render.com retourne maintenant correctement des réponses JSON-RPC valides, et votre application MyAI peut afficher de vrais exploits Metasploit dans les rapports de scan.

---

## 📞 Support

Si le problème persiste malgré ce guide:

1. **Logs Render.com**: Copier les 100 dernières lignes de logs
2. **Test Script Output**: Copier le résultat de `./scripts/test-render-fix.sh`
3. **Git Status**: Copier le résultat de `git log --oneline -10`
4. **Variables d'Environnement**: Liste des variables définies sur Render.com (sans les valeurs sensibles)

---

**Créé le**: 19 octobre 2025  
**Testé avec**: Python 3.11, FastMCP 0.9.0, Render.com Free Plan  
**Maintenance**: Mettre à jour ce guide si la structure du code change
