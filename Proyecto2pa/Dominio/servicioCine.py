# Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
#              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias

"""
Módulo: servicioCine.py
Descripción: Clase que representa un servicio de cine (POO)
"""

from datetime import datetime, date, time


class ServicioCine:
    """
    Clase que representa un servicio de cine.
    Implementa conceptos de POO: Encapsulamiento con properties.
    """

    CAPACIDAD_SALA = 100

    def __init__(self, codigo: str, tipo_evento: str, nombre: str, fecha: date, hora: time,
                 precio_base: float, sala: int, calidad: str = "2D",
                 asientos_vendidos: int = 0, duracion_min: int = 0, estado: str = "Disponible"):
        self._codigo = codigo
        self._tipo_evento = tipo_evento
        self._nombre = nombre
        self._fecha = fecha  # Ahora es date, no datetime
        self._hora = hora    # Nuevo campo separado
        self._precio_base = precio_base
        self._sala = sala
        self._calidad = calidad
        self._asientos_vendidos = asientos_vendidos
        self._duracion_min = duracion_min
        self._estado = estado

    # Properties
    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, v):
        self._codigo = v.strip() if v else ""

    @property
    def tipo_evento(self):
        return self._tipo_evento

    @tipo_evento.setter
    def tipo_evento(self, v):
        self._tipo_evento = v.strip() if v else ""

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, v):
        self._nombre = v.strip() if v else ""

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, v):
        self._fecha = v

    @property
    def hora(self):
        return self._hora

    @hora.setter
    def hora(self, v):
        self._hora = v

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, v):
        self._precio_base = float(v) if v else 0.0

    @property
    def sala(self):
        return self._sala

    @sala.setter
    def sala(self, v):
        self._sala = int(v) if v else 0

    @property
    def calidad(self):
        return self._calidad

    @calidad.setter
    def calidad(self, v):
        self._calidad = v if v in ['2D', '3D', 'VIP'] else '2D'

    @property
    def asientos_vendidos(self):
        return self._asientos_vendidos

    @asientos_vendidos.setter
    def asientos_vendidos(self, v):
        self._asientos_vendidos = int(v) if v else 0

    @property
    def duracion_min(self):
        return self._duracion_min

    @duracion_min.setter
    def duracion_min(self, v):
        self._duracion_min = int(v) if v else 0

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, v):
        self._estado = v

    def calcular_precio_total(self) -> float:
        """Calcula el precio total con recargos"""
        precio = self._precio_base
        if self._calidad == '3D':
            precio *= 1.30
        elif self._calidad == 'VIP':
            precio *= 1.50
        # Verificar si es antes de las 17:00 (5 PM)
        if self._hora.hour < 17:
            precio *= 0.80
        return round(precio, 2)

    def asientos_disponibles(self) -> int:
        return self.CAPACIDAD_SALA - self._asientos_vendidos

    def __str__(self):
        return f"{self._codigo} - {self._nombre} - Sala {self._sala} ({self._calidad})"
