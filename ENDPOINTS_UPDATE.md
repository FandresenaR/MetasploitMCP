# 📡 Endpoints Update - Important Changes

## Date: October 18, 2025

### ⚠️ Breaking Changes - MCP Endpoints

Les endpoints MCP ont été déplacés pour résoudre un conflit de routage.

#### ✅ Nouveaux Endpoints (Actifs)

| Endpoint | Type | Description |
|----------|------|-------------|
| `/` | GET | Health check (principal) |
| `/healthz` | GET | Health check (alternatif) |
| `/mcp/sse` | GET | Server-Sent Events pour MCP |
| `/mcp/messages/` | POST | Messages MCP |

#### ❌ Anciens Endpoints (Obsolètes)

| Endpoint | Nouveau | Note |
|----------|---------|------|
| `/sse` | `/mcp/sse` | Déplacé |
| `/messages/` | `/mcp/messages/` | Déplacé |

### 🔧 Pourquoi ce changement ?

Le problème initial était que le `Mount("/", app=mcp_router)` capturait TOUTES les requêtes avant que les routes FastAPI ne soient évaluées, causant des erreurs 404 sur `/healthz`.

**Solution appliquée :**
1. Définir les routes FastAPI (`@app.get`) AVANT le montage du router MCP
2. Monter le router MCP sous `/mcp` au lieu de `/`

### 🔄 Migration

#### Pour Claude Desktop / MCP Clients

Mettre à jour votre configuration MCP :

```json
{
  "mcpServers": {
    "metasploit": {
      "url": "https://metasploitmcp.onrender.com/mcp/sse",
      "transport": "sse"
    }
  }
}
```

#### Pour les Requêtes Directes

**Avant :**
```bash
curl -N https://metasploitmcp.onrender.com/sse
```

**Maintenant :**
```bash
curl -N https://metasploitmcp.onrender.com/mcp/sse
```

### ✅ Test de Santé

Vérifier que le serveur fonctionne correctement :

```bash
# Test simple
curl https://metasploitmcp.onrender.com/healthz

# Devrait retourner
{"status":"ok","msf_version":"6.x.x"}
# ou en cas d'erreur de connexion MSF
{"detail":"Metasploit Service Unavailable: ..."}
```

### 📊 État du Déploiement

- ✅ Code poussé sur GitHub (commit 574753f)
- ⏳ Redéploiement automatique sur Render en cours
- 🔄 Les changements seront actifs dans ~2-5 minutes

### 🆘 En cas de problème

Si vous rencontrez toujours des erreurs 404 :

1. **Vérifier le déploiement Render :**
   - Aller sur https://dashboard.render.com
   - Vérifier que le service `metasploitmcp` est en cours de déploiement
   - Attendre la fin du déploiement

2. **Forcer un redéploiement manuel :**
   - Dashboard Render → Votre service → Manual Deploy → Deploy latest commit

3. **Vérifier les logs :**
   ```bash
   # Via Render Dashboard
   Dashboard → metasploitmcp → Logs
   ```

### 📝 Fichiers à Mettre à Jour (TODO)

Les fichiers suivants contiennent d'anciennes références aux endpoints et doivent être mis à jour :

- [ ] `BEGINNER_GUIDE.md`
- [ ] `ORACLE_VS_FLYIO.md`
- [ ] `RENDER_SETUP_CHECKLIST.md`
- [ ] `MISE_A_JOUR_COMPLETE.md`
- [ ] `README.md`
- [ ] `MCP_INTEGRATION_GUIDE.md`

**Rechercher et remplacer :**
- `/sse` → `/mcp/sse`
- `/messages/` → `/mcp/messages/`
