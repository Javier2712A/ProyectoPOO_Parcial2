# Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
#              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias

"""
Módulo: servicioCineServicio.py
Descripción: Capa de lógica de negocio para ServicioCine
"""

from datetime import datetime, date, time
from Dominio.servicioCine import ServicioCine
from Datos.servicioCine_DAO import ServicioCineDAO


class ServicioCineServicio:
    """
    Clase de servicio que contiene la lógica de negocio y validaciones
    para las operaciones CRUD de ServicioCine.
    """

    # VALIDACIONES

    @staticmethod
    def validar_codigo(codigo: str) -> tuple:
        """Valida el formato del código"""
        if not codigo or not codigo.strip():
            return False, "El código no puede estar vacío"
        if len(codigo.strip()) < 3:
            return False, "El código debe tener al menos 3 caracteres"
        if len(codigo.strip()) > 10:
            return False, "El código no puede tener más de 10 caracteres"
        return True, ""

    @staticmethod
    def validar_tipo_evento(tipo_evento: str) -> tuple:
        """Valida el tipo de evento"""
        if not tipo_evento or not tipo_evento.strip():
            return False, "El tipo de evento no puede estar vacío"
        if len(tipo_evento.strip()) < 5:
            return False, "El tipo de evento debe tener al menos 5 caracteres"
        return True, ""

    @staticmethod
    def validar_nombre(nombre: str) -> tuple:
        """Valida el nombre de la película"""
        if not nombre or not nombre.strip():
            return False, "El nombre no puede estar vacío"
        if len(nombre.strip()) < 2:
            return False, "El nombre debe tener al menos 2 caracteres"
        return True, ""

    @staticmethod
    def validar_precio(precio: float) -> tuple:
        """Valida el precio base"""
        try:
            precio_float = float(precio)
            if precio_float < 0:
                return False, "El precio no puede ser negativo"
            if precio_float == 0:
                return False, "El precio debe ser mayor a 0"
            if precio_float > 1000:
                return False, "El precio no puede ser mayor a $1000"
            return True, ""
        except (ValueError, TypeError):
            return False, "El precio debe ser un número válido"

    @staticmethod
    def validar_sala(sala: int) -> tuple:
        """Valida el número de sala"""
        try:
            sala_int = int(sala)
            if sala_int < 1:
                return False, "El número de sala debe ser mayor a 0"
            if sala_int > 20:
                return False, "El número de sala no puede ser mayor a 20"
            return True, ""
        except (ValueError, TypeError):
            return False, "El número de sala debe ser un número entero válido"

    @staticmethod
    def validar_asientos(asientos: int) -> tuple:
        """Valida la cantidad de asientos vendidos"""
        try:
            asientos_int = int(asientos)
            if asientos_int < 0:
                return False, "Los asientos no pueden ser negativos"
            if asientos_int > ServicioCine.CAPACIDAD_SALA:
                return False, f"Los asientos no pueden superar {ServicioCine.CAPACIDAD_SALA}"
            return True, ""
        except (ValueError, TypeError):
            return False, "Los asientos deben ser un número entero válido"

    @staticmethod
    def validar_duracion(duracion: int) -> tuple:
        """Valida la duración en minutos"""
        try:
            duracion_int = int(duracion)
            if duracion_int < 0:
                return False, "La duración no puede ser negativa"
            if duracion_int > 300:
                return False, "La duración no puede ser mayor a 300 minutos"
            return True, ""
        except (ValueError, TypeError):
            return False, "La duración debe ser un número entero válido"

    # OPERACIONES CRUD CON VALIDACIÓN

    @classmethod
    def crear_servicio(cls, codigo: str, tipo_evento: str, nombre: str, fecha: date, hora: time,
                       precio_base: float, sala: int, calidad: str,
                       asientos_vendidos: int, duracion_min: int, estado: str) -> tuple:
        """Crea y guarda un nuevo servicio con validaciones."""

        # Validar código
        valido, mensaje = cls.validar_codigo(codigo)
        if not valido:
            return False, mensaje, None

        # Verificar que el código no exista
        servicio_existente = ServicioCineDAO.seleccionar_por_codigo(codigo)
        if servicio_existente:
            return False, f"Ya existe un servicio con el código '{codigo}'", None

        # Validar tipo de evento
        valido, mensaje = cls.validar_tipo_evento(tipo_evento)
        if not valido:
            return False, mensaje, None

        # Validar nombre
        valido, mensaje = cls.validar_nombre(nombre)
        if not valido:
            return False, mensaje, None

        # Validar precio
        valido, mensaje = cls.validar_precio(precio_base)
        if not valido:
            return False, mensaje, None

        # Validar sala
        valido, mensaje = cls.validar_sala(sala)
        if not valido:
            return False, mensaje, None

        # Validar asientos
        valido, mensaje = cls.validar_asientos(asientos_vendidos)
        if not valido:
            return False, mensaje, None

        # Validar duración
        valido, mensaje = cls.validar_duracion(duracion_min)
        if not valido:
            return False, mensaje, None

        # Crear objeto ServicioCine
        try:
            servicio = ServicioCine(
                codigo=codigo.strip(),
                tipo_evento=tipo_evento.strip(),
                nombre=nombre.strip(),
                fecha=fecha,
                hora=hora,
                precio_base=float(precio_base),
                sala=int(sala),
                calidad=calidad,
                asientos_vendidos=int(asientos_vendidos),
                duracion_min=int(duracion_min),
                estado=estado
            )

            # Insertar en la base de datos
            exito = ServicioCineDAO.insertar(servicio)

            if exito:
                return True, "Servicio creado exitosamente", servicio
            else:
                return False, "Error al guardar el servicio en la base de datos", None

        except Exception as e:
            return False, f"Error al crear servicio: {str(e)}", None

    @classmethod
    def buscar_servicio(cls, codigo: str) -> tuple:
        """Busca un servicio por código."""
        try:
            if not codigo or not codigo.strip():
                return False, "Debe proporcionar un código", None

            servicio = ServicioCineDAO.seleccionar_por_codigo(codigo.strip())
            if servicio:
                return True, "Servicio encontrado", servicio
            else:
                return False, f"No se encontró servicio con código '{codigo}'", None

        except Exception as e:
            return False, f"Error al buscar servicio: {str(e)}", None

    @classmethod
    def actualizar_servicio(cls, servicio: ServicioCine) -> tuple:
        """Actualiza un servicio existente con validaciones."""

        # Validaciones
        valido, mensaje = cls.validar_tipo_evento(servicio.tipo_evento)
        if not valido:
            return False, mensaje

        valido, mensaje = cls.validar_nombre(servicio.nombre)
        if not valido:
            return False, mensaje

        valido, mensaje = cls.validar_precio(servicio.precio_base)
        if not valido:
            return False, mensaje

        valido, mensaje = cls.validar_sala(servicio.sala)
        if not valido:
            return False, mensaje

        valido, mensaje = cls.validar_asientos(servicio.asientos_vendidos)
        if not valido:
            return False, mensaje

        valido, mensaje = cls.validar_duracion(servicio.duracion_min)
        if not valido:
            return False, mensaje

        # Actualizar en la base de datos
        try:
            exito = ServicioCineDAO.actualizar(servicio)
            if exito:
                return True, "Servicio actualizado exitosamente"
            else:
                return False, "No se pudo actualizar el servicio"
        except Exception as e:
            return False, f"Error al actualizar servicio: {str(e)}"

    @classmethod
    def eliminar_servicio(cls, codigo: str) -> tuple:
        """Elimina un servicio de la base de datos."""
        try:
            if not codigo or not codigo.strip():
                return False, "Código inválido"

            exito = ServicioCineDAO.eliminar(codigo.strip())
            if exito:
                return True, "Servicio eliminado exitosamente"
            else:
                return False, "No se encontró el servicio a eliminar"
        except Exception as e:
            return False, f"Error al eliminar servicio: {str(e)}"

    @classmethod
    def listar_todos(cls) -> list:
        """Obtiene la lista de todos los servicios."""
        try:
            return ServicioCineDAO.seleccionar_todos()
        except Exception as e:
            print(f"Error al listar servicios: {e}")
            return []

    @classmethod
    def obtener_estadisticas(cls) -> dict:
        """Obtiene estadísticas generales del sistema."""
        try:
            servicios = ServicioCineDAO.seleccionar_todos()

            total = len(servicios)
            servicios_2d = sum(1 for s in servicios if s.calidad == '2D')
            servicios_3d = sum(1 for s in servicios if s.calidad == '3D')
            servicios_vip = sum(1 for s in servicios if s.calidad == 'VIP')
            asientos_totales = sum(s.asientos_vendidos for s in servicios)
            ingresos_estimados = sum(s.calcular_precio_total() * s.asientos_vendidos for s in servicios)

            return {
                'total_servicios': total,
                'servicios_2d': servicios_2d,
                'servicios_3d': servicios_3d,
                'servicios_vip': servicios_vip,
                'total_asientos_vendidos': asientos_totales,
                'ingresos_estimados': round(ingresos_estimados, 2)
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}