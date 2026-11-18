# AgroGanadera — Sistema de Gestión de Ganado

Aplicación web desarrollada en **Django 5** para administrar un campo ganadero dedicado a la crianza y
venta de terneros. Permite clasificar el ganado por raza (modelo padre, administrado desde el Django
Admin) y gestionar la ficha completa de cada animal (modelo hijo), incluyendo su disponibilidad para
la venta, mediante un CRUD web completo construido con Vistas Basadas en Clases.

Proyecto de la **Evaluación Sumativa 3 (Hito 3)** de la asignatura **Programación Back End (TI3041)**,
Instituto Profesional INACAP, sede Osorno.

---

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Framework | Django 5.2 |
| Base de datos | MySQL 8.0 Server (utf8mb4) |
| Conector | PyMySQL (como `MySQLdb`) |
| Frontend | HTML5, Bootstrap 5, Django Template Language |
| Control de versiones | Git + GitHub |

## Arquitectura

El proyecto respeta MVT y la regla de **exactamente dos modelos con una única relación 1:N**:

| Modelo | Rol | Campos | Administración |
|---|---|---|---|
| `Raza` | Padre clasificador | `nombre`, `descripcion` | Solo Django Admin |
| `Ternero` | Hijo operativo | `numero_identificador`, `peso_kg`, `fecha_nacimiento`, `disponible_venta`, `precio_estimado`, `raza` (FK) | CRUD web con CBVs |

La ForeignKey usa `on_delete=models.CASCADE` y `related_name='terneros'`.

## Rutas principales

| Ruta | Vista | Acceso |
|---|---|---|
| `/` | `TerneroListView` (catálogo, con `select_related`) | Público |
| `/ternero/<pk>/` | `TerneroDetailView` | Público |
| `/ternero/nuevo/` | `TerneroCreateView` | Requiere sesión |
| `/ternero/<pk>/editar/` | `TerneroUpdateView` | Requiere sesión |
| `/ternero/<pk>/eliminar/` | `TerneroDeleteView` (con confirmación) | Requiere sesión |
| `/login/` y `/logout/` | `LoginView` / `LogoutView` | Público |
| `/admin/` | Django Admin (Razas y Terneros) | Superusuario |

## Instalación y ejecución local

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/otrolemao/AGROGANADERA.git
   cd AGROGANADERA
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear la base de datos en MySQL Workbench**

   ```sql
   CREATE DATABASE agroganadera CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Configurar la conexión** en `agroganadera_project/settings.py`
   (`DATABASES`: `ENGINE=django.db.backends.mysql`, `NAME=agroganadera`, `USER`, `PASSWORD`,
   `HOST=127.0.0.1`, `PORT=3306`).

6. **Aplicar migraciones**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Crear el superusuario y cargar las razas desde el Admin**

   ```bash
   python manage.py createsuperuser
   ```

8. **Levantar el servidor**

   ```bash
   python manage.py runserver
   ```

   Catálogo: <http://127.0.0.1:8000/> · Admin: <http://127.0.0.1:8000/admin/>

## Datos de prueba

La base contiene **4 razas** (Angus, Hereford, Holando, Normando) y **10 terneros** distribuidos entre
ellas, lo que cumple el mínimo exigido (≥ 4 padres y ≥ 10 hijos).

Consulta de verificación en MySQL Workbench:

```sql
SELECT COUNT(*) AS total_razas FROM ganado_raza;    -- >= 4
SELECT COUNT(*) AS total_terneros FROM ganado_ternero; -- >= 10

SELECT t.numero_identificador, t.peso_kg, r.nombre AS raza
FROM ganado_ternero t
INNER JOIN ganado_raza r ON t.raza_id = r.id;
```

## Estructura del proyecto

```
AGROGANADERA/
├── agroganadera_project/       Configuración (settings, urls, wsgi/asgi)
│   └── __init__.py             Registro de PyMySQL como MySQLdb
├── ganado/                     Aplicación principal
│   ├── models.py               Raza y Ternero
│   ├── admin.py                ModelAdmin con list_display, list_filter y search_fields
│   ├── forms.py                TerneroForm con widgets Bootstrap y validaciones
│   ├── views.py                5 CBVs (List, Detail, Create, Update, Delete)
│   ├── urls.py                 Rutas con nombre
│   ├── migrations/             Migraciones
│   └── templates/ganado/       base, catalogo, detalle, formulario, confirmar_eliminar, login
├── static/
│   ├── css/custom.css          Estilos propios del sistema
│   └── img/logo.svg            Logotipo
├── prompts_ia.md               Bitácora de IA en formato RTCF
├── requirements.txt
└── manage.py
```

## Autor

Jorge Martínez — [@otrolemao](https://github.com/otrolemao)
