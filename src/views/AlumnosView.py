import flet as ft
from models.ProfesoresModel import ProfesoresModel

class AlumnosView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.profesor_model = ProfesoresModel()
        self.data_table = None
        self.dialog = None
        
        # Obtener el alumno actual
        user = getattr(self.page, "user_data", None)
        self.id_usuario = user.get("ID_usuario") if user else None
        
        # Intentar obtener el alumno
        self.alumno_actual = None
        if self.id_usuario:
            try:
                self.alumno_actual = self.controller.obtener_por_usuario(self.id_usuario)
            except Exception as e:
                print(f"Error al obtener alumno: {e}")
                self.alumno_actual = None

    def build(self):
        # Si no hay alumno actual, mostrar mensaje
        if not self.alumno_actual:
            def volver_dashboard(e):
                self.page.go("/dashboard")
            
            def registrar_alumno(e):
                self.mostrar_formulario_registro()
            
            return ft.View(
                route="/alumnos",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Gestión de Alumnos", size=24),
                        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_dashboard),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PERSON_OFF, size=80, color=ft.Colors.ORANGE),
                            ft.Text("No se encontró información del alumno", size=20, color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD),
                            ft.Text("Parece que tu usuario no está registrado como alumno.", size=14, color=ft.Colors.GREY_600),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "📝 Registrar como Alumno",
                                on_click=registrar_alumno,
                                icon=ft.Icons.PERSON_ADD,
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                            ),
                            ft.TextButton("Volver al Dashboard", on_click=volver_dashboard),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        expand=True,
                    )
                ]
            )
        
        # Si hay alumno, mostrar la vista normal
        return self.build_vista_normal()
    
    def build_vista_normal(self):
        """Construye la vista normal cuando el alumno existe"""
        # Obtener solicitudes del alumno
        solicitudes = self.profesor_model.obtener_solicitudes_enviadas(self.alumno_actual['ID_alumno'])
        
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Apellido")),
                ft.DataColumn(ft.Text("No. Control")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[]
        )
        
        self.cargar_datos()
        
        def volver_dashboard(e):
            self.page.go("/dashboard")
        
        # Mostrar solicitudes del alumno
        solicitudes_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        if solicitudes:
            for s in solicitudes:
                estado_color = {
                    'pendiente': ft.Colors.ORANGE,
                    'aceptada': ft.Colors.GREEN,
                    'rechazada': ft.Colors.RED
                }.get(s['estado'], ft.Colors.GREY)
                
                estado_texto = {
                    'pendiente': '⏳ Pendiente',
                    'aceptada': '✅ Aceptada',
                    'rechazada': '❌ Rechazada'
                }.get(s['estado'], s['estado'])
                
                solicitudes_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{s['nombre']} {s['apellido']}", expand=True),
                            ft.Text(estado_texto, color=estado_color, weight=ft.FontWeight.BOLD),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                    )
                )
        else:
            solicitudes_list.controls.append(
                ft.Text("No has enviado solicitudes a profesores", color=ft.Colors.GREY_600)
            )
        
        tabla_scroll = ft.Container(
            content=self.data_table,
            height=400,
        )
        
        return ft.View(
            route="/alumnos",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gestión de Alumnos", size=24),
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
                                    ft.Text("📋 Mis Solicitudes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                                    ft.Divider(),
                                    ft.Container(
                                        content=solicitudes_list,
                                        height=150,
                                    ),
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Text("📋 Lista de Alumnos", size=18, weight=ft.FontWeight.BOLD),
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
    
    def mostrar_formulario_registro(self):
        """Muestra un formulario para registrar al alumno"""
        nombre_field = ft.TextField(label="Nombre", width=400, border_radius=10)
        apellido_field = ft.TextField(label="Apellido", width=400, border_radius=10)
        no_control_field = ft.TextField(label="Número de Control", width=400, border_radius=10)
        
        mensaje = ft.Text("", color=ft.Colors.RED, size=12)
        
        def guardar(e):
            if not nombre_field.value or not nombre_field.value.strip():
                mensaje.value = "El nombre es obligatorio"
                self.page.update()
                return
            
            if not apellido_field.value or not apellido_field.value.strip():
                mensaje.value = "El apellido es obligatorio"
                self.page.update()
                return
            
            if not no_control_field.value or not no_control_field.value.strip():
                mensaje.value = "El número de control es obligatorio"
                self.page.update()
                return
            
            # Crear el alumno
            success, msg = self.controller.crear(
                nombre_field.value.strip(),
                apellido_field.value.strip(),
                no_control_field.value.strip(),
                self.id_usuario
            )
            
            if success:
                dialog.open = False
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Alumno registrado exitosamente"), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
                # Recargar la vista
                self.page.go("/alumnos")
            else:
                mensaje.value = msg
            self.page.update()
        
        def cancelar(e):
            dialog.open = False
            self.page.go("/dashboard")
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Registrar como Alumno"),
            content=ft.Column([
                ft.Text("Completa tus datos para registrarte como alumno", size=14, color=ft.Colors.GREY_600),
                ft.Divider(),
                nombre_field,
                apellido_field,
                no_control_field,
                mensaje,
            ], width=450, height=320, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Registrar", on_click=guardar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def cargar_datos(self):
        alumnos = self.controller.listar()
        self.data_table.rows = []
        
        for alumno in alumnos:
            # Verificar si el alumno es el actual
            es_actual = alumno.get('ID_alumno') == self.alumno_actual['ID_alumno'] if self.alumno_actual else False
            
            acciones = ft.Row([
                ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, 
                            on_click=lambda e, a=alumno: self.editar_alumno(a)),
            ])
            
            # Si no es el alumno actual, mostrar botón para enviar solicitud
            if not es_actual:
                acciones.controls.append(
                    ft.IconButton(
                        ft.Icons.SEND,
                        icon_color=ft.Colors.GREEN,
                        on_click=lambda e, a=alumno: self.enviar_solicitud(a),
                        tooltip="Enviar solicitud a profesor"
                    )
                )
            
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(alumno.get('ID_alumno', '')))),
                    ft.DataCell(ft.Text(alumno.get('nombre', ''))),
                    ft.DataCell(ft.Text(alumno.get('apellido', ''))),
                    ft.DataCell(ft.Text(alumno.get('no_control', ''))),
                    ft.DataCell(acciones),
                ])
            )
        self.page.update()
    
    def enviar_solicitud(self, alumno):
        """Envía una solicitud a un profesor"""
        # Obtener profesores disponibles
        profesores = self.profesor_model.obtener_todos()
        
        if not profesores:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("No hay profesores disponibles"),
                bgcolor=ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Crear dropdown de profesores
        profesor_dropdown = ft.Dropdown(
            label="Seleccionar profesor",
            width=400,
            options=[
                ft.dropdown.Option(
                    str(p['ID_profesor']), 
                    f"{p['nombre']} {p['apellido']} - {p['especialidad'] or 'Sin especialidad'}"
                ) for p in profesores
            ],
            border_radius=10,
        )
        
        mensaje_field = ft.TextField(
            label="Mensaje (opcional)",
            multiline=True,
            min_lines=2,
            max_lines=4,
            width=400,
            border_radius=10,
        )
        
        mensaje_error = ft.Text("", color=ft.Colors.RED, size=12)
        
        def enviar(e):
            if not profesor_dropdown.value:
                mensaje_error.value = "Selecciona un profesor"
                self.page.update()
                return
            
            success, msg = self.profesor_model.crear_solicitud(
                self.alumno_actual['ID_alumno'],
                int(profesor_dropdown.value),
                mensaje_field.value if mensaje_field.value else None
            )
            
            if success:
                dialog.open = False
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(msg),
                    bgcolor=ft.Colors.GREEN
                )
                self.page.snack_bar.open = True
                self.page.update()
                # Recargar la vista
                self.page.go("/alumnos")
            else:
                mensaje_error.value = msg
                self.page.update()
        
        def cancelar(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Solicitar agregar a profesor"),
            content=ft.Column([
                ft.Text(f"Alumno: {self.alumno_actual['nombre']} {self.alumno_actual['apellido']}", weight=ft.FontWeight.BOLD),
                ft.Divider(),
                profesor_dropdown,
                mensaje_field,
                mensaje_error,
            ], width=450, height=320, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Enviar Solicitud", on_click=enviar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def mostrar_formulario(self, alumno=None):
        """Muestra el formulario para crear/editar alumno"""
        nombre_field = ft.TextField(label="Nombre", value=alumno.get('nombre') if alumno else "", width=400, border_radius=10)
        apellido_field = ft.TextField(label="Apellido", value=alumno.get('apellido') if alumno else "", width=400, border_radius=10)
        control_field = ft.TextField(label="Número de Control", value=alumno.get('no_control') if alumno else "", width=400, border_radius=10)
        
        mensaje = ft.Text("", color=ft.Colors.RED, size=12)
        
        def guardar(e):
            if not nombre_field.value or not nombre_field.value.strip():
                mensaje.value = "El nombre es obligatorio"
                self.page.update()
                return
            
            if not apellido_field.value or not apellido_field.value.strip():
                mensaje.value = "El apellido es obligatorio"
                self.page.update()
                return
            
            if not control_field.value or not control_field.value.strip():
                mensaje.value = "El número de control es obligatorio"
                self.page.update()
                return
            
            if alumno:
                success, msg = self.controller.actualizar(
                    alumno['ID_alumno'], 
                    nombre_field.value.strip(), 
                    apellido_field.value.strip(), 
                    control_field.value.strip()
                )
            else:
                success, msg = self.controller.crear(
                    nombre_field.value.strip(), 
                    apellido_field.value.strip(), 
                    control_field.value.strip(), 
                    self.id_usuario
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
            title=ft.Text("Agregar Alumno" if not alumno else "Editar Alumno"),
            content=ft.Column([
                nombre_field, 
                apellido_field, 
                control_field, 
                mensaje
            ], width=450, height=280, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def editar_alumno(self, alumno):
        self.mostrar_formulario(alumno)
    
    def eliminar_alumno(self, alumno):
        def confirmar(e):
            success, msg = self.controller.eliminar(alumno['ID_alumno'])
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
            content=ft.Text(f"¿Eliminar a {alumno['nombre']} {alumno['apellido']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()