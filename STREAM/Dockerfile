# start from base
FROM ubuntu:20.04
MAINTAINER Sangala Mballa Louis Michel <sangalamballamichel@gmail.com>

# Set non-interactive mode for apt (évite les blocages)
ENV DEBIAN_FRONTEND=noninteractive

# Install system-wide dependencies
RUN apt-get update && \
    apt-get -yqq install \
    autoconf \
    ant \
    libtcmalloc-minimal4 \
    swig \
    google-perftools \
    libboost-all-dev \
    bzip2 \
    libnuma-dev \
    libgoogle-perftools-dev \
    libdb-dev \
    libaio-dev \
    uuid-dev \
    libbz2-dev \
    libgtop2-dev \
    git \
    bash \
    sudo \
    libreadline-dev \
    ncurses-dev \
    gfortran \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Clone the STREAM repository
RUN git clone https://github.com/jeffhammond/STREAM.git /usr/src/stream

# Build STREAM benchmark
RUN cd /usr/src/stream && \
    gcc -O2 -fopenmp stream.c -o stream

# Définit le dossier de travail
WORKDIR /usr/src/stream

# Commande par défaut au lancement du conteneur
CMD ["./stream"]

