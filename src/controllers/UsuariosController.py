from models.ModelsUsuarios import ModelsUsuarios
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcrypt
import time
import hashlib

class AuthController:
    def __init__(self):
        self.usuario_model = ModelsUsuarios()
        self.tokens_activos = {}  

    def login(self, email, password):
        try:
            user_db = self.usuario_model.validar_login(email, password)

            if not user_db:
                return None, "Correo o contraseña incorrectos"

            user = {
                "id_usuario": user_db["ID_usuario"],
                "nombre": user_db["User"],
                "email": user_db["Email"],
            }

            return user, "Login exitoso"

        except Exception as e:
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

    def enviar_correo_recuperacion(self, email, token, username):
        """Envía correo real de recuperación"""
        try:
            
            EMAIL_USER = "delrioerik@gmail.com"
            EMAIL_PASSWORD = "i2314173101ermi"

            mensaje = MIMEMultipart("alternative")
            mensaje["Subject"] = "REmenus - Recuperación de Contraseña"
            mensaje["From"] = f"REmenus <{EMAIL_USER}>"
            mensaje["To"] = email

            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                    <h2 style="color: #1565C0;">🔐 REMenus - Recupera tu Contraseña</h2>
                    <hr style="border-color: #1565C0;">
                    <p>Hola <strong>{username}</strong>,</p>
                    <p>Hemos recibido una solicitud para restablecer tu contraseña.</p>
                    <p><strong>Tu código de verificación es:</strong></p>
                    <div style="background: #f0f0f0; padding: 15px; text-align: center; font-family: monospace; font-size: 24px; letter-spacing: 2px; border-radius: 8px;">
                        <strong>{token}</strong>
                    </div>
                    <p style="margin-top: 20px;">Este código expirará en <strong>30 minutos</strong>.</p>
                    <p>Si no solicitaste este cambio, ignora este mensaje.</p>
                    <hr>
                    <p style="font-size: 12px; color: #666;">REmenus - Sistema de Menús Digitales</p>
                </div>
            </body>
            </html>
            """

            mensaje.attach(MIMEText(html, "html"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.sendmail(EMAIL_USER, email, mensaje.as_string())

            print(f"✅ Correo enviado a {email}")
            return True
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")
            return False

    def solicitar_recuperacion(self, email: str) -> dict:
        try:
            usuario = self.usuario_model.obtener_por_email(email)

            if not usuario:
                return {
                    "success": False,
                    "message": "No existe una cuenta con este correo electrónico"
                }

            
            token_data = f"{usuario['ID_usuario']}{email}{time.time()}"
            token = hashlib.md5(token_data.encode()).hexdigest()

        
            self.tokens_activos[token] = {
                "user_id": usuario['ID_usuario'],
                "email": email,
                "expira": time.time() + 1800  
            }

            envio = self.enviar_correo_recuperacion(email, token, usuario['User'])

            if envio:
                return {
                    "success": True,
                    "message": f"Se ha enviado un código de verificación a {email}"
                }
            else:
                return {
                    "success": False,
                    "message": "Error al enviar el correo. Verifica tu conexión"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error al procesar la solicitud: {str(e)}"
            }

    def restablecer_contraseña(self, token: str, nueva_password: str) -> dict:
        try:
            if token not in self.tokens_activos:
                return {
                    "success": False,
                    "message": "Código inválido o expirado"
                }

            token_info = self.tokens_activos[token]

            if time.time() > token_info["expira"]:
                del self.tokens_activos[token]
                return {
                    "success": False,
                    "message": "El código ha expirado. Solicita uno nuevo"
                }

            
            if len(nueva_password) < 6:
                return {
                    "success": False,
                    "message": "La contraseña debe tener al menos 6 caracteres"
                }

            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(nueva_password.encode('utf-8'), salt)
            hashed_str = hashed.decode('utf-8')

            
            exito = self.usuario_model.actualizar_password(token_info["user_id"], hashed_str)

            
            del self.tokens_activos[token]

            if exito:
                return {
                    "success": True,
                    "message": "Contraseña actualizada correctamente. Ahora puedes iniciar sesión."
                }
            else:
                return {
                    "success": False,
                    "message": "Error al actualizar la contraseña"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error al procesar la solicitud: {str(e)}"
            }

    
    def reset_password(self, token: str, nueva_password: str) -> tuple:
        """
        Método de compatibilidad para otras vistas que esperan una tupla (bool, str)
        """
        resultado = self.restablecer_contraseña(token, nueva_password)
        return resultado.get("success", False), resultado.get("message", "")

    def obtener_usuario_por_id(self, id_usuario: int) -> dict:
        """Obtiene información de un usuario por su ID"""
        try:
            usuario = self.usuario_model.obtener_por_id(id_usuario)
            if usuario:
                return {"success": True, "usuario": usuario}
            return {"success": False, "message": "Usuario no encontrado"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def cambiar_password(self, id_usuario: int, password_actual: str, nueva_password: str) -> dict:
        """Cambia la contraseña de un usuario verificando la actual"""
        try:
            
            user = self.usuario_model.validar_login(
                self.usuario_model.obtener_por_id(id_usuario)["email"],
                password_actual
            )
            
            if not user:
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