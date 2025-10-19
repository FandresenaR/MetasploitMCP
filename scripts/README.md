# 🧪 Scripts de Test MetasploitMCP

Ce répertoire contient des scripts de test pour diagnostiquer et vérifier le serveur MetasploitMCP.

---

## 📋 Scripts Disponibles

### 1. `test-local-server.sh` - Test du Serveur Local

**Objectif**: Tester le serveur MetasploitMCP localement avant déploiement

**Mode**: MOCK (simule Metasploit sans connexion réelle)

**Usage**:
```bash
./scripts/test-local-server.sh
```

**Ce qui est testé**:
- ✅ Vérification des dépendances Python
- ✅ Démarrage du serveur en mode MOCK
- ✅ Health check (`/healthz`)
- ✅ Session SSE (`/mcp/sse`)
- ✅ Liste des outils (`tools/list`)
- ✅ Appel d'outil (`tools/call` → `list_exploits`)

**Durée**: ~10 secondes

**Résultat attendu**:
```
✅ Python 3 installé
✅ Dépendances installées
✅ Serveur démarré
✅ Health check: OK
✅ Session SSE: OK
✅ Tools list: OK
✅ Tools call: OK - JSON-RPC valide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ TOUS LES TESTS SONT PASSÉS!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 2. `test-render-fix.sh` - Test du Serveur Render.com

**Objectif**: Diagnostiquer le serveur MetasploitMCP déployé sur Render.com

**Mode**: Production (connexion au serveur réel)

**Usage**:
```bash
# Test avec URL par défaut
./scripts/test-render-fix.sh

# Test avec URL personnalisée
RENDER_URL=https://autre-url.onrender.com ./scripts/test-render-fix.sh
```

**Ce qui est testé**:
- ✅ Health check sur Render.com
- ✅ Session SSE (obtention d'un `session_id`)
- ✅ Liste des outils via MCP
- ❌ **Détection du bug "Accepted"** (test critique)

**Durée**: ~5 secondes

**Résultat attendu (SI TOUT FONCTIONNE)**:
```
✅ Health check: OK
✅ Session SSE: OK
✅ Tools list: OK
✅ Tools call: OK - JSON-RPC valide reçu
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ SUCCÈS: Le serveur fonctionne correctement!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Résultat attendu (SI BUG "Accepted" DÉTECTÉ)**:
```
✅ Health check: OK
✅ Session SSE: OK
⚠️  Tools list: Format inattendu
❌ PROBLÈME CONFIRMÉ: Le serveur retourne 'Accepted'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BUG DÉTECTÉ: Handler /mcp/messages/ mal implémenté
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🎯 Workflows d'Utilisation

### Workflow 1: Développement Local

Avant de déployer sur Render.com, tester localement:

```bash
# 1. Modifier le code
vim MetasploitMCP.py

# 2. Tester localement
./scripts/test-local-server.sh

# 3. Si tous les tests passent, commit et push
git add .
git commit -m "feat: Nouvelle fonctionnalité"
git push origin main
```

---

### Workflow 2: Diagnostic Render.com

Si le serveur Render.com a un problème:

```bash
# 1. Diagnostiquer le serveur
./scripts/test-render-fix.sh

# 2. Si bug détecté, forcer un redéploiement
git commit --allow-empty -m "chore: Trigger redeploy"
git push origin main

# 3. Attendre 3 minutes

# 4. Re-tester
./scripts/test-render-fix.sh
```

---

### Workflow 3: Tests Complets (Local + Render.com)

Avant un déploiement important:

```bash
# 1. Tester localement
./scripts/test-local-server.sh

# 2. Si OK, commit et push
git push origin main

# 3. Attendre le déploiement Render.com (3 min)

# 4. Tester Render.com
./scripts/test-render-fix.sh

