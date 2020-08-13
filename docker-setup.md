# Docker Setup

## Build image locally
docker build --tag ces-books:1.1 .
(change the version)

## Run container locally
docker run --publish 80:80  ces-books:1.1

## Publish to Docker Hub
1. Log in
docker login --username=redyelruc

2. Get List of Images
docker images

3. Tag Image
docker tag XXXXXXXXXX redyelruc/ces-books:1.1
(replace XXXXXXXX with the correct image number from the command above)

4. Push to Docker Hub
docker push redyelruc/ces-books

## Run container from image stored in Docker Hub
docker run --publish 80:80  redyelruc/ces-books:1.1

## To clean old images and containers
docker system prune -a