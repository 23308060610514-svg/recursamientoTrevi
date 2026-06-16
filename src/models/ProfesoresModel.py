from .databaseModel import Database
import bcrypt
from datetime import date, datetime

class ProfesoresModel:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        """Obtiene todos los profesores"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.ID_profesor, p.nombre, p.apellido, p.Email, p.especialidad,
                    u.user as nombre_usuario
                FROM profesores p
                JOIN usuarios u ON p.ID_usuario = u.ID_usuario
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_todos: {e}")
            return []
        finally:
            connection.close()

    def obtener_por_id(self, id_profesor):
        """Obtiene un profesor por ID"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.ID_profesor, p.nombre, p.apellido, p.Email, p.especialidad,
                    u.user as nombre_usuario, u.ID_usuario
                FROM profesores p
                JOIN usuarios u ON p.ID_usuario = u.ID_usuario
                WHERE p.ID_profesor = %s
            """, (id_profesor,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en obtener_por_id: {e}")
            return None
        finally:
            connection.close()

    def obtener_por_usuario(self, id_usuario):
        """Obtiene un profesor por ID de usuario"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID_profesor, nombre, apellido, Email, especialidad
                FROM profesores
                WHERE ID_usuario = %s
            """, (id_usuario,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en obtener_por_usuario: {e}")
            return None
        finally:
            connection.close()

    def crear(self, nombre, apellido, email, password, especialidad, id_usuario):
        """Crea un nuevo profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            fecha_actual = date.today()
            
            cursor.execute("""
                INSERT INTO profesores (nombre, apellido, Email, Password, especialidad, Fecha_Registro, ID_usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, email, hashed.decode('utf-8'), especialidad, fecha_actual, id_usuario))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en crear: {e}")
            return False
        finally:
            connection.close()

    def crear_completo(self, nombre, apellido, email, password, id_usuario):
        """Crea un nuevo profesor con contraseña ya hasheada"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            fecha_actual = date.today()
            
            cursor.execute("""
                INSERT INTO profesores (nombre, apellido, Email, Password, especialidad, Fecha_Registro, ID_usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombre, apellido, email, hashed.decode('utf-8'), None, fecha_actual, id_usuario))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en crear_completo: {e}")
            return False
        finally:
            connection.close()

    def actualizar(self, id_profesor, nombre, apellido, email, especialidad):
        """Actualiza un profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE profesores 
                SET nombre = %s, apellido = %s, Email = %s, especialidad = %s
                WHERE ID_profesor = %s
            """, (nombre, apellido, email, especialidad, id_profesor))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en actualizar: {e}")
            return False
        finally:
            connection.close()

    def eliminar(self, id_profesor):
        """Elimina un profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM profesores WHERE ID_profesor = %s", (id_profesor,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en eliminar: {e}")
            return False
        finally:
            connection.close()

    # Métodos para gestión de alumnos
    def obtener_alumnos_asignados(self, id_profesor):
        """Obtiene los alumnos asignados a un profesor"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.ID_alumno, a.nombre, a.apellido, a.no_control,
                    pa.fecha_asignacion, pa.estado
                FROM profesor_alumno pa
                JOIN alumnos a ON pa.ID_alumno = a.ID_alumno
                WHERE pa.ID_profesor = %s AND pa.estado = 'activo'
                ORDER BY a.apellido, a.nombre
            """, (id_profesor,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_alumnos_asignados: {e}")
            return []
        finally:
            connection.close()

    def obtener_alumnos_disponibles(self, id_profesor):
        """Obtiene alumnos que no están asignados a este profesor"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.ID_alumno, a.nombre, a.apellido, a.no_control
                FROM alumnos a
                WHERE a.ID_alumno NOT IN (
                    SELECT ID_alumno FROM profesor_alumno 
                    WHERE ID_profesor = %s AND estado = 'activo'
                )
                ORDER BY a.apellido, a.nombre
            """, (id_profesor,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_alumnos_disponibles: {e}")
            return []
        finally:
            connection.close()

    def asignar_alumno(self, id_profesor, id_alumno):
        """Asigna un alumno a un profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión"
        
        try:
            cursor = connection.cursor()
            fecha_actual = datetime.now()
            
            # Verificar si ya existe la relación
            cursor.execute("""
                SELECT ID_relacion FROM profesor_alumno 
                WHERE ID_profesor = %s AND ID_alumno = %s
            """, (id_profesor, id_alumno))
            
            if cursor.fetchone():
                # Actualizar a activo si existe
                cursor.execute("""
                    UPDATE profesor_alumno 
                    SET estado = 'activo', fecha_asignacion = %s
                    WHERE ID_profesor = %s AND ID_alumno = %s
                """, (fecha_actual, id_profesor, id_alumno))
            else:
                # Crear nueva relación
                cursor.execute("""
                    INSERT INTO profesor_alumno (ID_profesor, ID_alumno, fecha_asignacion, estado)
                    VALUES (%s, %s, %s, 'activo')
                """, (id_profesor, id_alumno, fecha_actual))
            
            connection.commit()
            return True, "Alumno asignado exitosamente"
        except Exception as e:
            print(f"Error en asignar_alumno: {e}")
            return False, f"Error al asignar alumno: {str(e)}"
        finally:
            connection.close()

    def desasignar_alumno(self, id_profesor, id_alumno):
        """Desasigna un alumno de un profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión"
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE profesor_alumno 
                SET estado = 'inactivo'
                WHERE ID_profesor = %s AND ID_alumno = %s
            """, (id_profesor, id_alumno))
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, "Alumno desasignado exitosamente"
            return False, "No se encontró la relación"
        except Exception as e:
            print(f"Error en desasignar_alumno: {e}")
            return False, f"Error al desasignar alumno: {str(e)}"
        finally:
            connection.close()

    # Métodos para solicitudes
    def crear_solicitud(self, id_alumno, id_profesor, mensaje=None):
        """Crea una solicitud de alumno a profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión"
        
        try:
            cursor = connection.cursor()
            fecha_actual = datetime.now()
            
            # Verificar si ya existe solicitud pendiente
            cursor.execute("""
                SELECT ID_solicitud FROM solicitudes_profesor 
                WHERE ID_alumno = %s AND ID_profesor = %s AND estado = 'pendiente'
            """, (id_alumno, id_profesor))
            
            if cursor.fetchone():
                return False, "Ya tienes una solicitud pendiente para este profesor"
            
            cursor.execute("""
                INSERT INTO solicitudes_profesor (ID_alumno, ID_profesor, fecha_solicitud, estado, mensaje)
                VALUES (%s, %s, %s, 'pendiente', %s)
            """, (id_alumno, id_profesor, fecha_actual, mensaje))
            connection.commit()
            return True, "Solicitud enviada exitosamente"
        except Exception as e:
            print(f"Error en crear_solicitud: {e}")
            return False, f"Error al crear solicitud: {str(e)}"
        finally:
            connection.close()

    def obtener_solicitudes_recibidas(self, id_profesor):
        """Obtiene las solicitudes pendientes para un profesor"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.ID_solicitud, s.fecha_solicitud, s.mensaje, s.estado,
                    a.ID_alumno, a.nombre, a.apellido, a.no_control
                FROM solicitudes_profesor s
                JOIN alumnos a ON s.ID_alumno = a.ID_alumno
                WHERE s.ID_profesor = %s AND s.estado = 'pendiente'
                ORDER BY s.fecha_solicitud DESC
            """, (id_profesor,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_solicitudes_recibidas: {e}")
            return []
        finally:
            connection.close()

    def obtener_solicitudes_enviadas(self, id_alumno):
        """Obtiene las solicitudes enviadas por un alumno"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.ID_solicitud, s.fecha_solicitud, s.mensaje, s.estado,
                    p.ID_profesor, p.nombre, p.apellido, p.Email
                FROM solicitudes_profesor s
                JOIN profesores p ON s.ID_profesor = p.ID_profesor
                WHERE s.ID_alumno = %s
                ORDER BY s.fecha_solicitud DESC
            """, (id_alumno,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_solicitudes_enviadas: {e}")
            return []
        finally:
            connection.close()

    def responder_solicitud(self, id_solicitud, aceptar):
        """Acepta o rechaza una solicitud"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión"
        
        try:
            cursor = connection.cursor(dictionary=True)
            
            # Obtener la solicitud
            cursor.execute("""
                SELECT ID_alumno, ID_profesor FROM solicitudes_profesor
                WHERE ID_solicitud = %s AND estado = 'pendiente'
            """, (id_solicitud,))
            solicitud = cursor.fetchone()
            
            if not solicitud:
                return False, "Solicitud no encontrada o ya procesada"
            
            nuevo_estado = 'aceptada' if aceptar else 'rechazada'
            
            # Actualizar estado de la solicitud
            cursor.execute("""
                UPDATE solicitudes_profesor 
                SET estado = %s
                WHERE ID_solicitud = %s
            """, (nuevo_estado, id_solicitud))
            
            # Si se acepta, asignar el alumno al profesor
            if aceptar:
                fecha_actual = datetime.now()
                # Verificar si ya existe la relación
                cursor.execute("""
                    SELECT ID_relacion FROM profesor_alumno 
                    WHERE ID_profesor = %s AND ID_alumno = %s
                """, (solicitud['ID_profesor'], solicitud['ID_alumno']))
                
                if cursor.fetchone():
                    cursor.execute("""
                        UPDATE profesor_alumno 
                        SET estado = 'activo', fecha_asignacion = %s
                        WHERE ID_profesor = %s AND ID_alumno = %s
                    """, (fecha_actual, solicitud['ID_profesor'], solicitud['ID_alumno']))
                else:
                    cursor.execute("""
                        INSERT INTO profesor_alumno (ID_profesor, ID_alumno, fecha_asignacion, estado)
                        VALUES (%s, %s, %s, 'activo')
                    """, (solicitud['ID_profesor'], solicitud['ID_alumno'], fecha_actual))
            
            connection.commit()
            mensaje = "Solicitud aceptada" if aceptar else "Solicitud rechazada"
            return True, mensaje
        except Exception as e:
            print(f"Error en responder_solicitud: {e}")
            return False, f"Error al procesar solicitud: {str(e)}"
        finally:
            connection.close()