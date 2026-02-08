# Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
#              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias

"""
Módulo: main.py
Descripción: Punto de entrada principal del sistema de gestión de cine con PyQt6
             Proyecto 2do Parcial - POO + UI (Qt Designer) + CRUD con SQL Server
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication, QMessageBox
from Datos.conexion import Conexion
from UI.vtnPrincipal import VtnPrincipal


def verificar_conexion():
    """
    Verifica la conexión a la base de datos antes de iniciar la aplicación.

    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    print("  SISTEMA DE GESTIÓN DE CINE - 2DO PARCIAL POO")
    print()
    print("Integrantes:")
    print("  • Agusto Gómez Javier Rodolfo")
    print("  • Castillo Sánchez Marco Elías")
    print("  • Santamaría Cevallos Viviana Sofía")
    print("  • Luis Miguel Soriano Arias")
    print()
    print("Verificando conexión a la base de datos...")
    print()

    try:
        if Conexion.probar_conexion():
            print(" Conexión a SQL Server exitosa")
            print(" Base de datos: CineDB")
            print(" Servidor: DESKTOP-7JOFM83")
            print()
            print(" Sistema listo para usar")
            print(" Iniciando interfaz gráfica...")
            print()
            return True
        else:
            print("\n No se pudo conectar a la base de datos")
            return False

    except Exception as e:
        print(f"\n Error al verificar conexión: {e}")
        print("\n IMPORTANTE:")
        print("  1. Verifique que SQL Server esté corriendo")
        print("  2. Verifique que la base de datos 'CineDB' exista")
        print("  3. Ejecute el script 'schema.sql' si es la primera vez")
        print("  4. Verifique que tenga permisos de acceso")
        return False


def main():
    """
    Función principal del programa.
    """
    app = QApplication(sys.argv)

    if not verificar_conexion():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Error de Conexión")
        msg.setText("No se pudo conectar a la base de datos SQL Server")
        msg.setInformativeText(
            "Verifique:\n"
            "1. SQL Server esté corriendo\n"
            "2. Base de datos 'CineDB' exista\n"
            "3. Haya ejecutado 'schema.sql'\n"
            "4. Tenga permisos de acceso"
        )
        msg.exec()
        sys.exit(1)

    try:
        ventana = VtnPrincipal()
        ventana.show()

        exit_code = app.exec()

        Conexion.cerrar_conexion()
        print("\n Sistema cerrado correctamente")

        sys.exit(exit_code)

    except Exception as e:
        print(f"\n Error al ejecutar la aplicación: {e}")
        Conexion.cerrar_conexion()
        sys.exit(1)


if __name__ == "__main__":
    main()
