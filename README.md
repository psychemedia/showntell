# `maps_build_image`

This repo contains the Binder build files for the `maps` demos.

On local computer, download this repo and then  build and push the image. Eg build the Binder container using `jupyter repo2docker`:


`jupyter-repo2docker --image-name=psychemedia/binder_maps --no-run`

Push to Dockerhub to make image publicly available:

`docker push psychemedia/binder_maps`

(`repo2docker` should be able to build from a Githuib repo branch directly - [but there's a bug?](https://github.com/jupyter/repo2docker/issues/135))


