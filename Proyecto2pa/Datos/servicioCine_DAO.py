# Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
#              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias

"""
Módulo: servicioCine_DAO.py
Descripción: Data Access Object para operaciones CRUD de ServicioCine con SQL Server
"""

from datetime import datetime, date, time
from Datos.conexion import Conexion
from Dominio.servicioCine import ServicioCine


class ServicioCineDAO:
    """
    Clase DAO para manejar operaciones CRUD de ServicioCine en SQL Server.
    """


    @classmethod
    def insertar(cls, servicio: ServicioCine) -> bool:
        """Inserta un nuevo servicio de cine en SQL Server."""
        try:
            sql = """
                INSERT INTO ServiciosCine 
                (codigo, tipo_evento, nombre, fecha, hora, precio_base, sala, calidad, asientos_vendidos, duracion_min, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            fecha_str = servicio.fecha.strftime('%Y-%m-%d') if isinstance(servicio.fecha, date) else servicio.fecha
            hora_str = servicio.hora.strftime('%H:%M:%S') if isinstance(servicio.hora, time) else servicio.hora

            parametros = (
                servicio.codigo,
                servicio.tipo_evento,
                servicio.nombre,
                fecha_str,
                hora_str,
                servicio.precio_base,
                servicio.sala,
                servicio.calidad,
                servicio.asientos_vendidos,
                servicio.duracion_min,
                servicio.estado
            )

            Conexion.ejecutar_comando(sql, parametros)
            print(f"✓ Servicio insertado correctamente: {servicio.codigo}")
            return True

        except Exception as e:
            print(f"✗ Error al insertar servicio: {e}")
            return False


    @classmethod
    def seleccionar_todos(cls) -> list:
        """Obtiene todos los servicios de cine de SQL Server."""
        try:
            sql = "SELECT * FROM ServiciosCine ORDER BY fecha DESC, hora DESC"
            registros = Conexion.ejecutar_consulta(sql)

            servicios = []
            for registro in registros:
                servicio = cls._crear_objeto_desde_registro(registro)
                servicios.append(servicio)

            return servicios

        except Exception as e:
            print(f"✗ Error al seleccionar servicios: {e}")
            return []

    @classmethod
    def seleccionar_por_codigo(cls, codigo: str):
        """Busca un servicio por su código."""
        try:
            sql = "SELECT * FROM ServiciosCine WHERE codigo = ?"
            registros = Conexion.ejecutar_consulta(sql, (codigo,))

            if registros:
                return cls._crear_objeto_desde_registro(registros[0])
            return None

        except Exception as e:
            print(f"✗ Error al buscar servicio por código: {e}")
            return None

    @classmethod
    def buscar_por_nombre(cls, nombre: str) -> list:
        """Busca servicios por nombre de película."""
        try:
            sql = "SELECT * FROM ServiciosCine WHERE nombre LIKE ? ORDER BY fecha DESC, hora DESC"
            registros = Conexion.ejecutar_consulta(sql, (f'%{nombre}%',))

            servicios = []
            for registro in registros:
                servicio = cls._crear_objeto_desde_registro(registro)
                servicios.append(servicio)

            return servicios

        except Exception as e:
            print(f"✗ Error al buscar por nombre: {e}")
            return []


    @classmethod
    def actualizar(cls, servicio: ServicioCine) -> bool:
        """Actualiza un servicio existente en SQL Server."""
        try:
            sql = """
                UPDATE ServiciosCine
                SET tipo_evento = ?, nombre = ?, fecha = ?, hora = ?, precio_base = ?,
                    sala = ?, calidad = ?, asientos_vendidos = ?, duracion_min = ?, estado = ?
                WHERE codigo = ?
            """

            fecha_str = servicio.fecha.strftime('%Y-%m-%d') if isinstance(servicio.fecha, date) else servicio.fecha
            hora_str = servicio.hora.strftime('%H:%M:%S') if isinstance(servicio.hora, time) else servicio.hora

            parametros = (
                servicio.tipo_evento,
                servicio.nombre,
                fecha_str,
                hora_str,
                servicio.precio_base,
                servicio.sala,
                servicio.calidad,
                servicio.asientos_vendidos,
                servicio.duracion_min,
                servicio.estado,
                servicio.codigo
            )

            filas_afectadas = Conexion.ejecutar_comando(sql, parametros)

            if filas_afectadas > 0:
                print(f"✓ Servicio actualizado correctamente: {servicio.codigo}")
                return True
            else:
                print(f"✗ No se encontró el servicio: {servicio.codigo}")
                return False

        except Exception as e:
            print(f"✗ Error al actualizar servicio: {e}")
            return False


    @classmethod
    def eliminar(cls, codigo: str) -> bool:
        """Elimina un servicio de SQL Server por su código."""
        try:
            sql = "DELETE FROM ServiciosCine WHERE codigo = ?"
            filas_afectadas = Conexion.ejecutar_comando(sql, (codigo,))

            if filas_afectadas > 0:
                print(f"✓ Servicio eliminado correctamente: {codigo}")
                return True
            else:
                print(f"✗ No se encontró el servicio: {codigo}")
                return False

        except Exception as e:
            print(f"✗ Error al eliminar servicio: {e}")
            return False


    @classmethod
    def _crear_objeto_desde_registro(cls, registro: dict) -> ServicioCine:
        """Crea un objeto ServicioCine desde un registro de SQL Server."""

        # Convertir fecha (puede venir como datetime.date o str)
        fecha_obj = registro['fecha']
        if isinstance(fecha_obj, str):
            fecha_obj = datetime.strptime(fecha_obj, '%Y-%m-%d').date()
        elif isinstance(fecha_obj, datetime):
            fecha_obj = fecha_obj.date()

        # Convertir hora (puede venir como datetime.time o str)
        hora_obj = registro['hora']
        if isinstance(hora_obj, str):
            hora_obj = datetime.strptime(hora_obj, '%H:%M:%S').time()
        elif isinstance(hora_obj, datetime):
            hora_obj = hora_obj.time()

        return ServicioCine(
            codigo=registro['codigo'],
            tipo_evento=registro['tipo_evento'],
            nombre=registro['nombre'],
            fecha=fecha_obj,
            hora=hora_obj,
            precio_base=float(registro['precio_base']),
            sala=int(registro['sala']),
            calidad=registro['calidad'],
            asientos_vendidos=int(registro['asientos_vendidos']),
            duracion_min=int(registro.get('duracion_min', 0)),
            estado=registro['estado']
        )

    @classmethod
    def contar_servicios(cls) -> int:
        """Cuenta el total de servicios en SQL Server."""
        try:
            sql = "SELECT COUNT(*) as total FROM ServiciosCine"
            resultado = Conexion.ejecutar_consulta(sql)
            return resultado[0]['total'] if resultado else 0
        except Exception as e:
            print(f" Error al contar servicios: {e}")
            return 0