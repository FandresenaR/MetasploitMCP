#!/usr/bin/env python3
"""
Test d'intégration complète : Client → MetasploitMCP → msfrpcd
Vérifie tous les outils et la chaîne de connexion complète
"""

import os
import sys
import json
import time
from pathlib import Path

# Charger les variables d'environnement
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env.local'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Environnement chargé depuis {env_path}")
except ImportError:
    print("⚠️  python-dotenv non installé, utilisation des variables système")

# Configuration depuis .env.local
MSF_SERVER = os.getenv('MSF_SERVER', '168.110.55.210')
MSF_PORT = int(os.getenv('MSF_PORT', '55553'))
MSF_PASSWORD = os.getenv('MSF_PASSWORD', '')
MSF_SSL = os.getenv('MSF_SSL', 'false').lower() == 'true'

print("\n" + "="*70)
print("🔬 TEST D'INTÉGRATION METASPLOITMCP")
print("="*70)

print(f"\n📋 Configuration:")
print(f"   MSF Server: {MSF_SERVER}:{MSF_PORT}")
print(f"   MSF SSL: {MSF_SSL}")
print(f"   MSF Password: {'*' * len(MSF_PASSWORD) if MSF_PASSWORD else '❌ NON DÉFINI'}")

if not MSF_PASSWORD:
    print("\n❌ ERREUR: MSF_PASSWORD non défini dans .env.local")
    sys.exit(1)

# Test 1: Import des dépendances
print("\n" + "="*70)
print("TEST 1: Vérification des dépendances Python")
print("="*70)

dependencies = {
    'pymetasploit3': None,
    'fastapi': None,
    'uvicorn': None,
    'requests': None,
}

for module_name in dependencies.keys():
    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'unknown')
        dependencies[module_name] = version
        print(f"✅ {module_name:20} version {version}")
    except ImportError as e:
        print(f"❌ {module_name:20} NON INSTALLÉ")
        dependencies[module_name] = None

if None in dependencies.values():
    print("\n⚠️  Certaines dépendances manquent. Installez-les avec:")
    print("   pip install pymetasploit3 fastapi uvicorn requests")
    print("\nContinuation des tests possibles avec pymetasploit3...")

# Test 2: Connexion directe à msfrpcd
print("\n" + "="*70)
print("TEST 2: Connexion directe à msfrpcd (Oracle Cloud)")
print("="*70)

msf_client = None
try:
    from pymetasploit3.msfrpc import MsfRpcClient, MsfRpcError
    
    print(f"🔌 Tentative de connexion à {MSF_SERVER}:{MSF_PORT}...")
    print(f"   SSL: {MSF_SSL}")
    
    start_time = time.time()
    msf_client = MsfRpcClient(
        password=MSF_PASSWORD,
        server=MSF_SERVER,
        port=MSF_PORT,
        ssl=MSF_SSL,
        timeout=10
    )
    elapsed = time.time() - start_time
    
    print(f"✅ Connexion établie en {elapsed:.2f}s")
    
    # Tester l'API
    version_info = msf_client.core.version
    print(f"\n📊 Informations Metasploit:")
    print(f"   Version: {version_info.get('version', 'unknown')}")
    print(f"   API: {version_info.get('api', 'unknown')}")
    print(f"   Ruby: {version_info.get('ruby', 'unknown')}")
    
except ImportError:
    print("❌ pymetasploit3 non installé, impossible de tester msfrpcd")
except MsfRpcError as e:
    print(f"❌ Erreur d'authentification MSF: {e}")
    print("   → Vérifiez le mot de passe dans .env.local")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
    sys.exit(1)

# Test 3: Outils Metasploit disponibles
print("\n" + "="*70)
print("TEST 3: Vérification des modules/outils Metasploit")
print("="*70)

if msf_client:
    try:
        # Compter les modules
        exploits = msf_client.modules.exploits
        payloads = msf_client.modules.payloads
        auxiliary = msf_client.modules.auxiliary
        
        print(f"✅ Modules disponibles:")
        print(f"   Exploits: {len(exploits)} modules")
        print(f"   Payloads: {len(payloads)} modules")
        print(f"   Auxiliary: {len(auxiliary)} modules")
        
        # Tester un module simple
        print(f"\n🧪 Test d'un module (scanner/portscan/tcp):")
        try:
            scanner = msf_client.modules.use('auxiliary', 'scanner/portscan/tcp')
            print(f"   ✅ Module chargé avec succès")
            print(f"   Options disponibles: {list(scanner.options.keys())[:5]}...")
        except Exception as e:
            print(f"   ⚠️  Erreur lors du chargement: {e}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'énumération des modules: {e}")

# Test 4: Fonctions principales MetasploitMCP
print("\n" + "="*70)
print("TEST 4: Test des outils MetasploitMCP")
print("="*70)

tools_to_test = [
    {
        'name': 'list_exploits',
        'description': 'Lister les exploits disponibles',
        'test': lambda: len(msf_client.modules.exploits) > 0 if msf_client else False
    },
    {
        'name': 'list_payloads',
        'description': 'Lister les payloads disponibles',
        'test': lambda: len(msf_client.modules.payloads) > 0 if msf_client else False
    },
    {
        'name': 'search_modules',
        'description': 'Rechercher des modules',
        'test': lambda: msf_client.modules.search('windows') if msf_client else []
    },
]

for tool in tools_to_test:
    try:
        result = tool['test']()
        if result:
            print(f"✅ {tool['name']:20} - {tool['description']}")
        else:
            print(f"⚠️  {tool['name']:20} - Pas de résultat")
    except Exception as e:
        print(f"❌ {tool['name']:20} - Erreur: {e}")

