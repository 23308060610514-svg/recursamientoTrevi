from models.AlumnosModel import AlumnosModel

class AlumnosController:
    def __init__(self):
        self.model = AlumnosModel()

    def listar(self):
        """Lista todos los alumnos"""
        try:
            return self.model.obtener_todos()
        except Exception as e:
            print(f"Error en listar: {e}")
            return []

    def obtener(self, id_alumno):
        """Obtiene un alumno por ID"""
        try:
            if not id_alumno:
                return None
            return self.model.obtener_por_id(id_alumno)
        except Exception as e:
            print(f"Error en obtener: {e}")
            return None

    def obtener_por_usuario(self, id_usuario):
        """Obtiene un alumno por ID de usuario"""
        try:
            if not id_usuario:
                return None
            return self.model.obtener_por_usuario(id_usuario)
        except Exception as e:
            print(f"Error en obtener_por_usuario: {e}")
            return None

    def crear(self, nombre, apellido, no_control, id_usuario):
        """Crea un nuevo alumno"""
        try:
            if self.model.crear(nombre, apellido, no_control, id_usuario):
                return True, "Alumno creado exitosamente"
            return False, "Error al crear alumno"
        except Exception as e:
            print(f"Error en crear: {e}")
            return False, f"Error al crear alumno: {str(e)}"

    def actualizar(self, id_alumno, nombre, apellido, no_control):
        """Actualiza un alumno"""
        try:
            if self.model.actualizar(id_alumno, nombre, apellido, no_control):
                return True, "Alumno actualizado exitosamente"
            return False, "Error al actualizar alumno"
        except Exception as e:
            print(f"Error en actualizar: {e}")
            return False, f"Error al actualizar alumno: {str(e)}"

    def eliminar(self, id_alumno):
        """Elimina un alumno"""
        try:
            if self.model.eliminar(id_alumno):
                return True, "Alumno eliminado exitosamente"
            return False, "Error al eliminar alumno"
        except Exception as e:
            print(f"Error en eliminar: {e}")
            return False, f"Error al eliminar alumno: {str(e)}"