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

**Datos de ejemplo:**

| Código | Tipo Evento | Nombre | Calidad |
|--------|-------------|--------|---------|
| C001 | Función Estelar | Superman | 3D |
| C002 | Matinée Familiar | Cómo entrenar a tu dragón | 2D |
| C003 | Función VIP Premium | Los 4 Fantásticos | VIP |
| C004 | Noche de Terror 3D | La hora de la desaparición | 3D |
| C005 | Especial Viernes | Chainsaw man | 2D |

---

##  Instrucciones de Ejecución

```bash
# Ejecutar el programa
python Main/main.py
```

**Salida esperada:**
```

  SISTEMA DE GESTIÓN DE CINE - 2DO PARCIAL POO

 Conexión exitosa a SQL Server
 Base de datos: CineDB
 Sistema listo para usar
 Iniciando interfaz gráfica...
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
![Pantalla Principal](<img width="1600" height="900" alt="Captura de pantalla 2026-02-08 221556" src="https://github.com/user-attachments/assets/f09d6ec0-e57a-4bd6-9d34-8bc45834c84e" />
)

### Operación CRUD - Guardar
![Guardar](<img width="1600" height="900" alt="Captura de pantalla 2026-02-08 221844" src="https://github.com/user-attachments/assets/2a285507-775e-47e3-8c89-e33f2c638220" />
)

### Operación CRUD - Buscar
![Buscar](<img width="1600" height="900" alt="Captura de pantalla 2026-02-08 221903" src="https://github.com/user-attachments/assets/d8d38a27-2ec4-47f0-b7b3-9dd606eefb07" />
)

### Base de Datos
![SQL Server](<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/c155fed8-d11b-46a7-a249-f4d66f0a2daf" />
)

### Consola con Fecha y Hora
![Consola](<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/550ac06c-677b-418e-9d1a-11592f3787ed" />
)

---

##  Video Demostrativo

**Duración:** 2 minutos  
**Link:** [Ver Video](https://drive.google.com/file/d/1qGOWsKdjGw-IsmTRv3R80Z26qNe8b-4W/view?usp=sharing)

**Contenido del video:**
- Demostración CRUD completo
- Explicación de clases
- Encapsulamiento
- Patrones de diseño
- Ejecución en vivo

---

<div align="center">

**Desarrollado con ❤️ por el Grupo 9**

Febrero 2026 • Versión 2.0 • ✅ Completo y Funcional

</div>
