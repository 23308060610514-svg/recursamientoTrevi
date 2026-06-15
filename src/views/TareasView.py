import flet as ft
from models.TareasModel import TareasModel
from models.AlumnosModel import AlumnosModel

class TareasView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.alumno_model = AlumnosModel()
        self.data_table = None
        self.dialog = None
        self.alumno_actual = None
        self.alumno_nombre = None

    def build(self):
        alumnos = self.alumno_model.obtener_todos()
        alumnos_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        for a in alumnos:
            alumnos_list.controls.append(
                ft.ElevatedButton(
                    text=f"{a['nombre']} {a['apellido']} - {a['no_control']}",
                    on_click=lambda e, alumno_id=a['ID_alumno'], nombre=f"{a['nombre']} {a['apellido']}": self.seleccionar_alumno(alumno_id, nombre),
                    width=400,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.BLUE_50,
                        color=ft.Colors.BLACK,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                )
            )
        
        # Texto para mostrar alumno seleccionado
        self.txt_alumno_seleccionado = ft.Text("Ningún alumno seleccionado", size=14, color=ft.Colors.GREY_600)
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight="bold")),
                ft.DataColumn(ft.Text("Materia", weight="bold")),
                ft.DataColumn(ft.Text("Título", weight="bold")),
                ft.DataColumn(ft.Text("Descripción", weight="bold")),
                ft.DataColumn(ft.Text("Fecha Entrega", weight="bold")),
                ft.DataColumn(ft.Text("Calificación", weight="bold")),
                ft.DataColumn(ft.Text("Acciones", weight="bold")),
            ],
            rows=[]
        )
        
        def agregar_tarea(e):
            if not self.alumno_actual:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Selecciona un alumno primero"), bgcolor=ft.Colors.RED)
                self.page.snack_bar.open = True
                self.page.update()
                return
            self.mostrar_formulario()
        
        def volver_dashboard(e):
            self.page.go("/dashboard")
        
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
                                    alumnos_list,
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
                                        ft.Text("👨‍🎓 Alumno seleccionado:", size=14, weight="bold"),
                                        self.txt_alumno_seleccionado,
                                    ]),
                                    ft.Divider(),
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "➕ Agregar Tarea", 
                                            on_click=agregar_tarea, 
                                            icon=ft.Icons.ASSIGNMENT_ADD,
                                            bgcolor=ft.Colors.GREEN_700,
                                            color=ft.Colors.WHITE,
                                        ),
                                    ], alignment=ft.MainAxisAlignment.END),
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Text("📝 Lista de Tareas", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Row([self.data_table]),
                        ),
                    ]),
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
            
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(tarea.get('ID_trabajo', '')))),
                    ft.DataCell(ft.Text(tarea.get('Materia', ''))),
                    ft.DataCell(ft.Text(tarea.get('titulo_trabajo', ''))),
                    ft.DataCell(ft.Text(tarea.get('descripcion', '')[:50] + "..." if len(tarea.get('descripcion', '')) > 50 else tarea.get('descripcion', ''))),
                    ft.DataCell(ft.Text(fecha)),
                    ft.DataCell(ft.Text(calificacion_texto, color=calificacion_color)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, 
                                    on_click=lambda e, t=tarea: self.editar_tarea(t)),
                        ft.IconButton(ft.Icons.GRADE, icon_color=ft.Colors.GREEN,
                                    on_click=lambda e, t=tarea: self.calificar_tarea(t)),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                    on_click=lambda e, t=tarea: self.eliminar_tarea(t)),
                    ])),
                ])
            )
        self.page.update()
    
    def mostrar_formulario(self, tarea=None):
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
            ], width=350, height=180, spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar Calificación", on_click=guardar_calificacion, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(calif_dialog)
        calif_dialog.open = True
        self.page.update()
    
    def editar_tarea(self, tarea):
        self.mostrar_formulario(tarea)
    
    def eliminar_tarea(self, tarea):
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