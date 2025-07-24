FROM alpine:latest
FROM python:3-alpine


# Install bash and java
RUN apk update
RUN apk --no-cache add musl-dev linux-headers g++
RUN apk add --update make cmake gcc g++ gfortran
RUN apk add py-pip
RUN pip install cython
RUN pip install numpy
RUN apk add git
RUN git clone https://github.com/vmchale/matrix-benchmarks.git
WORKDIR /matrix-benchmarks/
RUN cd /matrix-benchmarks/
#CMD cd /matrix-benchmarks/
CMD python bench.py

