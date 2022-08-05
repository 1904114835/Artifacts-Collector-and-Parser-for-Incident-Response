# Artifact Collector web server

## deployment
all the third party package needed for this project is listed in the requirements.txt file
```shell
pip install -r requirements.txt
```

## database initialization
to initialize the database, run the following command. the first thing to do is to create the database, and then use the ORM models to create the tables.
```shell
mysql -uroot -p
create database artifacts_v2.9;
```
```shell
python manage.py migrate
```

## start server
to launch the webserver locally, just run the following command
```shell
python manage.py runserver
```

