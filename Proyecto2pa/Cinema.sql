-- ============================================================================
-- Script SQL Server - Sistema de Gestión de Cine (VERSIÓN ACTUALIZADA)
-- Integrantes: Agusto Gómez Javier Rodolfo, Castillo Sánchez Marco Elías,
--              Santamaría Cevallos Viviana Sofía, Luis Miguel Soriano Arias
-- ============================================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'CineDB')
BEGIN
    CREATE DATABASE CineDB;
    PRINT 'Base de datos CineDB creada.';
END
GO

USE CineDB;
GO

-- Eliminar tabla si existe
IF OBJECT_ID('ServiciosCine', 'U') IS NOT NULL
    DROP TABLE ServiciosCine;
GO

-- Crear tabla ServiciosCine con nueva estructura
CREATE TABLE ServiciosCine (
    codigo VARCHAR(10) PRIMARY KEY NOT NULL,
    tipo_evento VARCHAR(100) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL,
    precio_base DECIMAL(10,2) NOT NULL,
    sala INT NOT NULL,
    calidad VARCHAR(10) NOT NULL DEFAULT '2D',
    asientos_vendidos INT DEFAULT 0,
    duracion_min INT DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'Disponible',
    created_at DATETIME DEFAULT GETDATE()
);
GO

-- Crear índices
CREATE INDEX idx_estado ON ServiciosCine(estado);
CREATE INDEX idx_fecha ON ServiciosCine(fecha);
CREATE INDEX idx_calidad ON ServiciosCine(calidad);
GO

-- Insertar datos de ejemplo actualizados
INSERT INTO ServiciosCine (codigo, tipo_evento, nombre, fecha, precio_base, sala, calidad, asientos_vendidos, duracion_min, estado) 
VALUES 
('C001', 'Función Estelar', 'Superman', CAST('2026-02-10 20:00:00' AS DATETIME), 10.50, 1, '3D', 45, 120, 'Disponible'),
('C002', 'Matinée Familiar', 'Cómo entrenar a tu dragón', CAST('2026-02-11 15:00:00' AS DATETIME), 8.00, 2, '2D', 30, 100, 'Disponible'),
('C003', 'Función VIP Premium', 'Los 4 Fantásticos', CAST('2026-02-12 21:30:00' AS DATETIME), 15.00, 3, 'VIP', 20, 110, 'Disponible'),
('C004', 'Noche de Terror 3D', 'La hora de la desaparición', CAST('2026-02-13 22:00:00' AS DATETIME), 12.50, 4, '3D', 55, 95, 'Disponible'),
('C005', 'Especial Viernes', 'Chainsaw man', CAST('2026-02-14 19:00:00' AS DATETIME), 11.00, 5, '2D', 40, 105, 'Disponible');
GO

PRINT 'Tabla ServiciosCine creada e inicializada correctamente.';
GO

-- Verificar la inserción
SELECT * FROM ServiciosCine;
GO

PRINT 'Total de registros insertados:';
SELECT COUNT(*) AS Total FROM ServiciosCine;
GO
