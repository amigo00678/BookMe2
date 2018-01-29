
A base project for client admin part.

mkvirtualenv cadmin
pip install -r requirements.txt
python manage.py makemigrations web
python manage.py migrate
python manage.py reload
python manage.py runserver 0.0.0.0:8000

Please see 'proj.png' for details.