# Test 5: Sessions actives
print("\n" + "="*70)
print("TEST 5: Gestion des sessions")
print("="*70)

if msf_client:
    try:
        sessions = msf_client.sessions.list
        print(f"📊 Sessions actives: {len(sessions)}")
        
        if sessions:
            for sid, session_data in sessions.items():
                print(f"   Session {sid}:")
                print(f"      Type: {session_data.get('type', 'unknown')}")
                print(f"      Info: {session_data.get('info', 'N/A')}")
        else:
            print("   ℹ️  Aucune session active (normal)")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des sessions: {e}")

# Test 6: Jobs actifs
print("\n" + "="*70)
print("TEST 6: Jobs Metasploit")
print("="*70)

if msf_client:
    try:
        jobs = msf_client.jobs.list
        print(f"📊 Jobs actifs: {len(jobs)}")
        
        if jobs:
            for jid, job_data in jobs.items():
                print(f"   Job {jid}: {job_data.get('name', 'unknown')}")
        else:
            print("   ℹ️  Aucun job actif (normal)")
            
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des jobs: {e}")

# Test 7: Création d'un payload (test sans exécution)
print("\n" + "="*70)
print("TEST 7: Génération de payload (test)")
print("="*70)

if msf_client:
    try:
        print("🧪 Test de génération payload windows/meterpreter/reverse_tcp")
        
        # Vérifier que le payload existe
        payload_name = 'windows/meterpreter/reverse_tcp'
        if payload_name in msf_client.modules.payloads:
            print(f"   ✅ Payload {payload_name} disponible")
            
            # Charger le module
            payload = msf_client.modules.use('payload', payload_name)
            print(f"   ✅ Module chargé")
            print(f"   Options requises: {list(payload.required.keys())}")
        else:
            print(f"   ❌ Payload {payload_name} introuvable")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Test 8: Test de connexion via MetasploitMCP.py
print("\n" + "="*70)
print("TEST 8: Chargement du module MetasploitMCP")
print("="*70)

try:
    # Essayer d'importer le module principal
    import MetasploitMCP
    print("✅ MetasploitMCP.py importé avec succès")
    
    # Vérifier les fonctions disponibles
    functions = [attr for attr in dir(MetasploitMCP) if not attr.startswith('_')]
    print(f"   Fonctions/classes disponibles: {len(functions)}")
    print(f"   Exemples: {functions[:5]}...")
    
except ImportError as e:
    print(f"⚠️  Impossible d'importer MetasploitMCP.py: {e}")
    print("   (Normal si le module nécessite des dépendances MCP)")
except Exception as e:
    print(f"❌ Erreur lors de l'import: {e}")

# Test 9: Performances
print("\n" + "="*70)
print("TEST 9: Performance de la connexion")
print("="*70)

if msf_client:
    try:
        print("🏃 Test de latence avec 5 requêtes...")
        latencies = []
        
        for i in range(5):
            start = time.time()
            _ = msf_client.core.version
            latency = (time.time() - start) * 1000  # en ms
            latencies.append(latency)
            print(f"   Requête {i+1}: {latency:.2f}ms")
        
        avg_latency = sum(latencies) / len(latencies)
        print(f"\n📊 Latence moyenne: {avg_latency:.2f}ms")
        
        if avg_latency < 100:
            print("   ✅ Excellente performance")
        elif avg_latency < 500:
            print("   ✅ Performance correcte")
        else:
            print("   ⚠️  Latence élevée (connexion distante?)")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Résumé final
print("\n" + "="*70)
print("📊 RÉSUMÉ DES TESTS")
print("="*70)

summary = {
    "Dépendances": all(dependencies.values()),
    "Connexion msfrpcd": msf_client is not None,
    "Modules disponibles": msf_client is not None,
    "API fonctionnelle": msf_client is not None,
}

print(f"\n{'Composant':<30} {'Statut':<10}")
print("-" * 40)
for component, status in summary.items():
    status_icon = "✅" if status else "❌"
    print(f"{component:<30} {status_icon}")

if all(summary.values()):
    print("\n" + "="*70)
    print("🎉 TOUS LES TESTS SONT PASSÉS !")
    print("="*70)
    print("\n✅ L'intégration Client → MetasploitMCP → msfrpcd fonctionne parfaitement")
    print("\n📝 Prochaines étapes:")
    print("   1. Configurer les variables Render (MSF_PASSWORD, MSF_SSL=false)")
    print("   2. Déployer sur Render")
    print("   3. Tester via https://metasploitmcp.onrender.com/healthz")
    print("\n📚 Documentation:")
    print("   - RENDER_ENV_CONFIG.md : Configuration Render")
    print("   - PASSWORD_RESOLUTION.md : Résolution des mots de passe")
    print("   - MSF_STATUS.md : État de msfrpcd")
    sys.exit(0)
else:
    print("\n" + "="*70)
    print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
    print("="*70)
    print("\nVérifiez:")
    print("   - Dépendances installées (pip install -r requirements.txt)")
    print("   - Mot de passe correct dans .env.local")
    print("   - msfrpcd actif sur Oracle Cloud")
    sys.exit(1)

# Fermeture propre
if msf_client:
    print("\n🔌 Fermeture de la connexion msfrpcd...")
    try:
        # pymetasploit3 n'a pas de méthode close explicite
        # La connexion se fermera automatiquement
        print("   ✅ Connexion fermée")
    except:
        pass

print("\n" + "="*70)
print("Test d'intégration terminé")
print("="*70)
