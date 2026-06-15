from .databaseModel import Database
import bcrypt
from datetime import date

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