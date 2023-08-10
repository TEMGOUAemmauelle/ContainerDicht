FROM alpine:latest
FROM python:3-alpine


# Install bash and java
RUN apk update
RUN apk --no-cache add musl-dev linux-headers g++
RUN apk add --update make cmake gcc g++ gfortran
RUN apk add py-pip
RUN pip install cython
RUN pip install numpy
RUN pip install psutil
COPY [ "test_cpu_mem.py", "test_cpu_mem.py" ]
CMD python test_cpu_mem.py 64000 128000 192000 256000 320000 384000 448000 512000 576000 640000

