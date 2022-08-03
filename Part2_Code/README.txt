# Artifact Collector web server

## deployment
all the third party package needed for this project is listed in the requirements.txt file
```shell
pip install -r requirements.txt
```

## database initialization
```shell
python manage.py migrate
```

## start server
to launch the webserver locally, just run the following command
```shell
python manage.py runserver
```

