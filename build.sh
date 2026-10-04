set -o errexit
python3 manage.py collectstatic
pip install -r requirements.txt
python3 manage.py  makemigrations
python3 manage.py  migrate
