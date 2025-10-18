# 🎭 Mode Mock - MetasploitMCP Sans Backend Metasploit

## 📖 Vue d'Ensemble

Le mode mock permet de déployer et tester MetasploitMCP **sans avoir besoin d'un serveur Metasploit fonctionnel**. C'est idéal pour :

- 🧪 Tester l'infrastructure MCP
- 🔧 Développer l'intégration MCP
- 📊 Démonstrations et prototypes
- ⚡ Développement rapide sans dépendances externes

## 🚀 Déploiement en Mode Mock

### Sur Render.com

Le serveur est configuré pour démarrer en mode mock via `render.yaml` :

```yaml
startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT --mock
```

### En Local

```bash
cd /home/twain/Project/MetasploitMCP
source venv/bin/activate
python MetasploitMCP.py --transport http --host 127.0.0.1 --port 8085 --mock
```

## ✅ Fonctionnalités en Mode Mock

### Health Check

```bash
curl https://metasploitmcp.onrender.com/healthz
```

**Réponse attendue** :
```json
{
  "status": "ok",
  "msf_version": "Mock Metasploit 6.0.0",
  "mode": "mock"
}
```

### Outils MCP Disponibles

Tous les outils MCP retournent des données mockées :

| Outil | Comportement Mock |
|-------|-------------------|
| `list_exploits` | Retourne 2 exploits d'exemple |
| `list_payloads` | Retourne 2 payloads d'exemple |
| `run_exploit` | Simule une exécution réussie |
| `list_active_sessions` | Retourne une liste vide |
| `send_session_command` | Retourne une erreur "session not found" |

### Connexion MCP

Le serveur expose les endpoints MCP standards :

```bash
# SSE Endpoint
curl -N https://metasploitmcp.onrender.com/mcp/sse

# Messages Endpoint
POST https://metasploitmcp.onrender.com/mcp/messages/
```

## 🔄 Passer en Mode Production

Une fois votre serveur Metasploit sur Oracle Cloud opérationnel :

### 1. Mettre à Jour render.yaml

```yaml
startCommand: python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT
# Retirer --mock
```

### 2. Configurer les Variables d'Environnement Render

Aller sur https://dashboard.render.com → metasploitmcp → Environment :

```bash
MSF_SERVER=168.110.55.210
MSF_PORT=55553
MSF_PASSWORD=MetasploitRPC2025_SecurePass!
MSF_SSL=false
```

### 3. Redéployer

```bash
git add render.yaml
git commit -m "Switch to production mode with real Metasploit backend"
git push origin main
```

Ou via le Dashboard Render : **Manual Deploy** → **Deploy latest commit**

## 🧪 Tests de Validation

### Test 1 : Health Check en Mode Mock

```bash
curl https://metasploitmcp.onrender.com/healthz
```

Devrait retourner `"mode": "mock"`.

### Test 2 : Endpoint MCP SSE

```bash
curl -N https://metasploitmcp.onrender.com/mcp/sse
```

Devrait retourner des events SSE :
```
event: endpoint
data: /mcp/messages/?session_id=...
```

### Test 3 : Liste des Exploits (Mock)

Via un client MCP ou en utilisant l'API directement, appeler l'outil `list_exploits`.

**Réponse mockée** :
```json
[
  "exploit/windows/smb/ms17_010_eternalblue",
  "exploit/unix/ftp/vsftpd_234_backdoor"
]
```

## ⚠️ Limitations du Mode Mock

### Ce qui NE fonctionne PAS :

- ❌ Exploitation réelle de vulnérabilités
- ❌ Génération de payloads réels
- ❌ Gestion de sessions Meterpreter
- ❌ Exécution de commandes dans des sessions
- ❌ Scan de vulnérabilités
- ❌ Post-exploitation

### Ce qui FONCTIONNE :

- ✅ Communication MCP (SSE, JSON-RPC)
- ✅ Découverte des outils MCP
- ✅ Structure des réponses API
- ✅ Health checks
- ✅ Tests d'intégration de l'infrastructure

## 🐛 Dépannage

### Problème : Health check retourne toujours un timeout

**Cause** : Le déploiement n'a pas encore pris en compte le flag `--mock`.

**Solution** :
1. Vérifier le Dashboard Render → Logs
2. Chercher `"Using mock Metasploit client for testing"`
3. Si absent, forcer un redéploiement :
   - Dashboard → Manual Deploy → Deploy latest commit

### Problème : Mode mock non activé malgré --mock

**Cause** : Le code vérifie `sys.argv` mais Render peut modifier la commande.

**Solution** : Utiliser une variable d'environnement :

```yaml
# render.yaml
envVars:
  - key: MSF_MOCK_MODE
    value: true
```

```python
# MetasploitMCP.py
mock_mode = os.getenv('MSF_MOCK_MODE', 'false').lower() == 'true' or '--mock' in sys.argv
```

## 📊 Monitoring

### Vérifier le Mode Actuel

```bash
# Via health check
curl -s https://metasploitmcp.onrender.com/healthz | jq '.mode'

# Devrait retourner "mock" ou null (si mode production)
```

### Logs Render

Dashboard → metasploitmcp → Logs

Chercher :
```
Using mock Metasploit client for testing
```

Ou en production :
```
Successfully connected to Metasploit RPC at ...
```

## 🎯 Cas d'Usage du Mode Mock

### 1. Développement MCP Client

Développez votre client MCP sans avoir besoin d'un serveur Metasploit :

```python
import requests

response = requests.get('https://metasploitmcp.onrender.com/mcp/sse', stream=True)
for line in response.iter_lines():
    print(line.decode())
```

### 2. Tests d'Intégration

```bash
# Test automatisé
curl -f https://metasploitmcp.onrender.com/healthz || exit 1
curl -f https://metasploitmcp.onrender.com/mcp/sse | head -5 || exit 1
```

### 3. Démos et Présentations

Montrez la structure MCP sans les risques de sécurité d'un vrai Metasploit.

## 🔐 Sécurité

### Avantages du Mode Mock

- ✅ Pas de vrai Metasploit exposé
- ✅ Pas de risque d'exploitation accidentelle
- ✅ Pas de credentials sensibles requis
- ✅ Sûr pour les environnements publics

### Recommandations

- 🔒 N'utilisez PAS le mode mock pour de vraies opérations de sécurité
- 🔒 Documentez clairement quand vous êtes en mode mock
- 🔒 Basculez en mode production uniquement quand nécessaire

## 📝 Prochaines Étapes

1. ✅ Vérifier que le mode mock fonctionne
2. ⏳ Résoudre les problèmes msfrpcd sur Oracle Cloud
3. 🔄 Basculer en mode production
4. 🧪 Tester toutes les fonctionnalités avec un vrai backend

---

**Status actuel** : Mode Mock activé sur Render (en attente de redéploiement)
