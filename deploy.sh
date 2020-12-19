#!/bin/bash
set -e

# must be sourced before set -u because it accesses unset variables...
source venv/bin/activate || (echo "Error while activating venv"; exit 1)
set -u

git pull
pip install -r requirements.txt
[ -d static/COMPILED ] || mkdir static/COMPILED

export DJANGO_SETTINGS_MODULE="WebConfig.settings.production"
python src/manage.py check --deploy
python src/manage.py migrate
python src/manage.py collectstatic --noinput --clear
python src/manage.py compilestatic
touch static/.gitkeep

(
    cd src
    python manage.py compilemessages
)

service uwsgi reload || service uwsgi restart
