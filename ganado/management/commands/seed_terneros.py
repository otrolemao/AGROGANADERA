"""Reinicia los datos de prueba de Ternero y les asigna las fotos reales.

Uso:
    python manage.py seed_terneros

El comando elimina todos los terneros existentes (no toca las Razas) y crea
10 registros nuevos. Para la imagen escanea la carpeta media/terneros/ y usa
el nombre real de cada archivo, por lo que funciona con .jpg, .jpeg, .png,
.webp, etc. sin importar la extension declarada.
"""

import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ganado.models import Raza, Ternero

# Razas base del proyecto. Solo se crean si no existen; nunca se eliminan.
RAZAS = [
    ('Angus', 'Raza britanica de carne, reconocida por su precocidad y calidad.'),
    ('Hereford', 'Raza britanica rustica, docil y de buen rendimiento carnicero.'),
    ('Holando', 'Raza lechera de origen holandes, tambien usada para carne.'),
    ('Normando', 'Raza francesa mixta, con buena produccion de leche y carne.'),
]

# Datos de prueba: (arete, peso, fecha_nacimiento, disponible, precio, raza)
DATOS_TERNEROS = [
    ('ARETE-001', '95.50', '2026-01-15', True, 450000, 'Angus'),
    ('ARETE-002', '112.00', '2026-02-03', True, 520000, 'Hereford'),
    ('ARETE-003', '128.75', '2025-12-10', False, 610000, 'Holando'),
    ('ARETE-004', '104.30', '2026-03-22', True, 480000, 'Normando'),
    ('ARETE-005', '140.20', '2025-11-05', True, 700000, 'Angus'),
    ('ARETE-006', '118.60', '2026-04-18', True, 550000, 'Hereford'),
    ('ARETE-007', '132.40', '2026-05-09', False, 640000, 'Holando'),
    ('ARETE-008', '99.80', '2026-06-12', True, 430000, 'Normando'),
    ('ARETE-009', '150.00', '2025-10-28', True, 760000, 'Angus'),
    ('ARETE-010', '121.35', '2026-07-01', True, 590000, 'Hereford'),
]

# Coincide con ternero1.jpg, ternero2.png, ternero3.webp, etc.
PATRON_IMAGEN = re.compile(r'^ternero(\d+)\.(jpe?g|png|webp|gif)$', re.IGNORECASE)


class Command(BaseCommand):
    help = 'Elimina los terneros y crea 10 de prueba con sus fotografias reales.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--media-dir',
            default=None,
            help='Carpeta de fotos (por defecto MEDIA_ROOT/terneros).',
        )

    def handle(self, *args, **options):
        carpeta = (
            Path(options['media_dir'])
            if options['media_dir']
            else Path(settings.MEDIA_ROOT) / 'terneros'
        )

        if not carpeta.is_dir():
            raise CommandError(f'No existe la carpeta de imagenes: {carpeta}')

        # Mapa numero -> nombre real del archivo (con su extension verdadera).
        imagenes = {}
        for archivo in sorted(carpeta.iterdir()):
            if not archivo.is_file():
                continue
            coincidencia = PATRON_IMAGEN.match(archivo.name)
            if coincidencia:
                imagenes[int(coincidencia.group(1))] = archivo.name

        if not imagenes:
            raise CommandError(
                f'No se encontraron archivos terneroN.(jpg|jpeg|png|webp|gif) en {carpeta}'
            )

        with transaction.atomic():
            eliminados = Ternero.objects.all().delete()[0]
            self.stdout.write(f'Terneros eliminados: {eliminados}')

            razas = {}
            for nombre, descripcion in RAZAS:
                raza, creada = Raza.objects.get_or_create(
                    nombre=nombre, defaults={'descripcion': descripcion}
                )
                razas[nombre] = raza
                if creada:
                    self.stdout.write(f'Raza creada: {nombre}')

            for indice, (arete, peso, fecha, disponible, precio, raza) in enumerate(
                DATOS_TERNEROS, start=1
            ):
                archivo = imagenes.get(indice)
                ternero = Ternero.objects.create(
                    numero_identificador=arete,
                    peso_kg=peso,
                    fecha_nacimiento=fecha,
                    disponible_venta=disponible,
                    precio_estimado=precio,
                    raza=razas[raza],
                    imagen=f'terneros/{archivo}' if archivo else None,
                )
                foto = ternero.imagen.name if ternero.imagen else 'SIN IMAGEN'
                self.stdout.write(f'  {ternero.numero_identificador} -> {foto}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Listo: {Ternero.objects.count()} terneros con '
                f'{sum(1 for t in Ternero.objects.all() if t.imagen)} fotografias asignadas.'
            )
        )
