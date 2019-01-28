This Web will process heart signals from a Holter monitor prototype device.
Also It will save patients' history.

Download this project and make it better! ;)

Thesis project.
Authors: Fiorella Quino O. and Gabriela Garcia G.
Lima - Peru (2017-2018)

* Python 3.7
* Django 2.1

# Installing Web App

1. Clone the project

2. Execute these commands

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

# Commands

### Dumpdata
`python manage.py dumpdata --exclude auth.permission --exclude contenttypes --ident 2 > initial.json`
