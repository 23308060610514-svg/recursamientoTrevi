from .databaseModel import Database

class CalificacionesModel:
    def __init__(self):
        self.db = Database()

    def obtener_por_alumno(self, id_alumno):
        """Obtiene calificaciones de un alumno"""
        connection = self.db.get_connection()
        if not connection:
            return []
        
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID_calificacion, Materia, Unidad1, Unidad2, Unidad3, Promedio
                FROM calificaciones
                WHERE ID_alumno = %s
            """, (id_alumno,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en obtener_por_alumno: {e}")
            return []
        finally:
            connection.close()

    def crear_o_actualizar(self, id_alumno, materia, unidad1, unidad2, unidad3):
        """Crea o actualiza calificaciones de un alumno"""
        connection = self.db.get_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT ID_calificacion FROM calificaciones 
                WHERE ID_alumno = %s AND Materia = %s
            """, (id_alumno, materia))
            existe = cursor.fetchone()
            if existe:
                cursor.execute("""
                    UPDATE calificaciones 
                    SET Unidad1 = %s, Unidad2 = %s, Unidad3 = %s
                    WHERE ID_alumno = %s AND Materia = %s
                """, (unidad1, unidad2, unidad3, id_alumno, materia))
            else:
                cursor.execute("""
                    INSERT INTO calificaciones (ID_alumno, Materia, Unidad1, Unidad2, Unidad3)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_alumno, materia, unidad1, unidad2, unidad3))
            
            connection.commit()
            return True
        except Exception as e:
            print(f"Error en crear_o_actualizar: {e}")
            return False
        finally:
            connection.close()