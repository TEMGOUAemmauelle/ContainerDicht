#!/bin/bash

# Démarrer netserver en arrière-plan
/usr/local/bin/netserver -D

# Attendre que netserver soit prêt
sleep 2

echo "Lancement du benchmark netperf client (10s)..."

# Lancer netperf en client vers localhost, durée 10s
netperf -H 127.0.0.1 -l 10

echo "Benchmark terminé, arrêt du serveur netserver..."

# Arrêter netserver
pkill netserver

echo "Terminé."
