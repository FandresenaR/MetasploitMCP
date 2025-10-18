# 🔧 Diagnostic et Solution - Problème de Connexion MSFRPCD

## 📊 Résumé du Diagnostic

| Test | Résultat | Conclusion |
|------|----------|------------|
| Port 55553 TCP accessible | ✅ Ouvert | Le firewall laisse passer |
| Connexion TCP établie | ✅ Réussit | Le serveur accepte les connexions |
| Réponse HTTP | ❌ Timeout | msfrpcd ne répond pas |
| Service systemd | ⚠️  Actif mais peut-être planté | Nécessite vérification |

## 🔍 Découvertes

1. **Mot de passe trouvé** : `MetasploitRPC2025_SecurePass!`
2. **Service systemd actif** : Le service tourne selon systemd
3. **Port ouvert** : 55553/TCP est accessible
4. **Pas de réponse** : msfrpcd ne répond pas aux requêtes HTTP

## ⚠️  Problème Probable

Le processus msfrpcd est probablement :
- **Planté/gelé** : Le processus existe mais ne répond plus
- **Mal configuré** : N'écoute pas sur la bonne interface
- **Incomplet** : Le démarrage n'est pas terminé

## ✅ Solution : Redémarrer Proprement MSFRPCD

### Étape 1 : Connexion au serveur

```bash
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210
```

###Étape 2 : Arrêter le service actuel

```bash
# Arrêter le service
sudo systemctl stop msfrpcd

# Tuer tous les processus msfrpcd résiduels
sudo pkill -9 msfrpcd

# Vérifier qu'il n'y a plus de processus
ps aux | grep msfrpcd
```

### Étape 3 : Vérifier/Corriger le service systemd

```bash
# Afficher le fichier de service
sudo cat /etc/systemd/system/msfrpcd.service
```

**Problème potentiel** : L'option `-S` (SSL) peut causer des problèmes.

**Service corrigé (SANS SSL)** :

```ini
[Unit]
Description=Metasploit RPC Daemon
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStartPre=/bin/sleep 5
ExecStart=/home/ubuntu/.rbenv/shims/ruby /home/ubuntu/metasploit-framework/msfrpcd -f -a 0.0.0.0 -p 55553 -U msf -P MetasploitRPC2025_SecurePass!
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Note** : J'ai retiré l'option `-S` (SSL) car elle cause des problèmes. Si vous voulez SSL, il faut d'abord générer des certificats.

Appliquer :

```bash
# Éditer le fichier
sudo nano /etc/systemd/system/msfrpcd.service
# (Coller le contenu ci-dessus)

# Recharger systemd
sudo systemctl daemon-reload

# Démarrer le service
sudo systemctl start msfrpcd

# Vérifier le statut
sudo systemctl status msfrpcd

# Suivre les logs en temps réel
sudo journalctl -u msfrpcd -f
```

### Étape 4 : Attendre le démarrage complet

msfrpcd peut prendre **30-60 secondes** pour démarrer complètement. Attendez jusqu'à voir dans les logs :

```
[*] MSGRPC starting on 0.0.0.0:55553 (NO SSL)
[*] MSGRPC ready at 2025-XX-XX XX:XX:XX
```

### Étape 5 : Tester depuis le serveur local

```bash
# Sur le serveur Oracle
curl -v -X POST http://localhost:55553/api/ \
  -d '{"method":"auth.login","params":["msf","MetasploitRPC2025_SecurePass!"]}' \
  -H "Content-Type: application/json"
```

Vous devriez voir :

```json
{"result":"success","token":"XXXXX"}
```

### Étape 6 : Tester depuis votre machine locale

```bash
# Sur votre machine
cd /home/twain/Project/MetasploitMCP
source venv/bin/activate
python3 test_oracle_direct.py
```

Vous devriez voir :

```
✅ SUCCÈS ! Connexion établie
   Version: 6.4.95-dev-
   API Version: 1.0
```

## 🔒 Alternative : Activer SSL Proprement

Si vous voulez vraiment SSL, il faut générer des certificats SSL :

```bash
# Sur le serveur Oracle
cd ~
mkdir -p .msf4/ssl
cd .msf4/ssl

# Générer une clé privée
openssl genrsa -out server.key 2048

# Générer un certificat auto-signé
openssl req -new -x509 -key server.key -out server.crt -days 365 \
  -subj "/C=US/ST=State/L=City/O=Org/CN=metasploit"

# Combiner en PEM
cat server.key server.crt > server.pem
chmod 600 server.pem
```

Puis modifier le service pour ajouter l'option `-S` :

```ini
ExecStart=/home/ubuntu/.rbenv/shims/ruby /home/ubuntu/metasploit-framework/msfrpcd -f -S -a 0.0.0.0 -p 55553 -U msf -P MetasploitRPC2025_SecurePass!
```

Et dans `.env.local` :

```bash
MSF_SSL=true
```

## 📋 Checklist

- [  ] SSH vers le serveur Oracle
- [ ] Arrêter msfrpcd (systemctl stop + pkill)
- [ ] Vérifier/Corriger /etc/systemd/system/msfrpcd.service
- [ ] systemctl daemon-reload
- [ ] systemctl start msfrpcd
- [ ] Attendre 60 secondes
- [ ] Vérifier les logs (journalctl -u msfrpcd -f)
- [ ] Tester localement (curl depuis le serveur)
- [ ] Tester à distance (python3 test_oracle_direct.py)
- [ ] Si succès : configurer Render avec les mêmes paramètres

## 🚀 Configuration Render (après validation)

Une fois la connexion validée localement, configurer Render :

```bash
MSF_SERVER=168.110.55.210
MSF_PORT=55553
MSF_PASSWORD=MetasploitRPC2025_SecurePass!
MSF_SSL=false  # ou true si vous activez SSL
```

## 📝 Notes

- **Sécurité** : msfrpcd sans SSL est vulnérable. À utiliser uniquement pour les tests.
- **Production** : Utilisez SSL + Firewall restrictif
- **Firewall Oracle** : Actuellement 55553 est ouvert publiquement - à restreindre !
