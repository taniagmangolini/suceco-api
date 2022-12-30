# suceco-api

Suceco Django API Project

### Useful Commands

#### Build the containeirs using the Dockerfile

docker build .

#### Build containeirs using the the docker-compose file

docker-compose build

#### Create a docker project

docker-compose run --rm app sh -c "django-admin startproject app ."

#### Run tests

docker-compose run --rm app sh -c "python manage.py test"

#### Run the linting tool flake8

docker-compose run --rm app sh -c "flake8"

#### Run system

docker-compose up

#### Create a new app

docker-compose run --rm app sh -c "python manage.py startapp core"
