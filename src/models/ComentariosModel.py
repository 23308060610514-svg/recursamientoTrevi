from .databaseModel import Database
from datetime import datetime

class ComentariosModel:
    def __init__(self):
        self.db = Database()

    def crear(self, id_trabajo, id_usuario, comentario):
        """Crea un nuevo comentario para una tarea"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión a la base de datos"
        
        try:
            cursor = connection.cursor()
            fecha_actual = datetime.now()
            
            cursor.execute("""
                INSERT INTO comentarios (ID_trabajo, ID_usuario, comentario, fecha)
                VALUES (%s, %s, %s, %s)
            """, (id_trabajo, id_usuario, comentario, fecha_actual))
            connection.commit()
            return True, "Comentario agregado exitosamente"
        except Exception as e:
            print(f"Error en crear comentario: {e}")
            return False, f"Error al crear comentario: {str(e)}"
        finally:
            connection.close()

    def crear_comentario_calificacion(self, id_calificacion, id_usuario, comentario):
        """Crea un nuevo comentario para una calificación"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión a la base de datos"
        
        try:
            cursor = connection.cursor()
            fecha_actual = datetime.now()
            
            cursor.execute("""
                INSERT INTO comentarios_calificaciones (ID_calificacion, ID_usuario, comentario, fecha)
                VALUES (%s, %s, %s, %s)
            """, (id_calificacion, id_usuario, comentario, fecha_actual))
            connection.commit()
            return True, "Comentario agregado exitosamente"
        except Exception as e:
            print(f"Error en crear comentario calificacion: {e}")
            return False, f"Error al crear comentario: {str(e)}"
        finally:
            connection.close()

    def obtener_por_trabajo(self, id_trabajo):
        """Obtiene todos los comentarios de un trabajo"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.ID_comentario, c.comentario, 
                    DATE_FORMAT(c.fecha, '%d/%m/%Y %H:%i') as fecha,
                    u.user as usuario
                FROM comentarios c
                JOIN usuarios u ON c.ID_usuario = u.ID_usuario
                WHERE c.ID_trabajo = %s
                ORDER BY c.fecha ASC
            """, (id_trabajo,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_por_trabajo: {e}")
            return []
        finally:
            connection.close()

    def obtener_por_calificacion(self, id_calificacion):
        """Obtiene todos los comentarios de una calificación"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.ID_comentario, c.comentario, 
                    DATE_FORMAT(c.fecha, '%d/%m/%Y %H:%i') as fecha,
                    u.user as usuario
                FROM comentarios_calificaciones c
                JOIN usuarios u ON c.ID_usuario = u.ID_usuario
                WHERE c.ID_calificacion = %s
                ORDER BY c.fecha ASC
            """, (id_calificacion,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_por_calificacion: {e}")
            return []
        finally:
            connection.close()

    def eliminar(self, id_comentario, id_usuario):
        """Elimina un comentario (solo el autor puede eliminar)"""
        connection = self.db.get_connection()
        if not connection:
            return False, "Error de conexión a la base de datos"
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM comentarios 
                WHERE ID_comentario = %s AND ID_usuario = %s
            """, (id_comentario, id_usuario))
            connection.commit()
            
            if cursor.rowcount > 0:
                return True, "Comentario eliminado"
            return False, "No tienes permiso para eliminar este comentario"
        except Exception as e:
            print(f"Error en eliminar comentario: {e}")
            return False, f"Error al eliminar comentario: {str(e)}"
        finally:
            connection.close()