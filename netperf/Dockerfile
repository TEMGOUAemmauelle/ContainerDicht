FROM ubuntu:20.04

# Installer dépendances nécessaires
RUN apt-get update && \
    apt-get install -y gcc make curl net-tools iproute2 procps && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Télécharger, compiler et installer netperf
RUN curl -LO https://github.com/HewlettPackard/netperf/archive/netperf-2.7.0.tar.gz && \
    tar -xzf netperf-2.7.0.tar.gz && \
    cd netperf-netperf-2.7.0 && \
    ./configure && make && make install

# Copier le script de lancement
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Lancer start.sh au démarrage du conteneur
CMD ["/app/start.sh"]
