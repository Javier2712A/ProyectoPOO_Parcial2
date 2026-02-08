# Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
#              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias

"""
Módulo: vtnPrincipal.py
Descripción: Ventana principal de la aplicación con interfaz Qt Designer
"""

import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import uic

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Dominio.servicioCine import ServicioCine
from Servicio.servicioCineServicio import ServicioCineServicio


class VtnPrincipal(QMainWindow):
    """
    Ventana principal del sistema de gestión de cine.
    Carga la interfaz desde el archivo .ui y maneja los eventos CRUD.
    """

    def __init__(self):
        """Constructor de la ventana principal"""
        super().__init__()

        # Cargar la interfaz desde el archivo .ui
        ui_path = os.path.join(os.path.dirname(__file__), 'vtnPrincipal.ui')
        uic.loadUi(ui_path, self)

        # Variable para almacenar el servicio actual
        self.servicio_actual = None

        # Conectar eventos de los botones
        self.conectar_eventos()

        # Inicializar valores por defecto
        self.inicializar_valores()

        # Centrar ventana
        self.centrar_ventana()

    def conectar_eventos(self):
        """Conecta los eventos de los botones con sus respectivos métodos"""
        self.btnGuardar.clicked.connect(self.guardar_servicio)
        self.btnBuscar.clicked.connect(self.buscar_servicio)
        self.btnActualizar.clicked.connect(self.actualizar_servicio)
        self.btnEliminar.clicked.connect(self.eliminar_servicio)
        self.btnLimpiar.clicked.connect(self.limpiar_campos)

    def inicializar_valores(self):
        """Inicializa valores por defecto en los campos"""
        fecha_actual = datetime.now()
        self.txtFecha.setText(fecha_actual.strftime('%d-%m-%Y'))
        self.txtHora.setText('20:00')
        self.txtAsientos.setText('0')
        self.txtDuracion.setText('0')
        self.cbxTipoEvento.setCurrentIndex(0)  # Función Estelar
        self.cbxEstado.setCurrentIndex(0)  # Disponible
        self.cbxCalidad.setCurrentIndex(0)  # 2D

    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(
            int((screen.width() - size.width()) / 2),
            int((screen.height() - size.height()) / 2)
        )

    # ==================== MÉTODOS CRUD ====================

    def guardar_servicio(self):
        """Guarda un nuevo servicio (CREATE)"""
        try:
            # Obtener datos del formulario
            codigo = self.txtCodigo.text().strip()
            tipo_evento = self.cbxTipoEvento.currentText()
            nombre = self.txtNombre.text().strip()
            fecha_str = self.txtFecha.text().strip()
            hora_str = self.txtHora.text().strip()
            precio = self.txtPrecio.text().strip()
            sala = self.txtSala.text().strip()
            asientos = self.txtAsientos.text().strip()
            duracion = self.txtDuracion.text().strip()
            calidad = self.cbxCalidad.currentText()
            estado = self.cbxEstado.currentText()

            # Validar campos vacíos
            if not all([codigo, tipo_evento, nombre, fecha_str, hora_str, precio, sala]):
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Todos los campos obligatorios deben estar llenos"
                )
                return

            # Convertir fecha y hora SEPARADAMENTE
            try:
                # Convertir fecha (DD-MM-YYYY a date)
                fecha_obj = datetime.strptime(fecha_str, '%d-%m-%Y').date()

                # Convertir hora (HH:MM a time)
                hora_obj = datetime.strptime(hora_str, '%H:%M').time()

            except ValueError:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Formato de fecha u hora inválido\nFecha: DD-MM-YYYY\nHora: HH:MM"
                )
                return

            # Crear servicio usando la capa de servicio
            exito, mensaje, servicio = ServicioCineServicio.crear_servicio(
                codigo=codigo,
                tipo_evento=tipo_evento,
                nombre=nombre,
                fecha=fecha_obj,
                hora=hora_obj,
                precio_base=float(precio),
                sala=int(sala),
                calidad=calidad,
                asientos_vendidos=int(asientos),
                duracion_min=int(duracion),
                estado=estado
            )

            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Error", mensaje)

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error en los datos ingresados:\n{str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error inesperado:\n{str(e)}"
            )

    def buscar_servicio(self):
        """Busca un servicio por código (READ)"""
        try:
            codigo = self.txtBuscarCodigo.text().strip()

            if not codigo:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Debe ingresar un código para buscar"
                )
                return

            # Buscar servicio
            exito, mensaje, servicio = ServicioCineServicio.buscar_servicio(codigo)

            if exito and servicio:
                # Cargar datos en el formulario
                self.servicio_actual = servicio
                self.txtCodigo.setText(servicio.codigo)

                # Establecer ComboBox de Tipo de Evento
                index_tipo = self.cbxTipoEvento.findText(servicio.tipo_evento)
                if index_tipo >= 0:
                    self.cbxTipoEvento.setCurrentIndex(index_tipo)

                self.txtNombre.setText(servicio.nombre)

                # CORRECCIÓN: Separar fecha y hora
                self.txtFecha.setText(servicio.fecha.strftime('%d-%m-%Y'))
                self.txtHora.setText(servicio.hora.strftime('%H:%M'))

                self.txtPrecio.setText(str(servicio.precio_base))
                self.txtSala.setText(str(servicio.sala))
                self.txtAsientos.setText(str(servicio.asientos_vendidos))
                self.txtDuracion.setText(str(servicio.duracion_min))

                # Establecer combobox
                index_estado = self.cbxEstado.findText(servicio.estado)
                if index_estado >= 0:
                    self.cbxEstado.setCurrentIndex(index_estado)

                index_calidad = self.cbxCalidad.findText(servicio.calidad)
                if index_calidad >= 0:
                    self.cbxCalidad.setCurrentIndex(index_calidad)

                QMessageBox.information(self, "Éxito", mensaje)
            else:
                QMessageBox.warning(self, "No encontrado", mensaje)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al buscar:\n{str(e)}"
            )

    def actualizar_servicio(self):
        """Actualiza un servicio existente (UPDATE)"""
        try:
            if not self.servicio_actual:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Primero debe buscar un servicio para actualizar"
                )
                return

            # Obtener datos del formulario
            tipo_evento = self.cbxTipoEvento.currentText()
            nombre = self.txtNombre.text().strip()
            fecha_str = self.txtFecha.text().strip()
            hora_str = self.txtHora.text().strip()
            precio = self.txtPrecio.text().strip()
            sala = self.txtSala.text().strip()
            asientos = self.txtAsientos.text().strip()
            duracion = self.txtDuracion.text().strip()
            calidad = self.cbxCalidad.currentText()
            estado = self.cbxEstado.currentText()

            # Validar campos vacíos
            if not all([tipo_evento, nombre, fecha_str, hora_str, precio, sala]):
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Todos los campos obligatorios deben estar llenos"
                )
                return

            # Convertir fecha y hora SEPARADAMENTE
            try:
                # Convertir fecha (DD-MM-YYYY a date)
                fecha_obj = datetime.strptime(fecha_str, '%d-%m-%Y').date()

                # Convertir hora (HH:MM a time)
                hora_obj = datetime.strptime(hora_str, '%H:%M').time()

            except ValueError:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Formato de fecha u hora inválido"
                )
                return

            # Actualizar objeto servicio
            self.servicio_actual.tipo_evento = tipo_evento
            self.servicio_actual.nombre = nombre
            self.servicio_actual.fecha = fecha_obj
            self.servicio_actual.hora = hora_obj
            self.servicio_actual.precio_base = float(precio)
            self.servicio_actual.sala = int(sala)
            self.servicio_actual.calidad = calidad
            self.servicio_actual.asientos_vendidos = int(asientos)
            self.servicio_actual.duracion_min = int(duracion)
            self.servicio_actual.estado = estado

            # Actualizar usando la capa de servicio
            exito, mensaje = ServicioCineServicio.actualizar_servicio(self.servicio_actual)

            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.limpiar_campos()
            else:
                QMessageBox.warning(self, "Error", mensaje)

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Error en los datos ingresados:\n{str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error inesperado:\n{str(e)}"
            )

    def eliminar_servicio(self):
        """Elimina un servicio (DELETE)"""
        try:
            if not self.servicio_actual:
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    "Primero debe buscar un servicio para eliminar"
                )
                return

            # Confirmar eliminación
            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Está seguro de eliminar el servicio '{self.servicio_actual.codigo}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if respuesta == QMessageBox.StandardButton.Yes:
                # Eliminar usando la capa de servicio
                exito, mensaje = ServicioCineServicio.eliminar_servicio(
                    self.servicio_actual.codigo
                )

                if exito:
                    QMessageBox.information(self, "Éxito", mensaje)
                    self.limpiar_campos()
                else:
                    QMessageBox.warning(self, "Error", mensaje)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al eliminar:\n{str(e)}"
            )

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.txtBuscarCodigo.clear()
        self.txtCodigo.clear()
        self.txtNombre.clear()
        self.txtPrecio.clear()
        self.txtSala.clear()
        self.txtAsientos.setText('0')
        self.txtDuracion.setText('0')

        fecha_actual = datetime.now()
        self.txtFecha.setText(fecha_actual.strftime('%d-%m-%Y'))
        self.txtHora.setText('20:00')

        self.cbxTipoEvento.setCurrentIndex(0)  # Función Estelar
        self.cbxEstado.setCurrentIndex(0)  # Disponible
        self.cbxCalidad.setCurrentIndex(0)  # 2D

        self.servicio_actual = None


# Prueba del módulo
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VtnPrincipal()
    ventana.show()
    sys.exit(app.exec())