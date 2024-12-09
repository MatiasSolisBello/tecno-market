# TecnoMarket

Proyecto basado en el [Curso de Django de Moises Sepulveda 2020](http://https://www.youtube.com/playlist?list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ "Curso de Django de Moises Sepulveda [2020]]")


## Indice

[Ejecución de proyecto](#ejecución-de-proyecto)

[Docker](#docker)

[Otros comandos](#otros-comandos)


## Ejecución de proyecto

Crear entorno virtual.
```bash
virtualenv venv
source venv/bin/activate
```

Instalar paquetes necesarios
```bash
pip install -r requirements.txt
```

Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

Crear superusuario
```bash
python manage.py createsuperuser
```

Crear archivo env dentro del folder con nombre del proyecto, para este proyecto especifico se necesita:
```bash
DEBUG=True
SOCIAL_AUTH_FACEBOOK_KEY=''
SOCIAL_AUTH_FACEBOOK_SECRET=''
```

Ejecutar servidor
```bash
python manage.py runserver
```

## Docker
```bash
docker compose -up --build
```

## Otros comandos
Verificar version de Python y Django respectivamente
```bash
python --version
python -m django --version
```

Crear proyecto en la misma carpeta (Para eso esta el punto final)
```bash
django-admin startproject <NombreProyecto> .
```