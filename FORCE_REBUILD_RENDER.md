# 🚨 FORCER UN REBUILD COMPLET SUR RENDER.COM

## Problème Confirmé

Les logs du nouveau service `metasploitmcp-1` montrent :
```
File "/app/MetasploitMCP.py", line 1939, in __call__
anyio.ClosedResourceError
```

**Preuve du problème** : La ligne 1939 n'existe QUE dans l'ancien code !
- Code local (correct) : **2094 lignes**
- Code Render (corrompu) : **~2114 lignes** (avec monkeypatch)

## 🎯 Solution Immédiate

### Option 1 : Modifier le Dockerfile (RECOMMANDÉ)

Ajoutez une ligne de "cache bust" dans le Dockerfile pour forcer un rebuild :

1. Ouvrir `Dockerfile` dans le projet
2. Ajouter juste après la ligne `FROM python:3.12-slim` :
   ```dockerfile
   # Force rebuild: 2025-10-19-21:05
   RUN echo "Build timestamp: $(date)"
   ```

3. Commiter et pusher :
   ```bash
   git add Dockerfile
   git commit -m "Force rebuild with timestamp"
   git push
   ```

### Option 2 : Supprimer et Recréer le Service

Si Option 1 ne fonctionne pas :

1. **Supprimer complètement** le service `metasploitmcp-1` sur Render.com
2. Attendre 5 minutes (pour que le cache soit vraiment libéré)
3. Créer un **NOUVEAU** service avec un nom différent : `metasploitmcp-fixed`
4. Vérifier que :
   - Branch = `main`
   - Build Command = (vide)
   - Start Command = `python MetasploitMCP.py --transport http --host 0.0.0.0 --port $PORT`

### Option 3 : Modifier le Build Command

Dans le dashboard Render.com pour `metasploitmcp-1` :

1. Aller dans **Settings** → **Build & Deploy**
2. **Build Command** : 
   ```bash
   pip cache purge && pip install --no-cache-dir -r requirements.txt
   ```
3. Sauvegarder
4. **Manual Deploy** → Cocher "Clear build cache"

## ✅ Vérification

Après le rebuild, le serveur NE DOIT PAS avoir d'erreur à la ligne 1939 :

```bash
# Test rapide
curl -s https://metasploitmcp-1.onrender.com/healthz

# Test complet
./scripts/test-render-fix.sh
```

**Résultat attendu** :
- ✅ Health check: OK
- ✅ Session SSE: OK
- ✅ Tools list: JSON-RPC (PAS "Accepted")
- ✅ Tool call: JSON-RPC (PAS "Accepted")

## 📊 Logs à Surveiller

Dans les logs Render.com après rebuild, chercher :

❌ **Mauvais signe** (ancien code) :
```
File "/app/MetasploitMCP.py", line 1939
anyio.ClosedResourceError
```

✅ **Bon signe** (nouveau code) :
```
INFO: Application startup complete
(Pas d'erreur ClosedResourceError)
```

## 🔧 Code Local (Vérification)

Le code local est correct :
```bash
grep -n "ServerSession._received_request" MetasploitMCP.py
# Doit retourner : (rien) = Monkeypatch supprimé ✅

wc -l MetasploitMCP.py
# Doit retourner : 2094 MetasploitMCP.py ✅
```

## 📝 Historique

- **19:50** : Bug découvert (ligne 1938)
- **19:52** : Code corrigé localement (commit 0bce836)
- **20:00-20:42** : 7 tentatives de déploiement (ÉCHEC cache)
- **20:50** : Nouveau service créé (metasploitmcp-1)
- **21:01** : MÊME PROBLÈME ligne 1939 sur nouveau service
- **21:05** : Solution : Forcer rebuild avec Dockerfile ou recréer service

---

**Date** : 19 octobre 2025 21:05  
**Status** : Cache Docker Render.com corrompu sur nouveau service  
**Action** : Forcer rebuild complet avec Option 1, 2 ou 3
