-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-06-2026 a las 05:31:53
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tablas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `ID_usuario` int(11) NOT NULL,
  `user` varchar(59) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Fecha_Registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `ID_alumno` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `no_control` varchar(20) NOT NULL,
  `ID_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `ID_profesor` int(11) NOT NULL,
  `nombre` varchar(59) NOT NULL,
  `apellido` varchar(59) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  `Fecha_Registro` date NOT NULL,
  `ID_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesor_alumno`
--

CREATE TABLE `profesor_alumno` (
  `ID_relacion` int(11) NOT NULL,
  `ID_profesor` int(11) NOT NULL,
  `ID_alumno` int(11) NOT NULL,
  `fecha_asignacion` datetime NOT NULL,
  `estado` enum('activo','inactivo') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitudes_profesor`
--

CREATE TABLE `solicitudes_profesor` (
  `ID_solicitud` int(11) NOT NULL,
  `ID_alumno` int(11) NOT NULL,
  `ID_profesor` int(11) NOT NULL,
  `fecha_solicitud` datetime NOT NULL,
  `estado` enum('pendiente','aceptada','rechazada') DEFAULT 'pendiente',
  `mensaje` text DEFAULT NULL,
  `fecha_respuesta` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajos`
--

CREATE TABLE `trabajos` (
  `ID_trabajo` int(11) NOT NULL,
  `ID_alumno` int(11) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `titulo_trabajo` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_entrega` date DEFAULT NULL,
  `calificacion` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentarios`
--

CREATE TABLE `comentarios` (
  `ID_comentario` int(11) NOT NULL,
  `ID_trabajo` int(11) NOT NULL,
  `ID_usuario` int(11) NOT NULL,
  `comentario` text NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones`
--

CREATE TABLE `calificaciones` (
  `ID_calificacion` int(11) NOT NULL,
  `ID_alumno` int(11) NOT NULL,
  `Materia` varchar(100) NOT NULL,
  `Unidad1` float DEFAULT NULL,
  `Unidad2` float DEFAULT NULL,
  `Unidad3` float DEFAULT NULL,
  `Promedio` float GENERATED ALWAYS AS ((`Unidad1` + `Unidad2` + `Unidad3`) / 3) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comentarios_calificaciones`
--

CREATE TABLE `comentarios_calificaciones` (
  `ID_comentario` int(11) NOT NULL,
  `ID_calificacion` int(11) NOT NULL,
  `ID_usuario` int(11) NOT NULL,
  `comentario` text NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Índices para tablas volcadas
--

-- Índices de la tabla `usuarios`
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`ID_usuario`),
  ADD UNIQUE KEY `Email` (`Email`);

-- Índices de la tabla `alumnos`
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`ID_alumno`),
  ADD UNIQUE KEY `no_control` (`no_control`),
  ADD KEY `ID_usuario` (`ID_usuario`);

-- Índices de la tabla `profesores`
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`ID_profesor`),
  ADD UNIQUE KEY `Email` (`Email`),
  ADD KEY `ID_usuario` (`ID_usuario`);

-- Índices de la tabla `profesor_alumno`
ALTER TABLE `profesor_alumno`
  ADD PRIMARY KEY (`ID_relacion`),
  ADD UNIQUE KEY `unique_relacion` (`ID_profesor`,`ID_alumno`),
  ADD KEY `idx_profesor` (`ID_profesor`),
  ADD KEY `idx_alumno` (`ID_alumno`);

-- Índices de la tabla `solicitudes_profesor`
ALTER TABLE `solicitudes_profesor`
  ADD PRIMARY KEY (`ID_solicitud`),
  ADD KEY `idx_alumno` (`ID_alumno`),
  ADD KEY `idx_profesor` (`ID_profesor`),
  ADD KEY `idx_estado` (`estado`),
  ADD KEY `idx_fecha` (`fecha_solicitud`);

-- Índices de la tabla `trabajos`
ALTER TABLE `trabajos`
  ADD PRIMARY KEY (`ID_trabajo`),
  ADD KEY `ID_alumno` (`ID_alumno`);

-- Índices de la tabla `comentarios`
ALTER TABLE `comentarios`
  ADD PRIMARY KEY (`ID_comentario`),
  ADD KEY `idx_trabajo` (`ID_trabajo`),
  ADD KEY `idx_usuario` (`ID_usuario`),
  ADD KEY `idx_fecha` (`fecha`);

-- Índices de la tabla `calificaciones`
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`ID_calificacion`),
  ADD KEY `ID_alumno` (`ID_alumno`);

-- Índices de la tabla `comentarios_calificaciones`
ALTER TABLE `comentarios_calificaciones`
  ADD PRIMARY KEY (`ID_comentario`),
  ADD KEY `idx_calificacion` (`ID_calificacion`),
  ADD KEY `idx_usuario` (`ID_usuario`),
  ADD KEY `idx_fecha` (`fecha`);

--
-- AUTO_INCREMENT de las tablas
--

ALTER TABLE `usuarios`
  MODIFY `ID_usuario` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `alumnos`
  MODIFY `ID_alumno` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `profesores`
  MODIFY `ID_profesor` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `profesor_alumno`
  MODIFY `ID_relacion` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `solicitudes_profesor`
  MODIFY `ID_solicitud` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `trabajos`
  MODIFY `ID_trabajo` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `comentarios`
  MODIFY `ID_comentario` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `calificaciones`
  MODIFY `ID_calificacion` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `comentarios_calificaciones`
  MODIFY `ID_comentario` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones (FOREIGN KEYS)
--

-- Restricciones para `alumnos`
ALTER TABLE `alumnos`
  ADD CONSTRAINT `alumnos_ibfk_1` FOREIGN KEY (`ID_usuario`) REFERENCES `usuarios` (`ID_usuario`) ON DELETE CASCADE;

-- Restricciones para `profesores`
ALTER TABLE `profesores`
  ADD CONSTRAINT `profesores_ibfk_1` FOREIGN KEY (`ID_usuario`) REFERENCES `usuarios` (`ID_usuario`) ON DELETE CASCADE;

-- Restricciones para `profesor_alumno`
ALTER TABLE `profesor_alumno`
  ADD CONSTRAINT `profesor_alumno_ibfk_1` FOREIGN KEY (`ID_profesor`) REFERENCES `profesores` (`ID_profesor`) ON DELETE CASCADE,
  ADD CONSTRAINT `profesor_alumno_ibfk_2` FOREIGN KEY (`ID_alumno`) REFERENCES `alumnos` (`ID_alumno`) ON DELETE CASCADE;

-- Restricciones para `solicitudes_profesor`
ALTER TABLE `solicitudes_profesor`
  ADD CONSTRAINT `solicitudes_profesor_ibfk_1` FOREIGN KEY (`ID_alumno`) REFERENCES `alumnos` (`ID_alumno`) ON DELETE CASCADE,
  ADD CONSTRAINT `solicitudes_profesor_ibfk_2` FOREIGN KEY (`ID_profesor`) REFERENCES `profesores` (`ID_profesor`) ON DELETE CASCADE;

-- Restricciones para `trabajos`
ALTER TABLE `trabajos`
  ADD CONSTRAINT `trabajos_ibfk_1` FOREIGN KEY (`ID_alumno`) REFERENCES `alumnos` (`ID_alumno`) ON DELETE CASCADE;

-- Restricciones para `comentarios`
ALTER TABLE `comentarios`
  ADD CONSTRAINT `comentarios_ibfk_1` FOREIGN KEY (`ID_trabajo`) REFERENCES `trabajos` (`ID_trabajo`) ON DELETE CASCADE,
  ADD CONSTRAINT `comentarios_ibfk_2` FOREIGN KEY (`ID_usuario`) REFERENCES `usuarios` (`ID_usuario`) ON DELETE CASCADE;

-- Restricciones para `calificaciones`
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`ID_alumno`) REFERENCES `alumnos` (`ID_alumno`) ON DELETE CASCADE;

-- Restricciones para `comentarios_calificaciones`
ALTER TABLE `comentarios_calificaciones`
  ADD CONSTRAINT `comentarios_calificaciones_ibfk_1` FOREIGN KEY (`ID_calificacion`) REFERENCES `calificaciones` (`ID_calificacion`) ON DELETE CASCADE,
  ADD CONSTRAINT `comentarios_calificaciones_ibfk_2` FOREIGN KEY (`ID_usuario`) REFERENCES `usuarios` (`ID_usuario`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
