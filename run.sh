set -e 
export PYTHONDONTWRITEBYTECODE='1'
export FLASK_APP=core/server.py

export user_authorization_secret_key="usersksksjdj"

export user_authorization_header_key='userauth'

flask db stamp heads
flask db migrate -m "Initial migration."
flask db upgrade

gunicorn -c gunicorn_config.py core.server:app