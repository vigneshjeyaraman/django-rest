## Postgres setting.

1. Create database with name usermanagement
    -- CREATE DATABASE USERMANAGEMENT;
2. Create an user and setting password.
    -- CREATE USER TUSHAR WITH PASSWORD 'TUSHAR';
3. Alter above created user as superuser.
    -- ALTER USER TUSHAR WITH SUPERUSER;

## Virtual environment
create a new virtual environment by running below command.

virtualenv -p <path to your python3.8> venv

## Activate the environment

source venv/bin/activate

## Install the dependencies

pip install -r requitements.txt

## run migration

./manage.py migrate

## create a super/ admin user

./manage.py createsuperuser

It will ask for email, username and password.

## Launch shell_plus

./manage.py shell_plus

## create admin token
Token.objects.create(user_id=<admin user id>)

## bring the server up

./manage.py runserver

## Postman collection
https://www.getpostman.com/collections/d593df0c1d49baca02b4

Import the above collection and run the APIs.

