# Web configuration interface for Kullo accounts

## Set up local test environment

We assume that the local Kullo DB has the name, user and password `kullo`.

### Create Postgres DB

    sudo -u postgres createuser -P webconfig  # enter the password "webconfig" when asked
    sudo -u postgres createdb -O webconfig webconfig

## Django

### Setup

    ./src/manage.py migrate

### Start server

    ./src/manage.py runserver
