# Trabalho Redes

## Dependencies
 - python >= ``3.9``
 - Django

## Configure the Virtual Environment
### Create Virtual Environment
    python -m venv .venv
### Activate the Virtual Environment
Linux

    source .venv/bin/activate
### Install Dependences
    pip install -r requirements.txt

## Run server project
Entre na pasta ``server`` e execute o seguinte comando no terminal

    python manage.py runserver 127.0.0.1:8001

## Run client project
Entre na pasta ``client`` e execute o seguinte comando no terminal

    python manage.py runserver
