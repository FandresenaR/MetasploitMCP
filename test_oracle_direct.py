#!/usr/bin/env python3
"""Test de connexion DIRECTE à MSFRPCD sur Oracle Cloud"""

import os
from dotenv import load_dotenv
from pymetasploit3.msfrpc import MsfRpcClient

# Charger les variables d'environnement
load_dotenv('.env.local')

def test_connection(server, port, password, ssl):
    """Tester la connexion à MSFRPCD"""
    print(f"🔍 Test de connexion à {server}:{port}")
    print(f"   SSL: {ssl}")
    print()
    
    try:
        client = MsfRpcClient(
            password=password,
            server=server,
            port=int(port),
            ssl=ssl
        )
        
        version = client.core.version
        print(f"✅ SUCCÈS ! Connexion établie")
        print(f"   Version: {version.get('version', 'unknown')}")
        print(f"   API: {version.get('api', 'unknown')}")
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC : {e}")
        return False

if __name__ == "__main__":
    password = os.getenv('MSF_PASSWORD', 'your_secure_password_here')
    ssl_setting = os.getenv('MSF_SSL', 'true').lower() == 'true'
    
    print("="*60)
    print("TEST 1: Connexion locale (127.0.0.1)")
    print("="*60)
    test_connection('127.0.0.1', 55553, password, ssl_setting)
    
    print("\n" + "="*60)
    print("TEST 2: Connexion Oracle Cloud (168.110.55.210)")
    print("="*60)
    test_connection('168.110.55.210', 55553, password, ssl_setting)
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print("""
Si TEST 1 réussit : msfrpcd tourne en local (tunnel SSH actif)
Si TEST 2 réussit : msfrpcd est accessible publiquement sur Oracle
Si les 2 échouent : msfrpcd n'est pas démarré ou mal configuré
    """)
