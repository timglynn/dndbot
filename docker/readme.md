DockerFile
==========

* dndbot is currently running in a docker container

## Build and Run
1. Put the `Dockerfile` into the directory containing the `dndbot` project
1. Build the image 
    `docker build --tag=dndbot .` 
1. Run the container
    `docker run -d --restart=on-failure:15 dndbot`


