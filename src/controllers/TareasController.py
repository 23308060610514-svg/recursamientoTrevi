from models.TareasModel import TareasModel

class TareasController:
    def __init__(self):
        self.model = TareasModel()

    def obtener_por_alumno(self, id_alumno):
        """Obtiene todas las tareas de un alumno"""
        return self.model.obtener_por_alumno(id_alumno)

    def crear(self, id_alumno, materia, titulo, descripcion, fecha_entrega):
        """Crea una nueva tarea"""
        if not materia or not titulo:
            return False, "Materia y título son obligatorios"
        
        if self.model.crear(id_alumno, materia, titulo, descripcion, fecha_entrega):
            return True, "Tarea creada exitosamente"
        return False, "Error al crear tarea"

    def actualizar(self, id_trabajo, materia, titulo, descripcion, fecha_entrega):
        """Actualiza una tarea existente"""
        if self.model.actualizar(id_trabajo, materia, titulo, descripcion, fecha_entrega):
            return True, "Tarea actualizada exitosamente"
        return False, "Error al actualizar tarea"

    def calificar(self, id_trabajo, calificacion):
        """Asigna una calificación a una tarea"""
        if calificacion < 0 or calificacion > 100:
            return False, "La calificación debe estar entre 0 y 100"
        
        if self.model.actualizar_calificacion(id_trabajo, calificacion):
            return True, "Calificación actualizada"
        return False, "Error al calificar"

    def eliminar(self, id_trabajo):
        """Elimina una tarea"""
        if self.model.eliminar(id_trabajo):
            return True, "Tarea eliminada"
        return False, "Error al eliminar tarea"