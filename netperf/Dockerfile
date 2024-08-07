FROM ubuntu:20.04
# Satisfy deps
RUN apt-get update && \
    apt-get install -y gcc make curl && \
    apt-get clean && \
    rm -rf /tmp/* /var/tmp/* && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /etc/dpkg/dpkg.cfg.d/02apt-speedup   

# Download netperf
RUN curl -LO https://github.com/HewlettPackard/netperf/archive/netperf-2.7.0.tar.gz && tar -xzf netperf-2.7.0.tar.gz  && cd netperf-netperf-2.7.0/ && ./configure && make && make install

CMD ["/usr/local/bin/netserver", "-D"]
 
