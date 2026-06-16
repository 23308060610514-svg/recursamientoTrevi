import flet as ft
from models.TareasModel import TareasModel
from models.AlumnosModel import AlumnosModel
from models.ComentariosModel import ComentariosModel

class TareasView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.alumno_model = AlumnosModel()
        self.comentario_model = ComentariosModel()
        self.data_table = None
        self.dialog = None
        self.alumno_actual = None
        self.alumno_nombre = None

    def build(self):
        user = getattr(self.page, "user_data", None)
        tipo_usuario = user.get("tipo") if user else "usuario"
        es_profesor = tipo_usuario == "profesor"
        
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
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Materia", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Título", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descripción", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Fecha Entrega", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Calificación", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Comentarios", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Acciones", weight=ft.FontWeight.BOLD)),
            ],
            rows=[]
        )
        
        def agregar_tarea(e):
            if not self.alumno_actual:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Selecciona un alumno primero"), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()
                return
            if not es_profesor:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden agregar tareas"), bgcolor=ft.Colors.RED)
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
        
        # Botón de agregar tarea (solo visible para profesores)
        btn_agregar_tarea = ft.ElevatedButton(
            "➕ Agregar Tarea", 
            on_click=agregar_tarea, 
            icon=ft.Icons.ASSIGNMENT_ADD,
            bgcolor=ft.Colors.GREEN_700,
            color=ft.Colors.WHITE,
            visible=es_profesor,
        )
        
        return ft.View(
            route="/tareas",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gestión de Tareas Escolares", size=24),
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
                                        btn_agregar_tarea,
                                    ], alignment=ft.MainAxisAlignment.END),
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Text("📝 Lista de Tareas", size=18, weight=ft.FontWeight.BOLD),
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
        tipo_usuario = user.get("tipo") if user else "usuario"
        es_profesor = tipo_usuario == "profesor"
        
        tareas = self.controller.obtener_por_alumno(self.alumno_actual)
        self.data_table.rows = []
        
        for tarea in tareas:
            fecha = tarea.get('fecha_entrega', '')
            if fecha:
                fecha = fecha.strftime("%d/%m/%Y") if hasattr(fecha, 'strftime') else str(fecha)
            else:
                fecha = "Sin fecha"
            
            calificacion = tarea.get('calificacion', '')
            calificacion_texto = str(calificacion) if calificacion else "Pendiente"
            calificacion_color = ft.Colors.GREEN if calificacion and calificacion >= 6 else ft.Colors.ORANGE if calificacion else ft.Colors.GREY
            
            # Obtener comentarios de la tarea
            comentarios = self.comentario_model.obtener_por_trabajo(tarea['ID_trabajo'])
            num_comentarios = len(comentarios)
            comentario_texto = f"💬 {num_comentarios}" if num_comentarios > 0 else "Sin comentarios"
            
            # Acciones según el tipo de usuario
            acciones = ft.Row([])
            
            if es_profesor:
                # Profesor puede editar, calificar y eliminar
                acciones.controls.extend([
                    ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, 
                                on_click=lambda e, t=tarea: self.editar_tarea(t)),
                    ft.IconButton(ft.Icons.GRADE, icon_color=ft.Colors.GREEN,
                                on_click=lambda e, t=tarea: self.calificar_tarea(t)),
                    ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                on_click=lambda e, t=tarea: self.eliminar_tarea(t)),
                ])
            else:
                # Alumno solo puede ver y comentar
                acciones.controls.append(
                    ft.IconButton(ft.Icons.COMMENT, icon_color=ft.Colors.ORANGE,
                                on_click=lambda e, t=tarea: self.ver_comentarios(t))
                )
            
            # Siempre mostrar botón de comentarios
            acciones.controls.append(
                ft.IconButton(ft.Icons.COMMENT, icon_color=ft.Colors.ORANGE,
                            on_click=lambda e, t=tarea: self.ver_comentarios(t))
            )
            
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(tarea.get('ID_trabajo', '')))),
                    ft.DataCell(ft.Text(tarea.get('Materia', ''))),
                    ft.DataCell(ft.Text(tarea.get('titulo_trabajo', ''))),
                    ft.DataCell(ft.Text(tarea.get('descripcion', '')[:50] + "..." if len(tarea.get('descripcion', '')) > 50 else tarea.get('descripcion', ''))),
                    ft.DataCell(ft.Text(fecha)),
                    ft.DataCell(ft.Text(calificacion_texto, color=calificacion_color)),
                    ft.DataCell(ft.Text(comentario_texto, color=ft.Colors.BLUE)),
                    ft.DataCell(acciones),
                ])
            )
        self.page.update()
    
    def ver_comentarios(self, tarea):
        """Muestra los comentarios de una tarea y permite agregar nuevos"""
        comentarios = self.comentario_model.obtener_por_trabajo(tarea['ID_trabajo'])
        
        user = getattr(self.page, "user_data", None)
        es_profesor = user.get("tipo") == "profesor" if user else False
        
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
            
            success, msg = self.comentario_model.crear(
                tarea['ID_trabajo'],
                user.get('ID_usuario'),
                comentario_field.value.strip()
            )
            
            if success:
                self.dialog.open = False
                self.cargar_datos()
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Comentario agregado"), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
            else:
                mensaje.value = msg
            self.page.update()
        
        def cancelar(e):
            self.dialog.open = False
            self.page.update()
        
        # Botón de agregar comentario (visible para todos)
        btn_agregar = ft.ElevatedButton(
            "💬 Agregar Comentario",
            on_click=guardar_comentario,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        self.dialog = ft.AlertDialog(
            title=ft.Text(f"Comentarios: {tarea.get('titulo_trabajo', '')}"),
            content=ft.Column([
                ft.Text(f"Materia: {tarea.get('Materia', '')}", size=14, weight=ft.FontWeight.BOLD),
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
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def mostrar_formulario(self, tarea=None):
        if not self.alumno_actual:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Selecciona un alumno primero"), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        user = getattr(self.page, "user_data", None)
        if user.get("tipo") != "profesor":
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden gestionar tareas"), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        materia_field = ft.TextField(label="Materia", value=tarea.get('Materia') if tarea else "", width=400, border_radius=10)
        titulo_field = ft.TextField(label="Título de la Tarea", value=tarea.get('titulo_trabajo') if tarea else "", width=400, border_radius=10)
        descripcion_field = ft.TextField(label="Descripción", value=tarea.get('descripcion') if tarea else "", multiline=True, min_lines=3, max_lines=5, width=400, border_radius=10)
        fecha_field = ft.TextField(label="Fecha de Entrega", value=tarea.get('fecha_entrega') if tarea else "", hint_text="YYYY-MM-DD", width=400, border_radius=10)
        
        mensaje = ft.Text("", color=ft.Colors.RED, size=12)
        
        def guardar(e):
            if not materia_field.value or not titulo_field.value:
                mensaje.value = "Materia y título son obligatorios"
                self.page.update()
                return
            
            if tarea:
                success, msg = self.controller.actualizar(
                    tarea['ID_trabajo'],
                    materia_field.value,
                    titulo_field.value,
                    descripcion_field.value,
                    fecha_field.value if fecha_field.value else None
                )
            else:
                success, msg = self.controller.crear(
                    self.alumno_actual,
                    materia_field.value,
                    titulo_field.value,
                    descripcion_field.value,
                    fecha_field.value if fecha_field.value else None
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
            title=ft.Text("Agregar Tarea" if not tarea else "Editar Tarea"),
            content=ft.Column([
                materia_field, 
                titulo_field, 
                descripcion_field, 
                fecha_field, 
                mensaje
            ], width=450, height=450, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def calificar_tarea(self, tarea):
        user = getattr(self.page, "user_data", None)
        if user.get("tipo") != "profesor":
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden calificar"), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        calificacion_field = ft.TextField(
            label="Calificación", 
            value=str(tarea.get('calificacion', '')) if tarea.get('calificacion') else "",
            hint_text="0-100",
            width=300,
            border_radius=10,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        mensaje = ft.Text("", color=ft.Colors.RED, size=12)
        
        def guardar_calificacion(e):
            try:
                calificacion = float(calificacion_field.value)
                if calificacion < 0 or calificacion > 100:
                    mensaje.value = "La calificación debe estar entre 0 y 100"
                    self.page.update()
                    return
            except ValueError:
                mensaje.value = "Ingresa un número válido"
                self.page.update()
                return
            
            success, msg = self.controller.calificar(tarea['ID_trabajo'], calificacion)
            
            if success:
                calif_dialog.open = False
                self.cargar_datos()
                self.page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
            else:
                mensaje.value = msg
            self.page.update()
        
        def cancelar(e):
            calif_dialog.open = False
            self.page.update()
        
        calif_dialog = ft.AlertDialog(
            title=ft.Text(f"Calificar Tarea: {tarea.get('titulo_trabajo', '')}"),
            content=ft.Column([
                ft.Text(f"Materia: {tarea.get('Materia', '')}", size=14),
                ft.Divider(),
                calificacion_field,
                mensaje,
            ], width=350, height=180, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar Calificación", on_click=guardar_calificacion, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(calif_dialog)
        calif_dialog.open = True
        self.page.update()
    
    def editar_tarea(self, tarea):
        user = getattr(self.page, "user_data", None)
        if user.get("tipo") != "profesor":
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden editar tareas"), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return
        self.mostrar_formulario(tarea)
    
    def eliminar_tarea(self, tarea):
        user = getattr(self.page, "user_data", None)
        if user.get("tipo") != "profesor":
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Solo profesores pueden eliminar tareas"), bgcolor=ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        def confirmar(e):
            success, msg = self.controller.eliminar(tarea['ID_trabajo'])
            confirm_dialog.open = False
            if success:
                self.cargar_datos()
            self.page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
        
        def cancelar(e):
            confirm_dialog.open = False
            self.page.update()
        
        confirm_dialog = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Eliminar la tarea '{tarea.get('titulo_trabajo', '')}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()