# 🚨 MSFRPCD NE RÉPOND PAS - Actions Urgentes

## ⚠️ Situation Actuelle

**Problème confirmé** : Le serveur msfrpcd sur Oracle Cloud (168.110.55.210:55553) :
- ✅ Le processus tourne (selon systemd)
- ✅ Le port 55553 est ouvert
- ❌ **NE RÉPOND PAS** aux requêtes

## 🔥 Action Immédiate Requise

Vous devez vous connecter **manuellement** au serveur Oracle Cloud pour diagnostiquer.

```bash
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210
```

## 📋 Commandes de Diagnostic à Exécuter

### 1. Vérifier le processus

```bash
# Voir tous les processus msfrpcd
ps aux | grep [m]sfrpcd

# Voir le processus avec la commande complète
ps -ef | grep [m]sfrpcd

# Nombre de processus
pgrep -c msfrpcd
```

### 2. Vérifier le port

```bash
# Qui écoute sur le port 55553 ?
sudo netstat -tlnp | grep 55553
# OU
sudo ss -tlnp | grep 55553
```

### 3. Vérifier les logs systemd

```bash
# Derniers logs
sudo journalctl -u msfrpcd -n 50

# Logs en temps réel
sudo journalctl -u msfrpcd -f
```

### 4. Tester localement depuis le serveur

```bash
# Test simple
curl -v http://localhost:55553/api/

# Test avec authentification
curl -X POST http://localhost:55553/api/ \
  -H "Content-Type: application/json" \
  -d '{"method":"auth.login","params":["msf","MetasploitRPC2025_SecurePass!"]}'
```

## 🔧 Solutions Possibles

### Solution 1 : Le processus est planté

```bash
# Arrêter complètement
sudo systemctl stop msfrpcd
sudo pkill -9 msfrpcd
sudo pkill -9 ruby  # Attention : tue tous les processus ruby !

# Redémarrer
sudo systemctl start msfrpcd

# Suivre le démarrage
sudo journalctl -u msfrpcd -f
```

Attendez jusqu'à voir :
```
[*] MSGRPC starting on 0.0.0.0:55553
[*] MSGRPC ready at ...
```

### Solution 2 : Démarrer manuellement (debug)

```bash
# Arrêter le service
sudo systemctl stop msfrpcd

# Démarrer manuellement pour voir les erreurs
cd /home/ubuntu/metasploit-framework
./msfrpcd -f -a 0.0.0.0 -p 55553 -U msf -P "MetasploitRPC2025_SecurePass!"
```

Vous verrez les erreurs en temps réel. Cherchez :
- `Error binding to port` → Port déjà utilisé
- `Failed to start` → Problème de configuration
- Aucune sortie → Le processus est bloqué

### Solution 3 : Changer le port

Si le port 55553 a un problème, essayez 55554 :

```bash
# Éditer le service
sudo nano /etc/systemd/system/msfrpcd.service

# Changer `-p 55553` par `-p 55554`

# Recharger et redémarrer
sudo systemctl daemon-reload
sudo systemctl restart msfrpcd

# Vérifier
sudo netstat -tlnp | grep 55554
```

Puis mettre à jour `.env.local` :
```bash
MSF_PORT=55554
```

### Solution 4 : Réinstaller Metasploit

Si rien ne fonctionne :

```bash
# Sauvegarder la config
cp -r ~/.msf4 ~/.msf4.backup

# Mettre à jour Metasploit
cd /home/ubuntu/metasploit-framework
git pull
bundle install

# Redémarrer msfrpcd
sudo systemctl restart msfrpcd
```

## 🐛 Problèmes Connus

### Problème : "Address already in use"

```bash
# Trouver qui utilise le port
sudo lsof -i :55553

# Tuer le processus
sudo kill -9 <PID>
```

### Problème : "Permission denied"

```bash
# Vérifier les permissions
ls -la /home/ubuntu/metasploit-framework/msfrpcd

# Si nécessaire
chmod +x /home/ubuntu/metasploit-framework/msfrpcd
```

### Problème : "LoadError: cannot load such file"

```bash
cd /home/ubuntu/metasploit-framework
bundle install
```

## 📊 Tests de Validation

### Test 1 : Depuis le serveur Oracle

```bash
curl -X POST http://localhost:55553/api/ \
  -H "Content-Type: application/json" \
  -d '{"method":"core.version","params":[]}'
```

**Résultat attendu** :
```json
{"version":"6.x.x","ruby":"ruby 3.x.x","api":"1.0"}
```

### Test 2 : Depuis votre machine locale

```bash
cd /home/twain/Project/MetasploitMCP
source venv/bin/activate
python3 test_oracle_direct.py
```

**Résultat attendu** :
```
✅ SUCCÈS ! Connexion établie
   Version: 6.4.95-dev-
```

## 🆘 Si Rien ne Fonctionne

### Option A : Utiliser un tunnel SSH

Au lieu d'exposer msfrpcd publiquement :

```bash
# Sur votre machine locale
ssh -i ~/.ssh/oracle_metasploit_key -L 55553:localhost:55553 ubuntu@168.110.55.210 -N -f

# Mettre à jour .env.local
MSF_SERVER=127.0.0.1
MSF_PORT=55553
```

### Option B : Déployer msfrpcd localement

Installer Metasploit Framework localement :

```bash
# Sur votre machine Kali
sudo apt update
sudo apt install metasploit-framework

# Démarrer msfrpcd localement
msfrpcd -P "VotreMotDePasse" -a 127.0.0.1 -p 55553

# Mettre à jour .env.local
MSF_SERVER=127.0.0.1
MSF_PORT=55553
MSF_PASSWORD=VotreMotDePasse
MSF_SSL=false
```

## 📞 Partager les Résultats

Après avoir exécuté les diagnostics, partagez :

1. **Sortie de** : `sudo journalctl -u msfrpcd -n 50`
2. **Sortie de** : `ps aux | grep msfrpcd`
3. **Sortie de** : `sudo netstat -tlnp | grep 55553`
4. **Sortie du test local** : `curl http://localhost:55553/api/`

Cela aidera à identifier le problème précis.
