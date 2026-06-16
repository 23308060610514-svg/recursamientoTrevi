from models.UsuariosModel import UsuariosModel
from models.schemasModel import UsuarioSchema
import bcrypt

class AuthController:
    def __init__(self):
        self.usuario_model = UsuariosModel()

    def login(self, email, password):
        try:
            user_db = self.usuario_model.validar_login(email, password)
            if not user_db:
                return None, "Correo o contraseña incorrectos"
            
            tipo_usuario = self.usuario_model.obtener_tipo_usuario(user_db["ID_usuario"])
            user = {
                "ID_usuario": user_db["ID_usuario"],
                "user": user_db["user"],
                "nombre": user_db["user"],
                "Email": user_db["Email"],
                "tipo": tipo_usuario
            }

            return user, "Login exitoso"

        except Exception as e:
            print(f"Error en login: {e}")
            return None, f"Error en login: {str(e)}"

    def registrar(self, usuario_data):
        try:
            if self.usuario_model.email_existe(usuario_data.email):
                return False, "El correo electrónico ya está registrado"

            exito = self.usuario_model.registrar(usuario_data)

            if exito:
                return True, "Usuario registrado exitosamente"
            else:
                return False, "Error al registrar usuario"

        except Exception as e:
            return False, f"Error en registro: {str(e)}"

    def registrar_alumno_completo(self, nombre, apellido, no_control, email, password):
        try:
            if self.usuario_model.email_existe(email):
                return False, "El correo electrónico ya está registrado"
            
            from models.schemasModel import UsuarioSchema
            usuario_data = UsuarioSchema(nombre=nombre, apellido=apellido, email=email, password=password)
            
            exito = self.usuario_model.registrar(usuario_data)
            if not exito:
                return False, "Error al registrar usuario"
            
            usuario = self.usuario_model.obtener_por_email(email)
            if not usuario:
                return False, "Error al obtener usuario creado"
            
            from models.AlumnosModel import AlumnosModel
            alumno_model = AlumnosModel()
            exito_alumno = alumno_model.crear(nombre, apellido, no_control, usuario["ID_usuario"])
            
            if exito_alumno:
                return True, "Alumno registrado exitosamente"
            else:
                return False, "Error al registrar alumno"
                
        except Exception as e:
            return False, f"Error en registro completo: {str(e)}"

    def registrar_profesor_completo(self, nombre, apellido, email, password):
        try:
            if self.usuario_model.email_existe(email):
                return False, "El correo electrónico ya está registrado"
            
            from models.schemasModel import UsuarioSchema
            usuario_data = UsuarioSchema(nombre=nombre, apellido=apellido, email=email, password=password)
            
            exito = self.usuario_model.registrar(usuario_data)
            if not exito:
                return False, "Error al registrar usuario"
            
            usuario = self.usuario_model.obtener_por_email(email)
            if not usuario:
                return False, "Error al obtener usuario creado"
            
            from models.ProfesoresModel import ProfesoresModel
            profesor_model = ProfesoresModel()
            exito_profesor = profesor_model.crear_completo(nombre, apellido, email, password, usuario["ID_usuario"])
            
            if exito_profesor:
                return True, "Profesor registrado exitosamente"
            else:
                return False, "Error al registrar profesor"
                
        except Exception as e:
            return False, f"Error en registro completo: {str(e)}"

    def obtener_usuario_por_id(self, id_usuario: int) -> dict:
        try:
            usuario = self.usuario_model.obtener_por_id(id_usuario)
            if usuario:
                return {"success": True, "usuario": usuario}
            return {"success": False, "message": "Usuario no encontrado"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def cambiar_password(self, id_usuario: int, password_actual: str, nueva_password: str) -> dict:
        try:
            usuario = self.usuario_model.obtener_por_id(id_usuario)
            if not usuario:
                return {"success": False, "message": "Usuario no encontrado"}
            
            user_db = self.usuario_model.validar_login(usuario["Email"], password_actual)
            
            if not user_db:
                return {"success": False, "message": "Contraseña actual incorrecta"}
            
            if len(nueva_password) < 6:
                return {"success": False, "message": "La nueva contraseña debe tener al menos 6 caracteres"}
            
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(nueva_password.encode('utf-8'), salt)
            hashed_str = hashed.decode('utf-8')
            
            exito = self.usuario_model.actualizar_password(id_usuario, hashed_str)
            
            if exito:
                return {"success": True, "message": "Contraseña actualizada correctamente"}
            return {"success": False, "message": "Error al actualizar la contraseña"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}