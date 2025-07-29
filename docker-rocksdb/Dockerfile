FROM golang:1.14.4-alpine

# Ajouter les dépôts edge (optionnel pour paquets récents)
RUN echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# Installer dépendances pour compiler RocksDB
RUN apk add --no-cache \
    build-base linux-headers \
    bash git perl cmake \
    zlib zlib-dev \
    bzip2 bzip2-dev \
    lz4 lz4-dev \
    zstd zstd-dev \
    snappy snappy-dev \
    gflags-dev

# Cloner et compiler RocksDB
RUN cd /tmp && \
    git clone https://github.com/facebook/rocksdb.git && \
    cd rocksdb && \
    git checkout v6.10.2 && \
    make -j$(nproc) shared_lib && \
    make db_bench -j$(nproc) && \
    mkdir -p /usr/local/rocksdb/lib /usr/local/rocksdb/include && \
    cp librocksdb.so* /usr/local/rocksdb/lib && \
    cp /usr/local/rocksdb/lib/librocksdb.so* /usr/lib/ && \
    cp -r include /usr/local/rocksdb/include && \
    cp -r include/* /usr/include/ && \
    cp db_bench /usr/local/bin && \
    cd / && rm -rf /tmp/rocksdb

# Point d’entrée : lancer un benchmark simple avec db_bench
CMD ["db_bench", "--benchmarks=fillseq", "--num=100000", "--value_size=100", "--db=/tmp/rocksdb_bench"]
