import bcrypt
from .DataBaseModel import Database

class ModelsUsuarios:
    def __init__(self):
        self.db = Database()
    
    def email_existe(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_usuario FROM usuarios WHERE Email = %s", (email,))
        existe = cursor.fetchone() is not None
        conn.close()
        return existe
        
    def registrar(self, usuario_data):
        print(f"📝 Registrando: {usuario_data.email}")
        print(f"   Contraseña: '{usuario_data.password}'")
        
        
        password_bytes = usuario_data.password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        hashed_str = hashed.decode('utf-8')
        
        print(f"   Hash generado: {hashed_str[:50]}...")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO usuarios (User, Email, Password, Fecha_Registro) 
                VALUES (%s, %s, %s, CURDATE())""",
                (usuario_data.nombre, usuario_data.email, hashed_str)
            )
            conn.commit()
            print("   ✅ Usuario registrado")
            return True
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
        finally:
            conn.close()
        
    def validar_login(self, email, password):
        print(f"\n🔐 Login: {email}")
        print(f"   Contraseña: '{password}'")
        
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE Email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            print("   ❌ Usuario no existe")
            return None
        
        print(f"   Usuario: {user['User']}")
        print(f"   Hash BD: {user['Password'][:50]}...")
        
        
        try:
            if bcrypt.checkpw(password.encode('utf-8'), user['Password'].encode('utf-8')):
                print("   ✅ LOGIN EXITOSO")
                return user
            else:
                print("   ❌ Contraseña incorrecta")
                return None
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None
    
    def obtener_por_id(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID_usuario, User as nombre, Email as email FROM usuarios WHERE ID_usuario = %s", (id_usuario,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def obtener_por_email(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ID_usuario, User, Email FROM usuarios WHERE Email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    def actualizar_password(self, id_usuario, nueva_password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET Password = %s WHERE ID_usuario = %s",
                (nueva_password, id_usuario)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar password: {e}")
            return False
        finally:
            conn.close()