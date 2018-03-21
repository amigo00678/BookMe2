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

Please see [project.png](https://github.com/amigo00678/CAdmin/blob/master/project.png)

And [project1.png](https://github.com/amigo00678/CAdmin/blob/master/project1.png) for updates.

Added [project2.png](https://github.com/amigo00678/CAdmin/blob/fixes/project2.png) for customer views.

All updates in [commits list](https://github.com/amigo00678/CAdmin/commits/master)