# 5. Si OK, tester dans MyAI
```

---

## 🛠️ Dépendances

### Pour `test-local-server.sh`

- Python 3.11+
- `pip` installé
- Dépendances dans `requirements.txt`
- `curl` et `jq` (pour les tests HTTP)

### Pour `test-render-fix.sh`

- `curl` (pour les requêtes HTTP)
- `jq` (pour parser le JSON)
- `timeout` (pour limiter la durée des requêtes SSE)
- `sed` (pour extraire le session_id)

Installation des outils (si manquants):
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install curl jq coreutils

# macOS
brew install curl jq coreutils

# Arch Linux
sudo pacman -S curl jq coreutils
```

---

## 📊 Codes de Sortie

Les scripts utilisent les codes de sortie standard:

- `0` = Succès ✅ (tous les tests passent)
- `1` = Échec ❌ (au moins un test échoue)

Usage dans des scripts CI/CD:
```bash
#!/bin/bash
set -e

# Tester localement
./scripts/test-local-server.sh || exit 1

# Déployer
git push origin main

# Attendre
sleep 180

# Tester Render.com
./scripts/test-render-fix.sh || exit 1

echo "✅ Déploiement validé!"
```

---

## 🔍 Détails Techniques

### Structure d'un Test

Tous les scripts suivent cette structure:

1. **Setup** - Configuration des variables et vérification des dépendances
2. **Tests** - Série de tests HTTP/MCP
3. **Validation** - Comparaison des réponses avec les attendus
4. **Reporting** - Affichage des résultats avec couleurs
5. **Cleanup** - Nettoyage (arrêt du serveur pour test local)

### Format des Réponses MCP

#### Requête JSON-RPC (exemple)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "list_exploits",
    "arguments": {"search_term": "ssh"}
  }
}
```

#### Réponse Correcte ✅
```json
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

#### Réponse Incorrecte ❌
```
"Accepted"
```

---

## 🐛 Dépannage

### Problème: `./scripts/test-local-server.sh: Permission denied`

**Solution**:
```bash
chmod +x scripts/*.sh
```

---

### Problème: `python3: command not found`

**Solution**:
```bash
# Vérifier l'installation de Python
python --version
python3 --version

# Si Python n'est pas installé
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# macOS
brew install python3
```

---

### Problème: `curl: command not found`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install curl

# macOS (curl est préinstallé normalement)
brew install curl
```

---

### Problème: `jq: command not found`

**Solution**:
```bash
# Ubuntu/Debian
sudo apt-get install jq

# macOS
brew install jq
```

---

### Problème: Test local échoue avec "ModuleNotFoundError"

**Solution**:
```bash
# Installer les dépendances
pip install -r requirements.txt

# Ou avec pip3
pip3 install -r requirements.txt
```

---

### Problème: Test Render.com timeout

**Cause**: Le serveur Render.com est lent ou en train de démarrer

**Solution**:
- Attendre 2-3 minutes après un déploiement
- Vérifier que Render.com affiche "Deploy succeeded"
- Consulter les logs Render.com (Dashboard → Logs)

---

## 📝 Logs

### Logs du Test Local

Le test local génère un fichier de log temporaire:
```bash
# Voir les logs pendant le test
tail -f /tmp/metasploit_mcp_test.log

# Voir les logs après le test
cat /tmp/metasploit_mcp_test.log
```

### Logs du Test Render.com

Le test Render.com n'écrit pas de logs locaux, mais affiche tout dans le terminal.

Pour sauvegarder l'output:
```bash
./scripts/test-render-fix.sh 2>&1 | tee test-render-output.txt
```

---

## 🎓 En Savoir Plus

- **Documentation MCP**: https://spec.modelcontextprotocol.io/
- **Guide de déploiement**: `../GUIDE_DEPLOIEMENT_RENDER.md`
- **Diagnostic du problème**: `../DIAGNOSTIC_RENDER_PROBLEM.md`
- **Action immédiate**: `../ACTION_IMMEDIATE.md`

---

**Créé le**: 19 octobre 2025  
**Version**: 1.0  
**Auteur**: Assistant AI  
**Licence**: Même licence que MetasploitMCP
