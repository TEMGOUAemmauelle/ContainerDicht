#!/bin/bash
# Adresse IP du serveur netperf (à modifier selon ton setup)
SERVER_IP="192.168.0.100"

echo "Lancement de netperf client vers $SERVER_IP pour 10 secondes"

# exec permet de remplacer le shell par netperf, 
# assurant que les signaux (SIGTERM) arrivent bien à netperf
exec netperf -H "$SERVER_IP" -l 10
