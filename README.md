# Proyecto Django

## Configuración local

Instala Django en tu entorno de Python y configura una clave secreta antes de iniciar el proyecto.

Puedes generar una clave con:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Guárdala en la variable de entorno `DJANGO_SECRET_KEY` o en `myproject/local_settings.py`:

```python
SECRET_KEY = "pega-aqui-tu-clave-generada"
```

No publiques esa clave. `local_settings.py`, `db.sqlite3` y el entorno virtual están excluidos de Git.

Para preparar la base de datos y ejecutar el servidor:

```powershell
python manage.py migrate
python manage.py runserver
```
