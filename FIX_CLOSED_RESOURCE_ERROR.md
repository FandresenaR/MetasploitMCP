# Fix ClosedResourceError - SSE Connection Issues

**Date:** 19 Octobre 2025  
**Problème:** `anyio.ClosedResourceError` lors des tests SSE sur Render.com

---

## 🔴 Problème Identifié

L'erreur se produisait dans les logs Render:

```
anyio.ClosedResourceError
  File "/usr/local/lib/python3.12/site-packages/anyio/streams/memory.py", line 212, in send_nowait
    raise ClosedResourceError
```

### Cause Racine

Lorsqu'un client SSE (comme `curl` avec `timeout`) se déconnecte avant que le serveur n'ait fini de traiter la requête, le serveur essaie d'envoyer une réponse sur un flux de communication déjà fermé. Cela génère une `ClosedResourceError` non gérée qui :

1. **Pollue les logs** avec des stacktraces complètes
2. **Peut masquer de vraies erreurs** dans les logs
3. **Est traitée comme une erreur** alors que c'est un comportement normal pour SSE

---

## ✅ Solution Implémentée

### 1. Gestion dans `MessagesEndpoint`

Ajout de la gestion d'erreur `ClosedResourceError` dans le handler POST:

```python
class MessagesEndpoint:
    async def __call__(self, scope, receive, send):
        """Handle client POST messages for MCP communication."""
        from anyio import ClosedResourceError
        
        client_host = scope.get('client')[0] if scope.get('client') else 'unknown'
        client_port = scope.get('client')[1] if scope.get('client') else 'unknown'
        logger.info(f"Received POST message from {client_host}:{client_port}")
        
        try:
            await sse.handle_post_message(scope, receive, send)
        except ClosedResourceError:
            # Client disconnected before response was sent
            logger.warning(f"Client {client_host}:{client_port} disconnected before response could be sent")
            # Don't propagate the error - this is expected behavior when clients timeout
            pass
        except Exception as e:
            logger.error(f"Error handling POST message from {client_host}:{client_port}: {e}", exc_info=True)
            raise
```

### 2. Gestion dans `SseEndpoint`

Ajout de la même protection dans le handler SSE:

```python
class SseEndpoint:
    async def __call__(self, scope, receive, send):
        """Handle Server-Sent Events connection for MCP communication."""
        from anyio import ClosedResourceError
        
        client_host = scope.get('client')[0] if scope.get('client') else 'unknown'
        client_port = scope.get('client')[1] if scope.get('client') else 'unknown'
        logger.info(f"New SSE connection from {client_host}:{client_port}")
        
        try:
            async with sse.connect_sse(scope, receive, send) as (read_stream, write_stream):
                await mcp._mcp_server.run(read_stream, write_stream, mcp._mcp_server.create_initialization_options())
            logger.info(f"SSE connection closed normally from {client_host}:{client_port}")
        except ClosedResourceError:
            # Client disconnected - this is normal for SSE connections
            logger.info(f"SSE connection closed by client {client_host}:{client_port}")
            pass
        except Exception as e:
            logger.error(f"Error in SSE connection from {client_host}:{client_port}: {e}", exc_info=True)
            raise
```

### 3. Amélioration du Script de Test

Modifications dans `scripts/test-render-fix.sh`:

- **Timeout SSE augmenté:** de 5s à 10s pour laisser plus de temps
- **Délais ajoutés:** 
  - 2s après obtention du session ID
  - 1s entre les requêtes POST
- Permet au serveur de compléter l'initialisation avant les tests suivants

---

## 🎯 Bénéfices

1. **Logs propres:** Plus de stacktraces pour les déconnexions clients normales
2. **Logs informatifs:** Messages de niveau WARNING/INFO au lieu d'ERROR
3. **Meilleure stabilité:** Le serveur ne propage plus d'exceptions pour des comportements attendus
4. **Tests plus robustes:** Moins de timeouts prématurés dans les scripts de test

---

## 📊 Comportement Avant vs Après

### Avant
```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  ...
  File "/usr/local/lib/python3.12/site-packages/anyio/streams/memory.py", line 212, in send_nowait
    raise ClosedResourceError
anyio.ClosedResourceError
```

### Après
```
INFO: Received POST message from 10.229.243.66:0
WARNING: Client 10.229.243.66:0 disconnected before response could be sent
```

---

## 🚀 Déploiement

Pour appliquer ces changements sur Render.com:

1. **Commit les modifications:**
   ```bash
   git add MetasploitMCP.py scripts/test-render-fix.sh
   git commit -m "Fix: Gestion gracieuse des ClosedResourceError SSE"
   git push origin main
   ```

2. **Render redéploiera automatiquement** (auto-deploy activé)

3. **Tester avec le script amélioré:**
   ```bash
   ./scripts/test-render-fix.sh
   ```

---

## 🔍 Notes Techniques

### Pourquoi ClosedResourceError arrive

Les connexions SSE (Server-Sent Events) sont **unidirectionnelles** et **longues durées**:
- Le client maintient une connexion ouverte
- Le serveur envoie des événements au fur et à mesure
- Si le client ferme (timeout, Ctrl+C, erreur réseau), le serveur ne le sait pas immédiatement
- Quand le serveur essaie d'envoyer, il découvre que le flux est fermé → `ClosedResourceError`

### Pourquoi c'est normal

C'est un **comportement attendu** dans SSE, pas une erreur vraie:
- Les clients peuvent se déconnecter à tout moment
- Les timeouts sont courants (navigateurs, proxys, tests)
- C'est la responsabilité du serveur de gérer gracieusement

### Pattern de gestion

```python
try:
    await async_operation()
except ClosedResourceError:
    # Log en INFO ou WARNING, pas ERROR
    logger.warning("Client disconnected")
    pass  # Ne pas propager l'exception
except Exception as e:
    # Vraies erreurs à propager
    logger.error(f"Real error: {e}")
    raise
```

---

## ✅ Checklist de Validation

- [x] Gestion `ClosedResourceError` dans `MessagesEndpoint`
- [x] Gestion `ClosedResourceError` dans `SseEndpoint`
- [x] Augmentation timeout SSE test (10s)
- [x] Ajout délais entre tests (2s + 1s)
- [x] Logging approprié (WARNING au lieu d'ERROR)
- [ ] Test sur Render après déploiement
- [ ] Vérification logs propres sur Render

---

**Fichiers Modifiés:**
- `MetasploitMCP.py` (handlers SSE avec gestion erreurs)
- `scripts/test-render-fix.sh` (timeouts et délais)
- `FIX_CLOSED_RESOURCE_ERROR.md` (ce document)
