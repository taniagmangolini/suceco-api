# suceco-api

Suceco Django API Project

The API Documentation is available at the path /api/docs. For instance: https://localhost:8000/api/docs.

### Useful Commands

#### Build

##### Build the containeirs using the Dockerfile

docker build .

##### Build containeirs using the the docker-compose file

docker-compose buil

#### Create a docker project

docker-compose run --rm app sh -c "django-admin startproject app ."

#### Tests

##### Run tests

docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"

##### Run teste and Coverage

docker-compose run --rm app sh -c "coverage run manage.py test && coverage report -m"

#### Run the linting tool flake8

docker-compose run --rm app sh -c "flake8"

To tell flake8 to ignore something, add # noqa to it.

#### Run system

docker-compose up

#### Create a new app

docker-compose run --rm app sh -c "python manage.py startapp appname"

#### Migrations

##### Create and apply migrations
docker-compose run --rm app sh -c "python manage.py makemigrations && python manage.py wait_for_db && python manage.py migrate"

##### Only migrate
docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"

##### Check migrations
docker-compose run --rm app sh -c "python manage.py showmigrations"

#### Run a specific management command (ex. wait_for_db)

docker-compose run --rm app sh -c "python manage.py wait_for_db"

#### Create a superuser

docker-compose run --rm app sh -c "python manage.py createsuperuser"