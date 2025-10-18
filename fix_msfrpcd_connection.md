# 🔧 Guide de Correction de la Connexion MSFRPCD

## 📊 Diagnostic Actuel

D'après les tests effectués :

| Test | Résultat | Signification |
|------|----------|---------------|
| Local (127.0.0.1:55553) | ❌ Connection refused | Pas de msfrpcd local / tunnel SSH inactif |
| Oracle (168.110.55.210:55553) | ❌ Authentication failed | msfrpcd actif MAIS mot de passe incorrect |

## ✅ Bonne Nouvelle

Le serveur msfrpcd sur Oracle Cloud **fonctionne et est accessible** ! Il suffit de corriger le mot de passe.

## 🔑 Solution : Récupérer le Bon Mot de Passe

### Option 1 : Vérifier le mot de passe sur le serveur Oracle

```bash
# Se connecter au serveur Oracle
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# Vérifier le processus msfrpcd
ps aux | grep msfrpcd

# Le mot de passe apparaîtra dans la ligne de commande
# Exemple : msfrpcd -P VOTRE_MOT_DE_PASSE -S -a 0.0.0.0 -p 55553
```

### Option 2 : Redémarrer msfrpcd avec un nouveau mot de passe

```bash
# Sur le serveur Oracle Cloud
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# Arrêter msfrpcd actuel
sudo pkill msfrpcd

# Choisir un nouveau mot de passe (exemple: MySecurePass123!)
export NEW_PASSWORD="MySecurePass123!"

# Redémarrer msfrpcd avec le nouveau mot de passe
msfrpcd -P "$NEW_PASSWORD" -S -a 0.0.0.0 -p 55553 -n

# Vérifier que ça tourne
ps aux | grep msfrpcd
```

### Option 3 : Utiliser systemd pour gérer msfrpcd

```bash
# Sur le serveur Oracle Cloud
ssh -i ~/.ssh/oracle_metasploit_key ubuntu@168.110.55.210

# Créer un service systemd
sudo nano /etc/systemd/system/msfrpcd.service
```

Contenu du fichier :

```ini
[Unit]
Description=Metasploit Framework RPC Daemon
After=network.target

[Service]
Type=simple
User=ubuntu
Environment="MSF_PASSWORD=VotreMotDePasseSecurise"
ExecStart=/usr/bin/msfrpcd -P ${MSF_PASSWORD} -S -a 0.0.0.0 -p 55553 -n
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Puis activer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable msfrpcd
sudo systemctl start msfrpcd
sudo systemctl status msfrpcd
```

## 📝 Mettre à Jour .env.local

Une fois le bon mot de passe récupéré :

```bash
# Dans votre projet local
cd /home/twain/Project/MetasploitMCP
nano .env.local
```

Mettre à jour :

```bash
MSF_PASSWORD=VOTRE_BON_MOT_DE_PASSE
MSF_SERVER=168.110.55.210
MSF_PORT=55553
MSF_SSL=true
```

## 🧪 Tester la Connexion

```bash
# Retester avec le nouveau mot de passe
python3 test_oracle_direct.py
```

Vous devriez voir :

```
TEST 2: Connexion Oracle Cloud (168.110.55.210)
============================================================
🔍 Test de connexion à 168.110.55.210:55553
   SSL: True

✅ SUCCÈS ! Connexion établie
   Version: 6.x.x
   API: 1.0
```

## 🚀 Configurer Render

Une fois la connexion locale validée, configurer Render :

1. Aller sur https://dashboard.render.com
2. Sélectionner votre service `metasploitmcp`
3. Aller dans **Environment**
4. Ajouter/Modifier les variables :
   - `MSF_SERVER` = `168.110.55.210`
   - `MSF_PORT` = `55553`
   - `MSF_PASSWORD` = `VOTRE_BON_MOT_DE_PASSE`
   - `MSF_SSL` = `true`
5. Sauvegarder → Redéploiement automatique

## ⚠️ Sécurité

**IMPORTANT** : Si msfrpcd est exposé publiquement sur Internet (0.0.0.0:55553), assurez-vous de :

1. **Utiliser un mot de passe très fort** (20+ caractères, aléatoire)
2. **Configurer le firewall Oracle Cloud** pour n'autoriser que :
   - Votre IP locale
   - Les IP de Render.com (si possible)
3. **Surveiller les logs** régulièrement
4. **Utiliser SSL** (déjà fait avec `-S`)

### Configurer le Firewall Oracle Cloud

```bash
# Sur Oracle Cloud Dashboard
Security Lists → Default Security List
→ Ingress Rules → Add Rule

Source CIDR: VOTRE_IP/32  # Remplacer par votre IP
Protocol: TCP
Port: 55553
Description: MSFRPCD - Mon IP uniquement
```

## 🔄 Alternative : Tunnel SSH

Si vous préférez ne pas exposer msfrpcd publiquement :

```bash
# Sur votre machine locale, créer un tunnel SSH
ssh -i ~/.ssh/oracle_metasploit_key -L 55553:localhost:55553 ubuntu@168.110.55.210 -N -f

# Puis dans .env.local
MSF_SERVER=127.0.0.1
MSF_PORT=55553
```

Cette approche est **plus sécurisée** mais nécessite que le tunnel soit toujours actif.
