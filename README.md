# suceco-api

Suceco Django API Project

The API Documentation is available at the path /api/docs. For instance: https://localhost:8000/api/docs.

### Useful

#### Build

##### Build the containeirs using the Dockerfile

docker build .

##### Build containeirs using the the docker-compose file

docker-compose build

#### Create a docker project

docker-compose run --rm app sh -c "django-admin startproject app ."

#### Tests

##### Run tests

docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"

##### Run tests and coverage

docker-compose run --rm app sh -c "coverage run manage.py test && coverage report -m"

#### Run the linting tool flake8

docker-compose run --rm app sh -c "flake8"

To tell flake8 to ignore something, add # noqa to it.

#### Run system

docker-compose up

You can specify a specific yml file on your commands. For instance:

docker-compose -f docker-compose.yml up

docker-compose -f docker-compose.yml up --force-recreate --renew-anon-volumes

To run in the background add -d. For instance:

docker-compose -f docker-compose.yml up -d

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

#### Production environment

The production environment will run the system using gunicorn and nginx.
Check the port it will be running at the nginx service defined in the docker-compose.prod.yml file.
The command to build and run in the production mode is:

docker-compose -f docker-compose.prod.yml up -d --build

To stop:

docker-compose -f docker-compose.prod.yml stop
