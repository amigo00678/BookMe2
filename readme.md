This is NOT a finished project, just the basics.

Django provides default admin, spartanian one. The target of this project is to create an admin for clients. So it has to be beautiful and convenient to use. Many modern CMSs have admins with statistics, objects editing, permissions, etc, etc.

```
mkvirtualenv cadmin
pip install -r requirements.txt
python manage.py makemigrations web
python manage.py migrate
python manage.py reload
python manage.py runserver 0.0.0.0:8000
```

Please see [updates](https://github.com/amigo00678/CAdmin/tree/fixes/progress)

As well as [commits list](https://github.com/amigo00678/CAdmin/commits/master)
