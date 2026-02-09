# #  Sistema de Gestión de Cine - Segundo Parcial POO

**Programación Orientada a Objetos**  
**Grupo 9 - Gestión de Servicios de Cine**  
**Universidad Estatal de Guayaquil**

---

##  Integrantes

- Agusto Gómez Javier Rodolfo
- Castillo Sánchez Marco Elías
- Santamaría Cevallos Viviana Sofía
- Luis Miguel Soriano Arias

---

##  Descripción del Proyecto

Sistema de **Gestión de Cine** con interfaz gráfica PyQt6 y base de datos SQL Server. Permite administrar funciones de cine, películas y salas mediante operaciones CRUD completas.

**Características:**
- Interfaz gráfica con Qt Designer (fondo negro, letras blancas)
- Base de datos SQL Server
- CRUD completo (Crear, Leer, Actualizar, Eliminar)
- Arquitectura en 4 capas

---

##  Tecnologías Utilizadas

| Tecnología | Versión |
|------------|---------|
| Python | 3.8+ |
| PyQt6 | 6.6.1 |
| SQL Server | 2019+ |
| pyodbc | 5.0.1 |

---

##  Estructura del Proyecto

```
ProyectoPOO_Parcial2_PyQt_v2/
│
├── Dominio/
│   └── servicioCine.py              # Clase principal (POO)
│
├── Datos/
│   ├── conexion.py                  # Conexión SQL Server (Singleton)
│   └── servicioCine_DAO.py          # CRUD - Patrón DAO
│
├── Servicio/
│   └── servicioCineServicio.py      # Validaciones
│
├── UI/
│   ├── vtnPrincipal.ui              # Diseño Qt Designer
│   └── vtnPrincipal.py              # Controlador
│
├── Main/
│   └── main.py                      # Ejecutor principal
│
├── schema.sql                        # Script de base de datos
├── requirements.txt                  # Dependencias
└── README.md                         # Este archivo
```

---

##  Diagrama de Clases

### Clase Principal: ServicioCine

```python
class ServicioCine:
    # Atributos privados (encapsulados)
    _codigo: str
    _tipo_evento: str
    _nombre: str
    _fecha: datetime
    _precio_base: float
    _sala: int
    _calidad: str          # '2D', '3D', 'VIP'
    _asientos_vendidos: int
    _duracion_min: int
    _estado: str
    
    # Properties (getters/setters)
    @property
    def codigo(self) -> str
    
    @property
    def tipo_evento(self) -> str
    
    # Métodos
    def calcular_precio_total(self) -> float
    def asientos_disponibles(self) -> int
```

### Arquitectura en Capas:

```
┌─────────────────────┐
│   UI (Interfaz)     │  ← PyQt6 - vtnPrincipal.py
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  Servicio (Lógica)  │  ← Validaciones
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│   Datos (DAO)       │  ← CRUD - SQL Server
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│  Dominio (Modelo)   │  ← Clase ServicioCine (POO)
└─────────────────────┘
```

---

##  Base de Datos

**Servidor:** `DESKTOP-7JOFM83`  
**Base de datos:** `CineDB`  
**Tabla:** `ServiciosCine`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| codigo | VARCHAR(10) | PRIMARY KEY |
| tipo_evento | VARCHAR(100) | Tipo de función |
| nombre | VARCHAR(100) | Nombre de película |
| fecha | DATETIME | Fecha y hora |
| precio_base | DECIMAL(10,2) | Precio base |
| sala | INT | Número de sala |
| calidad | VARCHAR(10) | 2D, 3D o VIP |
| asientos_vendidos | INT | Asientos vendidos |
| duracion_min | INT | Duración en minutos |
| estado | VARCHAR(20) | Disponible/Cancelado/Finalizado/En curso |

**Datos de ejemplo:**

| Código | Tipo Evento | Nombre | Calidad |
|--------|-------------|--------|---------|
| C001 | Función Estelar | Superman | 3D |
| C002 | Matinée Familiar | Cómo entrenar a tu dragón | 2D |
| C003 | Función VIP Premium | Los 4 Fantásticos | VIP |
| C004 | Noche de Terror 3D | La hora de la desaparición | 3D |
| C005 | Especial Viernes | Chainsaw man | 2D |

---

