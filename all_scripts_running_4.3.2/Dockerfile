# start from base
FROM ubuntu:16.04
MAINTAINER Sangala Mballa Louis Michel <sangalamballamichel@gmail.com>
# install system-wide deps 
RUN apt-get update 
RUN apt-get -yqq install autoconf ant libtcmalloc-minimal4 swig google-perftools libboost1.58-all-dev bzip2 libnuma-dev  libgoogle-perftools-dev libdb5.3++-dev libmysqld-dev libaio-dev uuid-dev libbz2-dev libgtop2-dev git bash sudo libreadline-dev ncurses-dev gfortran
RUN apt-get install netperf
RUN apt install time strace
CMD strace -T -C -o net100.txt netperf -t TCP_STREAM -c -C -H 172.17.0.2 -l 20 -- -m 100000 







