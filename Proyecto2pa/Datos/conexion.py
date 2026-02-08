# Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
#              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias

import pyodbc as bd


class Conexion:
    _SERVIDOR = 'DESKTOP-7JOFM83'
    _BBDD = 'CineDB'
    _conexion = None
    _cursor = None

    @classmethod
    def obtener_conexion(cls):
        if cls._conexion is None:
            try:
                connection_string = (
                    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                    f'SERVER={cls._SERVIDOR};'
                    f'DATABASE={cls._BBDD};'
                    f'Trusted_Connection=yes;'
                )
                cls._conexion = bd.connect(connection_string)
                print(f" Conexión exitosa a la base de datos: {cls._BBDD}")
            except bd.Error as e:
                print(f" Error al conectar: {e}")
                raise
        return cls._conexion

    @classmethod
    def obtener_cursor(cls):
        if cls._cursor is None or cls._conexion is None:
            conexion = cls.obtener_conexion()
            cls._cursor = conexion.cursor()
        return cls._cursor

    @classmethod
    def cerrar_conexion(cls):
        if cls._cursor is not None:
            cls._cursor.close()
            cls._cursor = None
        if cls._conexion is not None:
            cls._conexion.close()
            cls._conexion = None
            print(" Conexión cerrada")

    @classmethod
    def ejecutar_consulta(cls, consulta: str, parametros: tuple = None) -> list:
        try:
            cursor = cls.obtener_cursor()
            if parametros:
                cursor.execute(consulta, parametros)
            else:
                cursor.execute(consulta)

            columnas = [column[0] for column in cursor.description]
            resultados = []
            for fila in cursor.fetchall():
                fila_dict = {}
                for i, valor in enumerate(fila):
                    fila_dict[columnas[i]] = valor
                resultados.append(fila_dict)
            return resultados
        except bd.Error as e:
            print(f" Error al ejecutar consulta: {e}")
            raise

    @classmethod
    def ejecutar_comando(cls, comando: str, parametros: tuple = None) -> int:
        try:
            conexion = cls.obtener_conexion()
            cursor = cls.obtener_cursor()
            if parametros:
                cursor.execute(comando, parametros)
            else:
                cursor.execute(comando)
            conexion.commit()
            return cursor.rowcount
        except bd.Error as e:
            conexion.rollback()
            print(f" Error al ejecutar comando: {e}")
            raise

    @classmethod
    def probar_conexion(cls) -> bool:
        try:
            conexion = cls.obtener_conexion()
            cursor = cls.obtener_cursor()
            cursor.execute("SELECT 1")
            print(" Prueba de conexión exitosa")
            return True
        except Exception as e:
            print(f" Prueba de conexión fallida: {e}")
            return False
