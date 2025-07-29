FROM alpine:3.16

# Installer les outils nécessaires
RUN apk update && \
    apk add --no-cache git make gcc bash libc-dev build-base linux-headers perl && \
    # Cloner le dépôt UnixBench
    mkdir -p /usr/src && \
    cd /usr/src && \
    git clone --depth 1 https://github.com/kdlucas/byte-unixbench.git && \
    cd /usr/src/byte-unixbench/UnixBench && \
    make

# Définir le répertoire de travail
WORKDIR /usr/src/byte-unixbench/UnixBench

# Commande exécutée automatiquement au lancement du conteneur
CMD ["./Run"]
