from .databaseModel import Database

class AlumnosModel:
    def __init__(self):
        self.db = Database()

    def obtener_todos(self):
        """Obtiene todos los alumnos"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.ID_alumno, a.nombre, a.apellido, a.no_control, 
                    u.user as nombre_usuario, u.Email
                FROM alumnos a
                JOIN usuarios u ON a.ID_usuario = u.ID_usuario
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_todos: {e}")
            return []
        finally:
            connection.close()

    def obtener_por_id(self, id_alumno):
        """Obtiene un alumno por ID"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT a.ID_alumno, a.nombre, a.apellido, a.no_control, a.ID_usuario,
                    u.user as nombre_usuario, u.Email
                FROM alumnos a
                JOIN usuarios u ON a.ID_usuario = u.ID_usuario
                WHERE a.ID_alumno = %s
            """, (id_alumno,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en obtener_por_id: {e}")
            return None
        finally:
            connection.close()

    def obtener_por_usuario(self, id_usuario):
        """Obtiene un alumno por ID de usuario"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID_alumno, nombre, apellido, no_control
                FROM alumnos
                WHERE ID_usuario = %s
            """, (id_usuario,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error en obtener_por_usuario: {e}")
            return None
        finally:
            connection.close()

    def crear(self, nombre, apellido, no_control, id_usuario):
        """Crea un nuevo alumno"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO alumnos (nombre, apellido, no_control, ID_usuario)
                VALUES (%s, %s, %s, %s)
            """, (nombre, apellido, no_control, id_usuario))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en crear: {e}")
            return False
        finally:
            connection.close()

    def actualizar(self, id_alumno, nombre, apellido, no_control):
        """Actualiza un alumno"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE alumnos 
                SET nombre = %s, apellido = %s, no_control = %s
                WHERE ID_alumno = %s
            """, (nombre, apellido, no_control, id_alumno))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en actualizar: {e}")
            return False
        finally:
            connection.close()

    def eliminar(self, id_alumno):
        """Elimina un alumno"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM alumnos WHERE ID_alumno = %s", (id_alumno,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en eliminar: {e}")
            return False
        finally:
            connection.close()