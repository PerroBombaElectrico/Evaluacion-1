# Evaluación Sumativa 2 - Caso 2: Control de ventas

## Descripción del sistema

Aplicación web desarrollada con Django para gestionar productos y ventas de una pequeña tienda. El sistema incluye:

- CRUD de productos.
- Registro de ventas con varios productos.
- Cálculo automático de subtotales y totales.
- Control de stock con validación de disponibilidad.
- Reporte de ventas por rango de fechas.
- Administración con Django Admin.
- Configuración para entornos de desarrollo y producción.

## Tecnologías utilizadas

- Python 3.12+
- Django 5.x
- PostgreSQL (producción)
- SQLite (desarrollo local)
- HTML + CSS + Django templates
- WhiteNoise para archivos estáticos
- PostgreSQL driver: `psycopg`
- Variables de entorno con `python-dotenv`
- Configuración regional de Chile: español de Chile, zona horaria de Santiago y pesos chilenos (CLP)

## Instalación local

1. Clona el repositorio.
2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Activa el entorno virtual:

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

5. Crea un archivo `.env` a partir de `.env.example`:

```bash
copy .env.example .env
```

O en Linux/macOS:

```bash
cp .env.example .env
```

6. Ajusta variables de entorno si es necesario.

## Configuración de variables de entorno

El proyecto usa variables en `.env`:

```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

Para producción con PostgreSQL, usa una línea como esta:

```env
DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
DEBUG=False
ALLOWED_HOSTS=miapp.onrender.com
CSRF_TRUSTED_ORIGINS=https://miapp.onrender.com
```

## Migraciones

```bash
python manage.py migrate
```

## Crear superusuario

```bash
python manage.py createsuperuser
```

## Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en:

```text
http://127.0.0.1:8000/
```

## Pruebas

```bash
python manage.py test
```

## Publicación en GitHub

```bash
git init
git add .
git commit -m "Entrega ES02"
git branch -M main
git remote add origin <URL_DEL_REPOSITORIO>
git push -u origin main
```

## PostgreSQL en producción

Se recomienda usar PostgreSQL en producción para la parte de entrega final. Ejemplo de conexión:

```env
DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
```

## Despliegue en la nube

### Importante sobre Vercel

Vercel no es una opción recomendada para un proyecto Django tradicional con servidor WSGI y PostgreSQL, salvo que se configure con un servicio externo o una estructura específica. Tiene limitaciones para apps Django clásicas que requieren:

- servidor WSGI o ASGI de Django,
- migraciones y manejo de estáticos,
- configuración de `collectstatic`,
- un runtime de app server que no siempre encaja con proyectos Django tradicionales.

Por eso, para esta entrega la recomendación es usar un servicio compatible, por ejemplo:

- Render
- Railway
- Fly.io
- PythonAnywhere

La configuración recomendada es:

1. Subir el proyecto a GitHub.
2. Conectar el repositorio a Render/Railway.
3. Añadir la base PostgreSQL.
4. Configurar variables de entorno.
5. Ejecutar migraciones y `collectstatic`.
6. Habilitar HTTPS.

## Lista de comprobación ES02

- [x] Proyecto reutilizado y estructura organizada.
- [x] Modelo `Producto` con validaciones.
- [x] Modelo `Venta` con total calculado.
- [x] Modelo `DetalleVenta` con relación y subtotal.
- [x] CRUD completo de productos.
- [x] Registro de ventas con multiplicidad de productos.
- [x] Validación de stock y consistencia.
- [x] Cálculo de total y subtotales en servidor.
- [x] Paginación y búsqueda.
- [x] Reporte por rango de fechas.
- [x] Django Admin personalizado.
- [x] Variables de entorno y `.env.example`.
- [x] Configuración de despliegue y WhiteNoise.
- [x] Pruebas automatizadas.
- [x] README en español.

## Guion breve de presentación

"Este proyecto es una aplicación de control de ventas para una pequeña tienda. Permite gestionar productos, registrar ventas con varios artículos, validar stock y consultar reportes por fecha. La solución está desarrollada con Django, usa SQLite en desarrollo y PostgreSQL en producción, y conserva buenas prácticas como validaciones del lado del servidor, transacciones y control de stock. Además, tiene administración personalizada con Django Admin y está preparada para desplegarse en un servicio compatible como Render o Railway."

## Nota final

La lógica principal está enfocada en un flujo realista y seguro de ventas, evitando confiar en valores enviados desde el navegador y calculando los totales en el servidor.
