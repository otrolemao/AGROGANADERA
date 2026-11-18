# Bitácora de uso de Inteligencia Artificial — AgroGanadera

**Asignatura:** Programación Back End (TI3041) — Evaluación Sumativa 3 (Hito 3)
**Estudiante:** Jorge Martínez (usuario GitHub `otrolemao`)
**Asistente utilizado:** DeepSeek (chat web) como tutor técnico, y Google Stitch para referencias de diseño.
**Criterio de uso:** la IA se usó para generar borradores de código y explicar el *por qué* de cada
decisión; todo el código fue ejecutado, probado en el navegador y corregido en clase antes de subirse.

---

## Marco RTCF

Cada prompt se documenta con los cuatro componentes: **R**ol, **T**area, **C**ontexto y **F**ormato.

---

## Prompt 1 — Modelamiento relacional (Bloque 1)

**Rol**
> Actúa como tutor de backend Django para un estudiante de segundo año de Ingeniería en Informática.

**Tarea**
> Generar el archivo `models.py` con exactamente dos modelos relacionados 1:N: un modelo padre
> clasificador `Raza` y un modelo hijo `Ternero` con ForeignKey hacia el padre, `on_delete` explícito,
> `verbose_name` en cada campo y método `__str__`.

**Contexto**
> Proyecto de evaluación: sistema de gestión de un campo ganadero que cría y vende terneros. Se exige
> un mínimo de cuatro campos propios variados (texto, decimal, fecha y booleano) además de la FK, y el
> modelo padre solo se administra desde el Django Admin. No se permiten relaciones ManyToMany.

**Formato**
> Código Python limpio, archivo completo listo para pegar, sin emojis ni comentarios decorativos.
> Después del código, una explicación breve de por qué corresponde `on_delete=models.CASCADE` y qué
> significa `related_name`.

**Resultado obtenido:** `ganado/models.py` con `Raza` y `Ternero`; se ajustaron los nombres de los
campos al negocio y se verificó la migración `0001_initial` en MySQL Workbench.

---

## Prompt 2 — CRUD con CBVs y optimización ORM (Bloque 2)

**Rol**
> Actúa como profesor de Django corrigiendo un trabajo práctico de vistas basadas en clases.

**Tarea**
> Escribir `views.py`, `urls.py` y las plantillas para el ciclo CRUD completo del modelo hijo usando
> `ListView`, `DetailView`, `CreateView`, `UpdateView` y `DeleteView`, con `select_related` en el
> catálogo y `reverse_lazy` en las redirecciones.

**Contexto**
> Mismo proyecto ganadero. El catálogo es público y debe listar los terneros con su raza en una tabla
> Bootstrap 5; el detalle se obtiene por `<int:pk>`; la eliminación necesita una plantilla intermedia
> de confirmación. La evaluación exige explícitamente `select_related('raza')` para evitar el problema
> N+1 y una plantilla `base.html` de la que hereden todas las vistas.

**Formato**
> Un bloque de código por archivo, indicando la ruta exacta de cada uno. Al final, explicar en tres
> líneas qué consulta SQL genera `select_related` frente a no usarlo.

**Resultado obtenido:** las 5 CBVs y las plantillas `base.html`, `catalogo.html`, `detalle.html`,
`formulario.html` y `confirmar_eliminar.html`. Se comprobó en el navegador que el catálogo muestra la
raza sin consultas extra y que el detalle de un `pk` inexistente devuelve 404.

---

## Prompt 3 — Depuración de la vista en blanco (Bloque 3)

**Rol**
> Actúa como compañero de equipo que depura errores de Django junto conmigo.

**Tarea**
> Diagnosticar por qué después de configurar el login la aplicación se ve completamente en blanco al
> iniciar sesión, y entregar los pasos de corrección ordenados.

**Contexto**
> Tengo activado `LoginRequiredMixin` en las vistas de creación, edición y borrado, y el
> `LOGIN_REDIRECT_URL` apunta al catálogo. El servidor responde 200 en `/` y en `/login/` pero la
> página que veo está vacía. Uso Django 5.2 con plantillas dentro de `ganado/templates/ganado/`.

**Formato**
> Lista numerada de verificaciones con el resultado esperado en cada una, y el fragmento de código
> exacto a corregir. Sin teoría extensa.

**Resultado obtenido:** el problema estaba en la carga de la plantilla y en la sesión del usuario de
prueba; se creó un superusuario nuevo y el login mostró correctamente el catálogo y la barra de
navegación con el nombre del usuario.

---

## Prompt 4 — Conexión a MySQL (Bloque 1, cierre)

**Rol**
> Actúa como administrador de bases de datos que apoya a un estudiante en un laboratorio de Django.

**Tarea**
> Explicar cómo crear el esquema en MySQL Workbench con cotejamiento `utf8mb4`, configurar
> `DATABASES` en `settings.py` y ejecutar las migraciones para que las tablas aparezcan en Workbench.

**Contexto**
> MySQL 8.0 local en `127.0.0.1:3306`, usuario `root`. El proyecto venía funcionando en SQLite y ya
> tenía los modelos definidos y datos de prueba cargados (4 razas y 10 terneros) que hay que conservar.

**Formato**
> Pasos numerados con el comando exacto de terminal y la sentencia SQL de verificación. Al final, las
> tres consultas de auditoría (`COUNT` de padres, `COUNT` de hijos e `INNER JOIN`).

**Resultado obtenido:** base `agroganadera` creada en MySQL, migraciones aplicadas y datos migrados
desde SQLite; verificado con `SELECT COUNT(*)` en Workbench.

---

## Declaración de uso responsable

- El código sugerido por la IA fue **leído, ejecutado y corregido**; no se subió código sin probarlo.
- Las explicaciones se usaron para entender la lógica (MRO de los mixins, `select_related`, migraciones).
- Las credenciales de la base de datos local son de desarrollo y están en `settings.py` solo porque el
  proyecto se evalúa en el laboratorio; en un entorno real irían en variables de entorno.