##  Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Javier2712A/ProyectoPOO_Parcial2.git
cd ProyectoPOO_Parcial2
```

### 2. Instalar dependencias

```bash
pip install PyQt6 pyodbc
```

### 3. Configurar base de datos

1. Abrir **SQL Server Management Studio (SSMS)**
2. Ejecutar el archivo `schema.sql`
3. Verificar que se creó la base de datos `CineDB`

### 4. Configurar conexión (si es necesario)

Si tu servidor SQL Server es diferente, editar `Datos/conexion.py` línea 11:

```python
_SERVIDOR = 'TU-SERVIDOR-AQUI'  # Cambiar por tu servidor
```

---

##  Instrucciones de Ejecución

```bash
# Ejecutar el programa
python Main/main.py
```

**Salida esperada:**
```
============================================================
  SISTEMA DE GESTIÓN DE CINE - 2DO PARCIAL POO
============================================================

✓ Conexión exitosa a SQL Server
✓ Base de datos: CineDB
✓ Sistema listo para usar
✓ Iniciando interfaz gráfica...
```

La ventana gráfica se abrirá automáticamente.

---

##  Funcionalidades CRUD

### CREATE - Guardar
1. Llenar todos los campos
2. Clic en **"Guardar"** (verde)
3. Confirmación de éxito

### READ - Buscar
1. Ingresar código en "Buscar por código"
2. Clic en **"Buscar"** (azul)
3. Los datos se cargan automáticamente

### UPDATE - Actualizar
1. Primero buscar el servicio
2. Modificar los campos
3. Clic en **"Actualizar"** (naranja)

### DELETE - Eliminar
1. Buscar el servicio
2. Clic en **"Eliminar"** (rojo)
3. Confirmar eliminación

---

##  Conceptos POO Implementados

### 1. Encapsulamiento 
```python
class ServicioCine:
    def __init__(self, codigo, tipo_evento, ...):
        self._codigo = codigo        # Atributo privado
        self._tipo_evento = tipo_evento
    
    @property
    def codigo(self):               # Getter
        return self._codigo
    
    @tipo_evento.setter
    def tipo_evento(self, valor):   # Setter con validación
        if not valor.strip():
            raise ValueError("No puede estar vacío")
        self._tipo_evento = valor
```

### 2. Abstracción 
- Arquitectura en 4 capas
- Separación de responsabilidades
- El usuario no ve la complejidad interna

### 3. Patrones de Diseño 
- **Singleton:** Conexión única a BD
- **DAO:** Separación de lógica de datos
- **MVC:** Separación Modelo-Vista-Controlador

---

##  Capturas de Pantalla

> **Nota:** Las capturas muestran fecha y hora del sistema visibles

### Pantalla Principal
![Pantalla Principal](./capturas/01_pantalla_principal.png)

### Operación CRUD - Guardar
![Guardar](./capturas/02_guardar_servicio.png)

### Operación CRUD - Buscar
![Buscar](./capturas/03_buscar_servicio.png)

### Base de Datos
![SQL Server](./capturas/04_tabla_sql_server.png)

### Consola con Fecha y Hora
![Consola](./capturas/05_consola_ejecucion.png)

---

##  Video Demostrativo

**Duración:** 2 minutos  
**Link:** [Ver Video](COLOCAR-LINK-AQUI)

**Contenido del video:**
- Demostración CRUD completo
- Explicación de clases
- Encapsulamiento
- Patrones de diseño
- Ejecución en vivo

>  **Importante:** Reemplazar `COLOCAR-LINK-AQUI` con el link de tu video en YouTube o Google Drive con permisos de visualización.

---

##  Requisitos del Sistema

- Python 3.8 o superior
- SQL Server (cualquier versión)
- ODBC Driver 17 for SQL Server
- Windows 10/11 (recomendado)

---

##  Solución de Problemas

### Error: "ODBC Driver 17 not found"
**Solución:** Descargar e instalar desde https://go.microsoft.com/fwlink/?linkid=2223304

### Error: "Database 'CineDB' not found"
**Solución:** Ejecutar el archivo `schema.sql` en SSMS

### Error: No puede conectar al servidor
**Solución:** Verificar que SQL Server esté corriendo y cambiar el servidor en `conexion.py`

---

##  Contacto

**Repositorio:** https://github.com/Javier2712A/ProyectoPOO_Parcial2  
**Issues:** https://github.com/Javier2712A/ProyectoPOO_Parcial2/issues

---

##  Licencia

Proyecto académico desarrollado para la asignatura de **Programación Orientada a Objetos** en la **Universidad Estatal de Guayaquil**.

MIT License - Copyright (c) 2026 Grupo 9 - POO

---

<div align="center">

**Desarrollado con ❤️ por el Grupo 9**

Febrero 2026 • Versión 2.0 • ✅ Completo y Funcional

</div>
