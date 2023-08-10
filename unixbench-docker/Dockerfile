FROM alpine:3.16

ARG unix_VERSION=v5.1.3

RUN apk update && \
    ls && \
    apk add git make gcc libc-dev bash && \
    apk add --no-cache build-base linux-headers perl && \
    #pip install x11-apps && \
    #./install_drawstuff.sh && \
    mkdir /usr/src && \
    cd /usr/src && \
    git clone --depth 1  https://github.com/kdlucas/byte-unixbench.git && \
    ls && \
    cd byte-unixbench/UnixBench && \
    #cd /usr/src/unixbench/byte-unixbench/UnixBench && \
    # Fix 'install -c' flag
    make



    
    





