from models.ProfesoresModel import ProfesoresModel
from models.UsuariosModel import UsuariosModel
from models.schemasModel import UsuarioSchema

class ProfesoresController:
    def __init__(self):
        self.model = ProfesoresModel()
        self.usuario_model = UsuariosModel()

    def listar(self):
        """Lista todos los profesores"""
        return self.model.obtener_todos()

    def obtener(self, id_profesor):
        """Obtiene un profesor por ID"""
        return self.model.obtener_por_id(id_profesor)

    def crear(self, nombre, apellido, email, password, especialidad, id_usuario):
        """Crea un nuevo profesor con su usuario asociado"""
        try:
            if self.usuario_model.email_existe(email):
                return False, "El correo electrónico ya está registrado"
            usuario_data = UsuarioSchema(nombre=nombre, email=email, password=password)
            if not self.usuario_model.registrar(usuario_data):
                return False, "Error al crear el usuario"
            usuario = self.usuario_model.obtener_por_email(email)
            if not usuario:
                return False, "Error al obtener el usuario creado"
            if self.model.crear(nombre, apellido, email, password, especialidad, usuario['ID_usuario']):
                return True, "Profesor creado exitosamente"
            return False, "Error al crear el profesor"
            
        except Exception as e:
            return False, f"Error al crear profesor: {str(e)}"

    def actualizar(self, id_profesor, nombre, apellido, email, especialidad):
        """Actualiza un profesor"""
        if self.model.actualizar(id_profesor, nombre, apellido, email, especialidad):
            return True, "Profesor actualizado exitosamente"
        return False, "Error al actualizar profesor"

    def eliminar(self, id_profesor):
        """Elimina un profesor (y su usuario asociado por CASCADE)"""
        if self.model.eliminar(id_profesor):
            return True, "Profesor eliminado exitosamente"
        return False, "Error al eliminar profesor"