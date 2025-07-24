FROM golang:1.14.4-alpine

RUN echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "@edge http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --no-cache \
  build-base linux-headers \
  bash git perl cmake \
  zlib zlib-dev \
  bzip2 bzip2-dev \
  lz4 lz4-dev \
  zstd zstd-dev \
  snappy snappy-dev \
  gflags-dev

# Installer RocksDB
RUN cd /tmp && \
    git clone https://github.com/facebook/rocksdb.git && \
    cd rocksdb && \
    git checkout v6.10.2 && \
    make -j$(nproc) shared_lib && \
    mkdir -p /usr/local/rocksdb/lib /usr/local/rocksdb/include && \
    cp librocksdb.so* /usr/local/rocksdb/lib && \
    cp /usr/local/rocksdb/lib/librocksdb.so* /usr/lib/ && \
    cp -r include /usr/local/rocksdb/include && \
    cp -r include/* /usr/include/ && \
    cd / && rm -rf /tmp/rocksdb
