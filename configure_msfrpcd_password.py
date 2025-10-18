#!/usr/bin/env python3
"""Script interactif pour tester et configurer le mot de passe MSFRPCD"""

import os
import sys
from getpass import getpass
from pymetasploit3.msfrpc import MsfRpcClient

def test_password(server, port, password, ssl=True):
    """Tester un mot de passe spécifique"""
    try:
        client = MsfRpcClient(
            password=password,
            server=server,
            port=int(port),
            ssl=ssl
        )
        version = client.core.version
        return True, version
    except Exception as e:
        return False, str(e)

def update_env_file(password):
    """Mettre à jour le fichier .env.local avec le bon mot de passe"""
    env_path = '.env.local'
    
    if not os.path.exists(env_path):
        print(f"❌ Fichier {env_path} introuvable")
        return False
    
    # Lire le contenu actuel
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Remplacer la ligne MSF_PASSWORD
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('MSF_PASSWORD='):
            lines[i] = f'MSF_PASSWORD={password}\n'
            updated = True
            break
    
    if not updated:
        print("⚠️  MSF_PASSWORD non trouvé dans .env.local, ajout...")
        lines.append(f'\nMSF_PASSWORD={password}\n')
    
    # Écrire le fichier mis à jour
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Fichier {env_path} mis à jour")
    return True

def main():
    print("="*70)
    print("🔐 TEST ET CONFIGURATION DU MOT DE PASSE MSFRPCD")
    print("="*70)
    print()
    
    server = '168.110.55.210'
    port = 55553
    
    print(f"Serveur cible : {server}:{port}")
    print()
    
    # Essayer d'abord le mot de passe du .env.local
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    current_password = os.getenv('MSF_PASSWORD', '')
    
    if current_password and current_password != 'your_secure_password_here':
        print("🔍 Test avec le mot de passe actuel de .env.local...")
        success, result = test_password(server, port, current_password)
        if success:
            print(f"✅ SUCCÈS ! Le mot de passe actuel fonctionne")
            print(f"   Version Metasploit : {result.get('version', 'unknown')}")
            print(f"   API Version : {result.get('api', 'unknown')}")
            return
        else:
            print(f"❌ Échec : {result}")
            print()
    
    # Demander un nouveau mot de passe
    print("Veuillez entrer le mot de passe MSFRPCD du serveur Oracle Cloud")
    print("(Vous pouvez le trouver avec: ssh ubuntu@168.110.55.210 'ps aux | grep msfrpcd')")
    print()
    
    while True:
        password = getpass("Mot de passe MSFRPCD : ")
        
        if not password:
            print("❌ Le mot de passe ne peut pas être vide")
            continue
        
        print(f"\n🔍 Test de connexion avec le mot de passe fourni...")
        success, result = test_password(server, port, password)
        
        if success:
            print(f"\n✅ SUCCÈS ! Connexion établie")
            print(f"   Version Metasploit : {result.get('version', 'unknown')}")
            print(f"   API Version : {result.get('api', 'unknown')}")
            print()
            
            # Demander si on met à jour .env.local
            response = input("Voulez-vous sauvegarder ce mot de passe dans .env.local ? (o/N) : ").lower()
            if response in ['o', 'oui', 'y', 'yes']:
                if update_env_file(password):
                    print("\n🎉 Configuration terminée avec succès !")
                    print("\nProchaines étapes :")
                    print("1. Tester localement : python3 test_oracle_direct.py")
                    print("2. Configurer Render avec les mêmes credentials")
                    print("3. Variables Render à définir :")
                    print(f"   - MSF_SERVER={server}")
                    print(f"   - MSF_PORT={port}")
                    print(f"   - MSF_PASSWORD=<le_mot_de_passe_qui_fonctionne>")
                    print(f"   - MSF_SSL=true")
            break
        else:
            print(f"\n❌ Échec : {result}")
            print()
            response = input("Voulez-vous réessayer avec un autre mot de passe ? (O/n) : ").lower()
            if response in ['n', 'non', 'no']:
                print("\n⚠️  Configuration non terminée")
                print("\nPour récupérer le bon mot de passe :")
                print(f"1. ssh -i ~/.ssh/oracle_metasploit_key ubuntu@{server}")
                print("2. ps aux | grep msfrpcd")
                print("3. Le mot de passe apparaît après l'option -P")
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Opération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
