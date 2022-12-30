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

#### Coverage tests

docker-compose run --rm app sh -c "coverage run manage.py test && coverage report -m"

#### Run the linting tool flake8

docker-compose run --rm app sh -c "flake8"

To tell flake8 to ignore something, add # noqa to it.

#### Run system

docker-compose up

#### Create a new app

docker-compose run --rm app sh -c "python manage.py startapp appname"


#### Create and apply migrations

docker-compose run --rm app sh -c "python manage.py makemigrations && python manage.py migrate"

#### Run a specific management command (ex. wait_for_db)

docker-compose run --rm app sh -c "python manage.py wait_for_db"

