# docker-netperf
A docker image for netperf testing.

If the container is run without arguments, it will start a netserver daemon. The container also has the netperf client installed, so you can start another container to run the client.

## Example

To compare throughput between Docker host networking and bridged networking:

```
$ # Run host-network netperf test
$ docker/podman  run -dt --net=host --name netserver-host paultiplady/netperf
$ docker/podman  run -it --net=host paultiplady/netperf netperf –l 10 -i 10 -I 95,1 -c -j -H 127.0.0.1 -t OMNI -- -D  -T tcp -O THROUGHPUT,THROUGHPUT_UNITS,STDDEV_LATENCY,LOCAL_CPU_UTIL
OMNI Send TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 127.0.0.1 () port 0 AF_INET : +/-0.500% @ 95% conf.  : nodelay
Throughput Throughput  Stddev       Local  
           Units       Latency      CPU    
                       Microseconds Util   
                                    %      
25220.39   10^6bits/s  23.82        30.31  


$ # Run bridged-network netperf test
$ docker/podman run -dt --name netserver-bridge netperf
$ ip=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' netserver-bridge)
$ docker run -it paultiplady/netperf netperf –l 10 -i 10 -I 95,1 -c -j -H $ip -t OMNI -- -D  -T tcp -O THROUGHPUT,THROUGHPUT_UNITS,STDDEV_LATENCY,LOCAL_CPU_UTIL
OMNI Send TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 172.17.0.74 () port 0 AF_INET : +/-0.500% @ 95% conf.  : nodelay
Throughput Throughput  Stddev       Local  
           Units       Latency      CPU    
                       Microseconds Util   
                                    %      
11198.09   10^6bits/s  32.46        31.51  


How CRI-O Works:

    Kubernetes communicates with CRI-O: Kubernetes uses the CRI to interact with the container runtime.
    CRI-O manages container lifecycle: It handles tasks like pulling images, creating containers, starting, stopping, and removing containers.
    OCI runtime execution: CRI-O delegates the actual container execution to an OCI-compliant runtime like runc.

If you're using Kubernetes, CRI-O offers a native and efficient way to manage containers.

## how to run the benchmark CRI-O

To test the performance of the storage, just go in a folder that mounts the storage and run : 
```bash
kubectl run -it net --image=registry.io/netperf
kubectl run -it name --image=registry.io/netperf -- netperf -t TCP_STREAM -H @ip_net -c -C -l 300 -- -m 64  //(registry=docker )
