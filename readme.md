# TecnoMarket_v1

Proyecto basado en el [Curso de Django de Moises Sepulveda 2020](http://https://www.youtube.com/playlist?list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ "Curso de Django de Moises Sepulveda [2020]]") Este proyecto incluye:

- Operaciones CRUD
- Paginación de datos
- Sweet Alert
- Autorizacion y autenticacion por roles y credenciales de Facebook
- Operaciones basicas con Django Rest Framework
- PWA
------------
## Ejecución de proyecto

Verificar version de Python y Django respectivamente
```bash
python --version
python -m django --version
 ```

Crear entorno virtual.
```bash
virtualenv venv
source venv/bin/activate
 ```

Instalar Django / paquetes necesarios

```bash
pip install Django==3.1.2
pip install -r requirements.txt
 ```
Crear proyecto en la misma carpeta (Para eso esta el punto final)
```bash
django-admin startproject <NombreProyecto> .
```

 Ejecutar servidor
```bash
python manage.py runserver
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


 
 
 
 
 