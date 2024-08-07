# docker-apache-benchmark

Apache Benchmark Docker image.

❗Breaking changes on v2.0.0: now the `ab` command is not needed after the image name. This readme has been updated accordingly.

```
docker build -t ab .
```

## HTTP POST request

Sending a POST request is slightly more convoluted. As `ab` requires the POST body to be in a file, you should pass the file from the host (well, the Docker client) to the container. There are several ways to do that, but perhaps the easiest is to share the current directory:

```
docker/podman  run --rm ab -n 1000000 -c 100  -r http://10.88.0.2:80/
```

you must have the `post.json` file readable in your host current directory prior to execute `docker run ...`

# Notes

## Testing on localhost

If you try to test a server on your localhost, you cannot point to it using `http://localhost:8080/` as this is the address of the `jordi/ab` container itself. To test a service in your local machine or in a container in your local machine, use either the _hostname_ of your workstation (that will point to your Ethernet/WiFi IP address) or the Docker bridge address, that usually is `172.17.0.1`. For example, to launch an HTTP service in docker and benchmark it:

```
docker run -d -p 8080:8080 server:http
docker run --rm ab -k -c 100 -n 100000 http://172.17.0.1:8080/ 
```


