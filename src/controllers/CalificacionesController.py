from models.CalificacionesModel import CalificacionesModel

class CalificacionesController:
    def __init__(self):
        self.model = CalificacionesModel()

    def obtener_por_alumno(self, id_alumno):
        return self.model.obtener_por_alumno(id_alumno)

    def guardar(self, id_alumno, materia, unidad1, unidad2, unidad3):
        if not materia:
            return False, "La materia es obligatoria"
        
        if self.model.crear_o_actualizar(id_alumno, materia, unidad1, unidad2, unidad3):
            return True, "Calificaciones guardadas exitosamente"
        return False, "Error al guardar calificaciones"