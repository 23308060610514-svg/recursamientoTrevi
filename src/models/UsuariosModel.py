import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import date
from .databaseModel import Database

class UsuariosModel:
    def __init__(self):
        self.db = Database()

    def validar_login(self, email, password):
        """Valida credenciales de usuario"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT ID_usuario, user, Email, Password FROM usuarios WHERE Email = %s", (email,))
            user = cursor.fetchone()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['Password'].encode('utf-8')):
                return user
            return None
        except Error as e:
            print(f"Error en validar_login: {e}")
            return None
        finally:
            connection.close()

    def email_existe(self, email):
        """Verifica si el email ya está registrado"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID_usuario FROM usuarios WHERE Email = %s", (email,))
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error en email_existe: {e}")
            return False
        finally:
            connection.close()

    def registrar(self, usuario_data):
        """Registra un nuevo usuario"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(usuario_data.password.encode('utf-8'), salt)
            
            fecha_actual = date.today()
            
            cursor.execute("""
                INSERT INTO usuarios (user, Email, Password, Fecha_Registro)
                VALUES (%s, %s, %s, %s)
            """, (usuario_data.nombre, usuario_data.email, hashed.decode('utf-8'), fecha_actual))
            
            connection.commit()
            return True
        except Error as e:
            print(f"Error en registrar: {e}")
            return False
        finally:
            connection.close()

    def obtener_por_email(self, email):
        """Obtiene usuario por email"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT ID_usuario, user, Email, Fecha_Registro FROM usuarios WHERE Email = %s", (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error en obtener_por_email: {e}")
            return None
        finally:
            connection.close()

    def obtener_por_id(self, id_usuario):
        """Obtiene usuario por ID"""
        connection = self.db.get_connection()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT ID_usuario, user, Email, Fecha_Registro FROM usuarios WHERE ID_usuario = %s", (id_usuario,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error en obtener_por_id: {e}")
            return None
        finally:
            connection.close()

    def actualizar_password(self, id_usuario, nueva_password_hash):
        """Actualiza la contraseña de un usuario"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE usuarios SET Password = %s WHERE ID_usuario = %s", (nueva_password_hash, id_usuario))
            connection.commit()
            return True
        except Error as e:
            print(f"Error en actualizar_password: {e}")
            return False
        finally:
            connection.close()
            
    def obtener_tipo_usuario(self, id_usuario):
        """Obtiene el tipo de usuario (alumno, profesor o admin)"""
        connection = self.db.get_connection()
        if not connection:
            return "usuario"
    
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID_alumno FROM alumnos WHERE ID_usuario = %s", (id_usuario,))
            if cursor.fetchone():
                return "alumno"
        
            cursor.execute("SELECT ID_profesor FROM profesores WHERE ID_usuario = %s", (id_usuario,))
            if cursor.fetchone():
                return "profesor"
        
            return "admin"
        except Exception as e:
            print(f"Error en obtener_tipo_usuario: {e}")
            return "usuario"
        finally:
            connection.close()

    def es_profesor(self, id_usuario):
        """Verifica si un usuario es profesor"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT ID_profesor FROM profesores WHERE ID_usuario = %s", (id_usuario,))
            return cursor.fetchone() is not None
        except Exception as e:
            print(f"Error en es_profesor: {e}")
            return False
        finally:
            connection.close()