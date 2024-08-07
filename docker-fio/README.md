#fio
fio is IO benchmark docker image with fio cli

## how to run the benchmark

To test the performance of the storage, just go in a folder that mounts the storage and run : 
```bash
docker/podman  run -it --rm -v $PWD:/data infrabuilder/fio
```

You will get the benchmark result in container output

How CRI-O Works:

    Kubernetes communicates with CRI-O: Kubernetes uses the CRI to interact with the container runtime.
    CRI-O manages container lifecycle: It handles tasks like pulling images, creating containers, starting, stopping, and removing containers.
    OCI runtime execution: CRI-O delegates the actual container execution to an OCI-compliant runtime like runc.

If you're using Kubernetes, CRI-O offers a native and efficient way to manage containers.

## how to run the benchmark CRI-O

To test the performance of the storage, just go in a folder that mounts the storage and run : 
```bash

kubectl run -it --name --image=registry.io/fio   //(registry=docker )
