#!/bin/bash
# Script pour récupérer le mot de passe MSFRPCD sur le serveur Oracle Cloud

echo "============================================================"
echo "🔍 RÉCUPÉRATION DU MOT DE PASSE MSFRPCD"
echo "============================================================"
echo ""

SERVER="168.110.55.210"
KEY="$HOME/.ssh/oracle_metasploit_key"

echo "Connexion au serveur Oracle Cloud ($SERVER)..."
echo ""

# Vérifier si la clé SSH existe
if [ ! -f "$KEY" ]; then
    echo "❌ Clé SSH introuvable : $KEY"
    echo "Veuillez vérifier le chemin de votre clé SSH"
    exit 1
fi

echo "1️⃣  Vérification du processus msfrpcd..."
echo "---"
ssh -i "$KEY" ubuntu@$SERVER "ps aux | grep '[m]sfrpcd'" || {
    echo ""
    echo "❌ msfrpcd ne semble pas être en cours d'exécution"
    echo ""
    echo "Pour le démarrer :"
    echo "  ssh -i $KEY ubuntu@$SERVER"
    echo "  msfrpcd -P VotreMotDePasse -S -a 0.0.0.0 -p 55553 -n"
    exit 1
}

echo ""
echo "2️⃣  Extraction du mot de passe..."
echo "---"

PASSWORD=$(ssh -i "$KEY" ubuntu@$SERVER "ps aux | grep '[m]sfrpcd' | grep -oP '(?<=-P )[^ ]+' | head -1")

if [ -n "$PASSWORD" ]; then
    echo "✅ Mot de passe trouvé : $PASSWORD"
    echo ""
    echo "============================================================"
    echo "📋 INFORMATIONS DE CONNEXION"
    echo "============================================================"
    echo "Serveur   : $SERVER"
    echo "Port      : 55553"
    echo "Mot de passe : $PASSWORD"
    echo "SSL       : true"
    echo ""
    echo "Vous pouvez maintenant :"
    echo "1. Tester avec : python3 configure_msfrpcd_password.py"
    echo "2. Ou mettre à jour .env.local manuellement"
    echo ""
else
    echo "⚠️  Impossible d'extraire le mot de passe automatiquement"
    echo ""
    echo "Le processus msfrpcd tourne, mais le format est inhabituel."
    echo "Commande trouvée :"
    ssh -i "$KEY" ubuntu@$SERVER "ps aux | grep '[m]sfrpcd'"
    echo ""
    echo "Connectez-vous manuellement pour vérifier :"
    echo "  ssh -i $KEY ubuntu@$SERVER"
    echo "  ps aux | grep msfrpcd"
fi
