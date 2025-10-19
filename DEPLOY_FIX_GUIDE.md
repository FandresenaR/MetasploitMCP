# Guide de Déploiement - Fix ClosedResourceError

**Date:** 19 Octobre 2025  
**Fix:** Gestion des déconnexions SSE client

---

## 🚀 Étapes de Déploiement

### 1. Pousser le Code sur GitHub

```bash
cd /home/twain/Project/MetasploitMCP
git push origin main
```

### 2. Vérifier le Déploiement sur Render

1. Aller sur https://dashboard.render.com
2. Sélectionner le service **metasploitmcp-1**
3. Vérifier que le **Auto-Deploy** est activé
4. Attendre que le nouveau déploiement démarre (devrait être automatique)
5. Surveiller les logs de déploiement

### 3. Attendre la Fin du Déploiement

Le déploiement prend environ **10-15 minutes**:
- Build de l'image Docker
- Installation des dépendances
- Démarrage du service

### 4. Tester le Service Déployé

Une fois le déploiement terminé (statut "Live"):

```bash
# Test rapide health check
curl -s https://metasploitmcp-1.onrender.com/healthz | jq

# Test complet avec le script de diagnostic
./scripts/test-render-fix.sh
```

---

## ✅ Résultats Attendus

### Logs Render AVANT le Fix
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  ...
anyio.ClosedResourceError
```

### Logs Render APRÈS le Fix
```
INFO: Received POST message from 10.229.243.66:0
INFO:     10.229.243.66:0 - "POST /mcp/messages/?session_id=xxx HTTP/1.1" 202 Accepted
WARNING: Client 10.229.243.66:0 disconnected before response could be sent
```

### Script de Test APRÈS le Fix
```
═══════════════════════════════════════════════════════
  Test de Diagnostic du Serveur MetasploitMCP
  URL: https://metasploitmcp-1.onrender.com
═══════════════════════════════════════════════════════

[1/4] Test Health Check...
✅ Health check: OK

[2/4] Test Session SSE...
✅ Session SSE: OK
Session ID obtenu: abc123...

[3/4] Test Liste des Outils...
✅ Tools list: OK
Nombre d'outils disponibles: 14

[4/4] Test Appel d'Outil (list_exploits)...
✅ Tools call: OK - JSON-RPC valide reçu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ SUCCÈS: Le serveur fonctionne correctement!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔍 Vérifications Post-Déploiement

### 1. Vérifier les Logs Render

Dans le dashboard Render, vérifier que:
- ✅ Plus de stacktraces `ClosedResourceError` massives
- ✅ Messages de WARNING clairs pour les déconnexions clients
- ✅ Service répond aux requêtes health check

### 2. Tester avec Claude Desktop

Si vous utilisez Claude Desktop avec MCP:

```json
// Dans claude_desktop_config.json
{
  "mcpServers": {
    "metasploit": {
      "command": "uv",
      "args": ["--directory", "/path/to/MetasploitMCP", "run", "MetasploitMCP.py"],
      "env": {
        "OPENROUTER_API_KEY": "votre_clé"
      }
    }
  }
}
```

Redémarrer Claude Desktop et vérifier que les outils Metasploit sont disponibles.

### 3. Tester Manuellement les Endpoints

```bash
# Health check
curl https://metasploitmcp-1.onrender.com/healthz

# Session SSE (devrait créer une session)
curl -N https://metasploitmcp-1.onrender.com/mcp/sse

# Appel d'outil (nécessite un session_id valide)
curl -X POST https://metasploitmcp-1.onrender.com/mcp/messages/?session_id=SESSION_ID \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

---

## 🐛 Troubleshooting

### Le déploiement échoue
1. Vérifier les logs de build sur Render
2. S'assurer que `requirements.txt` est à jour
3. Vérifier que le Dockerfile est correct

### Les tests échouent encore avec ClosedResourceError
1. Vérifier que le code déployé est bien la dernière version
2. Forcer un redéploiement depuis le dashboard Render
3. Vérifier les variables d'environnement (OPENROUTER_API_KEY)

### Le service ne répond pas
1. Vérifier l'état du service sur Render (devrait être "Live")
2. Attendre 1-2 minutes après le déploiement (startup time)
3. Vérifier les logs Render pour d'éventuelles erreurs

---

## 📝 Notes

- **Auto-Deploy:** Si activé, chaque `git push` déclenche un nouveau déploiement
- **Healthz Endpoint:** Toujours tester avec `/healthz` d'abord
- **SSE Timeout:** Les connexions SSE peuvent prendre quelques secondes à s'établir
- **Logs:** Les logs Render sont en temps réel et très utiles pour le debugging

---

## ✅ Checklist Finale

Avant de valider le déploiement:

- [ ] Code poussé sur GitHub (`git push origin main`)
- [ ] Déploiement Render terminé (statut "Live")
- [ ] Health check répond (`/healthz` retourne 200 OK)
- [ ] Script de test passe (`./scripts/test-render-fix.sh`)
- [ ] Logs Render propres (pas d'ERROR ClosedResourceError)
- [ ] Tests manuels réussis (session SSE + tools/list)

---

**Prochaines Étapes:**

Une fois le déploiement validé, vous pouvez:
1. Utiliser le serveur dans Claude Desktop
2. Tester les différents outils Metasploit
3. Monitorer les performances via les logs Render

**Documentation Complète:** Voir `FIX_CLOSED_RESOURCE_ERROR.md` pour les détails techniques.
