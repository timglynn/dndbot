DockerFile
==========

* `dndbot` is currently running in a docker container on a CentOS 7 host.

## Build and Run
1. Put the `Dockerfile` into the directory containing the `dndbot` project, with
the `redis.conf` file

1. Build the image 

    `docker build --tag=dndbot .` 

1. Run the container

    `docker run -d --restart=on-failure:15 dndbot`


