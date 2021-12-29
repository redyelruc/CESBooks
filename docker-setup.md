# Docker Setup

## Using Docker Compose
1. Create a file called .env and enter the following text:
   DB_NAME=library
   DB_APPLICATION_USER=XXXXXXXXX
   DB_APPLICATION_PASSWORD=XXXXXXXXX
   DB_ROOT_PASSWORD=XXXXXXXXX
(replace the XXXXXs with credentials)
2. Run the app and db services:
`docker-compose up`
3. To start the services separately:
`docker-compose up librarydb`
`docker-compose up libraryapp`

## Using Docker

### Build image locally
`docker build --tag ces-books:4.0 .`
(change the version)

### Run container locally
`docker run --publish 80:80 -e DATABASE='mysql://<your_username>:<your_mysql_password>@<your_mysql_hostname>/<your_database_name>' ces-books:4.0`

### Publish to Docker Hub
1. Log in
`docker login --username=redyelruc`

2. Get List of Images
`docker images`

3. Tag Image
`docker tag XXXXXXXXXX redyelruc/ces-books:4.0`
(replace XXXXXXXX with the correct image number from the command above)

4. Push to Docker Hub
`docker push redyelruc/ces-books`

### Run container from image stored in Docker Hub
`docker run --publish 80:80 -e DATABASE='mysql://<your_username>:<your_mysql_password>@<your_mysql_hostname>/<your_database_name>' redyelruc/ces-books:4.0`

## To clean old images and containers
`docker system prune -a`
