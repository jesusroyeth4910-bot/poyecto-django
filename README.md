# Proyecto Django

## Configuración local

Instala las dependencias y configura una clave secreta antes de iniciar el proyecto:

```powershell
python -m pip install -r requirements.txt
```

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

## Publicar en Render

El archivo `render.yaml` configura el servidor web, PostgreSQL, archivos estáticos y migraciones. En Render, inicia sesión, crea un Blueprint desde este repositorio y confirma los servicios definidos.

Después de que termine el despliegue:

1. En Render, configura los valores secretos `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` y `DJANGO_SUPERUSER_PASSWORD` cuando se te soliciten.
2. Render crea el usuario administrador durante el inicio del servicio. El comando no cambia la contraseña si ese usuario ya existe.
3. Entra en `https://<dominio-del-servicio>/admin/`.

La configuración inicial usa servicios gratuitos, apropiados para pruebas. El servicio web puede suspenderse por inactividad y la base de datos gratuita caduca a los 30 días. Render no ofrece Shell para servicios web gratuitos. Revisa los límites y condiciones vigentes; usa un plan con almacenamiento persistente antes de guardar datos importantes.
