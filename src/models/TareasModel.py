from .databaseModel import Database

class TareasModel:
    def __init__(self):
        self.db = Database()

    def obtener_por_alumno(self, id_alumno):
        """Obtiene tareas de un alumno"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID_trabajo, Materia, titulo_trabajo, descripcion, fecha_entrega, calificacion
                FROM trabajos
                WHERE ID_alumno = %s
                ORDER BY fecha_entrega ASC
            """, (id_alumno,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_por_alumno: {e}")
            return []
        finally:
            connection.close()

    def crear(self, id_alumno, materia, titulo, descripcion, fecha_entrega):
        """Crea una nueva tarea"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO trabajos (ID_alumno, Materia, titulo_trabajo, descripcion, fecha_entrega)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_alumno, materia, titulo, descripcion, fecha_entrega))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en crear: {e}")
            return False
        finally:
            connection.close()

    def actualizar(self, id_trabajo, materia, titulo, descripcion, fecha_entrega):
        """Actualiza una tarea"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE trabajos 
                SET Materia = %s, titulo_trabajo = %s, descripcion = %s, fecha_entrega = %s
                WHERE ID_trabajo = %s
            """, (materia, titulo, descripcion, fecha_entrega, id_trabajo))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en actualizar: {e}")
            return False
        finally:
            connection.close()

    def actualizar_calificacion(self, id_trabajo, calificacion):
        """Actualiza la calificación de una tarea"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE trabajos SET calificacion = %s WHERE ID_trabajo = %s", (calificacion, id_trabajo))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en actualizar_calificacion: {e}")
            return False
        finally:
            connection.close()

    def eliminar(self, id_trabajo):
        """Elimina una tarea"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM trabajos WHERE ID_trabajo = %s", (id_trabajo,))
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en eliminar: {e}")
            return False
        finally:
            connection.close()