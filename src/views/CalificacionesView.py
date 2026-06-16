import flet as ft
from models.AlumnosModel import AlumnosModel
from models.ComentariosModel import ComentariosModel

class CalificacionesView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.alumno_model = AlumnosModel()
        self.comentario_model = ComentariosModel()
        self.data_table = None
        self.dialog = None
        self.alumno_actual = None
        self.alumno_nombre = None
        self.dialog_comentarios = None

    def build(self):
        user = getattr(self.page, "user_data", None)
        es_profesor = user.get("tipo") == "profesor" if user else False
        
        alumnos = self.alumno_model.obtener_todos()
        
        alumnos_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        for a in alumnos:
            alumnos_list.controls.append(
                ft.ElevatedButton(
                    content=ft.Text(f"{a['nombre']} {a['apellido']} - {a['no_control']}"),
                    on_click=lambda e, alumno_id=a['ID_alumno'], nombre=f"{a['nombre']} {a['apellido']}": self.seleccionar_alumno(alumno_id, nombre),
                    width=400,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_50,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                )
            )
        
        self.txt_alumno_seleccionado = ft.Text("Ningún alumno seleccionado", size=14, color=ft.Colors.GREY_600)
        
        # Columnas de la tabla (6 columnas fijas)
        columnas = [
            ft.DataColumn(ft.Text("Materia", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Unidad 1", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Unidad 2", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Unidad 3", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Promedio", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Comentarios", weight=ft.FontWeight.BOLD)),
        ]
        
        self.data_table = ft.DataTable(
            columns=columnas,
            rows=[]
        )
        
        def agregar_calificacion(e):
            if not self.alumno_actual:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Selecciona un alumno primero"), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()
                return
            if not es_profesor:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden agregar calificaciones"), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.mostrar_formulario()
        
        def volver_dashboard(e):
            self.page.go("/dashboard")
        
        alumnos_scroll = ft.Container(
            content=alumnos_list,
            height=200,
        )
        
        tabla_scroll = ft.Container(
            content=self.data_table,
            height=400,
        )
        
        btn_agregar = ft.ElevatedButton(
            "➕ Agregar Calificación", 
            on_click=agregar_calificacion, 
            icon=ft.Icons.GRADE,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            visible=es_profesor,
        )
        
        return ft.View(
            route="/calificaciones",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gestión de Calificaciones", size=24),
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_dashboard),
                    actions=[
                        ft.IconButton(ft.Icons.REFRESH, on_click=lambda _: self.cargar_datos()),
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("📋 Seleccionar Alumno", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Container(height=10),
                                    alumnos_scroll,
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Row([
                                        ft.Text("👨‍🎓 Alumno seleccionado:", size=14, weight=ft.FontWeight.BOLD),
                                        self.txt_alumno_seleccionado,
                                    ]),
                                    ft.Divider(),
                                    ft.Row([
                                        btn_agregar,
                                    ], alignment=ft.MainAxisAlignment.END),
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Text("📊 Calificaciones por Materia", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    tabla_scroll,
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                    ], scroll=ft.ScrollMode.AUTO),
                    padding=20,
                    expand=True,
                )
            ]
        )
    
    def seleccionar_alumno(self, alumno_id, nombre):
        self.alumno_actual = alumno_id
        self.alumno_nombre = nombre
        self.txt_alumno_seleccionado.value = nombre
        self.txt_alumno_seleccionado.color = ft.Colors.GREEN_700
        self.cargar_datos()
        self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Alumno seleccionado: {nombre}"), bgcolor=ft.Colors.GREEN)
        self.page.snack_bar.open = True
        self.page.update()
    
    def cargar_datos(self):
        if not self.alumno_actual:
            self.data_table.rows = []
            self.page.update()
            return
        
        user = getattr(self.page, "user_data", None)
        es_profesor = user.get("tipo") == "profesor" if user else False
        id_usuario = user.get("ID_usuario") if user else None
        
        calificaciones = self.controller.obtener_por_alumno(self.alumno_actual)
        self.data_table.rows = []
        
        for cal in calificaciones:
            promedio = cal.get('Promedio', 0)
            if promedio:
                promedio = float(promedio)
            promedio_color = ft.Colors.GREEN if promedio >= 6 else ft.Colors.RED if promedio > 0 else ft.Colors.GREY
            
            # Obtener comentarios de la calificación
            comentarios = self.comentario_model.obtener_por_calificacion(cal['ID_calificacion'])
            num_comentarios = len(comentarios)
            comentario_texto = f"💬 {num_comentarios}" if num_comentarios > 0 else "Sin comentarios"
            
            # Crear las celdas base (6 columnas)
            celdas = [
                ft.DataCell(ft.Text(cal.get('Materia', ''))),
                ft.DataCell(ft.Text(str(cal.get('Unidad1', '-')) if cal.get('Unidad1') is not None else '-')),
                ft.DataCell(ft.Text(str(cal.get('Unidad2', '-')) if cal.get('Unidad2') is not None else '-')),
                ft.DataCell(ft.Text(str(cal.get('Unidad3', '-')) if cal.get('Unidad3') is not None else '-')),
                ft.DataCell(ft.Text(f"{promedio:.1f}" if promedio else "-", color=promedio_color)),
            ]
            
            # Sexta columna: Comentarios
            # Botón de comentarios visible para todos
            btn_comentarios = ft.IconButton(
                ft.Icons.COMMENT, 
                icon_color=ft.Colors.ORANGE,
                on_click=lambda e, c=cal: self.ver_comentarios_calificacion(c),
                tooltip="Ver comentarios"
            )
            
            # Si es profesor, también mostrar botón de editar
            if es_profesor:
                btn_editar = ft.IconButton(
                    ft.Icons.EDIT, 
                    icon_color=ft.Colors.BLUE, 
                    on_click=lambda e, c=cal: self.mostrar_formulario(c),
                    tooltip="Editar calificación"
                )
                celdas.append(ft.DataCell(ft.Row([btn_editar, btn_comentarios])))
            else:
                # Alumnos solo ven el botón de comentarios
                celdas.append(ft.DataCell(ft.Row([btn_comentarios])))
            
            self.data_table.rows.append(ft.DataRow(cells=celdas))
        self.page.update()
    
    def ver_comentarios_calificacion(self, calificacion):
        """Muestra los comentarios de una calificación y permite agregar nuevos"""
        user = getattr(self.page, "user_data", None)
        id_usuario = user.get("ID_usuario") if user else None
        nombre_usuario = user.get("user") or user.get("nombre") or "Usuario"
        
        comentarios = self.comentario_model.obtener_por_calificacion(calificacion['ID_calificacion'])
        
        # Crear lista de comentarios
        comentarios_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        if comentarios:
            for comentario in comentarios:
                comentarios_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(comentario.get('usuario', 'Usuario'), weight=ft.FontWeight.BOLD, size=12),
                                ft.Text("·", size=12),
                                ft.Text(comentario.get('fecha', ''), size=11, color=ft.Colors.GREY_600),
                            ]),
                            ft.Text(comentario.get('comentario', ''), size=13),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                    )
                )
        else:
            comentarios_list.controls.append(
                ft.Text("No hay comentarios aún", color=ft.Colors.GREY_600, size=14)
            )
        
        # Campo para nuevo comentario
        comentario_field = ft.TextField(
            label="Escribe tu comentario",
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=400,
            border_radius=10,
        )
        
        mensaje = ft.Text("", color=ft.Colors.RED, size=12)
        
        def guardar_comentario(e):
            if not comentario_field.value or not comentario_field.value.strip():
                mensaje.value = "El comentario no puede estar vacío"
                self.page.update()
                return
            
            success, msg = self.comentario_model.crear_comentario_calificacion(
                calificacion['ID_calificacion'],
                id_usuario,
                comentario_field.value.strip()
            )
            
            if success:
                self.dialog_comentarios.open = False
                self.cargar_datos()
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Comentario agregado"), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
            else:
                mensaje.value = msg
            self.page.update()
        
        def cancelar(e):
            self.dialog_comentarios.open = False
            self.page.update()
        
        # Botón de agregar comentario (visible para todos)
        btn_agregar = ft.ElevatedButton(
            "💬 Agregar Comentario",
            on_click=guardar_comentario,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        self.dialog_comentarios = ft.AlertDialog(
            title=ft.Text(f"Comentarios: {calificacion.get('Materia', '')}"),
            content=ft.Column([
                ft.Text(f"Alumno: {self.alumno_nombre}", size=14, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Comentarios:", size=14, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=comentarios_list,
                    height=200,
                ),
                ft.Divider(),
                comentario_field,
                mensaje,
            ], width=450, height=450, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cerrar", on_click=cancelar),
                btn_agregar,
            ],
        )
        self.page.overlay.append(self.dialog_comentarios)
        self.dialog_comentarios.open = True
        self.page.update()
    
    def mostrar_formulario(self, calificacion=None):
        user = getattr(self.page, "user_data", None)
        if user.get("tipo") != "profesor":
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden gestionar calificaciones"), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        materia_field = ft.TextField(label="Materia", value=calificacion.get('Materia') if calificacion else "", width=400, border_radius=10)
        unidad1_field = ft.TextField(label="Unidad 1", value=str(calificacion.get('Unidad1', '')) if calificacion and calificacion.get('Unidad1') else "", width=150, hint_text="0-100", border_radius=10)
        unidad2_field = ft.TextField(label="Unidad 2", value=str(calificacion.get('Unidad2', '')) if calificacion and calificacion.get('Unidad2') else "", width=150, hint_text="0-100", border_radius=10)
        unidad3_field = ft.TextField(label="Unidad 3", value=str(calificacion.get('Unidad3', '')) if calificacion and calificacion.get('Unidad3') else "", width=150, hint_text="0-100", border_radius=10)
        
        mensaje = ft.Text("", color=ft.Colors.RED, size=12)
        
        def guardar(e):
            if not materia_field.value:
                mensaje.value = "La materia es obligatoria"
                self.page.update()
                return
            
            def parse_calificacion(valor):
                try:
                    return float(valor) if valor and valor.strip() else None
                except ValueError:
                    return None
            
            unidad1 = parse_calificacion(unidad1_field.value)
            unidad2 = parse_calificacion(unidad2_field.value)
            unidad3 = parse_calificacion(unidad3_field.value)
            
            for unidad, nombre in [(unidad1, "Unidad 1"), (unidad2, "Unidad 2"), (unidad3, "Unidad 3")]:
                if unidad is not None and (unidad < 0 or unidad > 100):
                    mensaje.value = f"{nombre} debe estar entre 0 y 100"
                    self.page.update()
                    return
            
            success, msg = self.controller.guardar(
                self.alumno_actual,
                materia_field.value,
                unidad1,
                unidad2,
                unidad3
            )
            
            if success:
                self.dialog.open = False
                self.cargar_datos()
                self.page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
            else:
                mensaje.value = msg
            self.page.update()
        
        def cancelar(e):
            self.dialog.open = False
            self.page.update()
        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Agregar Calificación" if not calificacion else "Editar Calificación"),
            content=ft.Column([
                materia_field,
                ft.Row([unidad1_field, unidad2_field, unidad3_field], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                mensaje,
            ], width=450, height=250, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()