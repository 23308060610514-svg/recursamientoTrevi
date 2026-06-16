import flet as ft
from models.ProfesoresModel import ProfesoresModel
from models.AlumnosModel import AlumnosModel

class ProfesoresView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.model = ProfesoresModel()
        self.alumno_model = AlumnosModel()
        self.data_table = None
        self.dialog = None
        self.alumno_seleccionado = None
        
        # Obtener el profesor actual
        user = getattr(self.page, "user_data", None)
        self.id_usuario = user.get("ID_usuario") if user else None
        
        # Intentar obtener el profesor
        self.profesor_actual = None
        if self.id_usuario:
            self.profesor_actual = self.model.obtener_por_usuario(self.id_usuario)
            
            # Si no existe, intentar crear el profesor automáticamente
            if not self.profesor_actual:
                print(f"No se encontró profesor para el usuario {self.id_usuario}. Creando...")
                # Crear profesor automáticamente
                nombre = user.get("user") or user.get("nombre") or "Profesor"
                apellido = user.get("apellido") or ""
                email = user.get("Email") or user.get("email") or f"profesor{self.id_usuario}@ejemplo.com"
                password = "temp123"  # Contraseña temporal
                
                # Crear el profesor en la base de datos
                exito = self.model.crear_completo(nombre, apellido, email, password, self.id_usuario)
                if exito:
                    # Recargar el profesor
                    self.profesor_actual = self.model.obtener_por_usuario(self.id_usuario)
                    print("Profesor creado exitosamente")
                else:
                    print("Error al crear profesor automáticamente")

    def build(self):
        # Si no hay profesor actual, mostrar mensaje y botón para crear
        if not self.profesor_actual:
            def crear_profesor(e):
                # Mostrar diálogo para crear profesor
                self.mostrar_formulario_creacion()
            
            def volver_dashboard(e):
                self.page.go("/dashboard")
            
            return ft.View(
                route="/profesores",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Gestión de Profesores", size=24),
                        leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_dashboard),
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Icon(ft.Icons.PERSON_OFF, size=80, color=ft.Colors.ORANGE),
                            ft.Text("No se encontró información del profesor", size=20, color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD),
                            ft.Text("Parece que tu usuario no está registrado como profesor.", size=14, color=ft.Colors.GREY_600),
                            ft.Container(height=20),
                            ft.ElevatedButton(
                                "📝 Registrar como Profesor",
                                on_click=crear_profesor,
                                icon=ft.Icons.PERSON_ADD,
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                            ),
                            ft.TextButton("Volver al Dashboard", on_click=volver_dashboard),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ]
            )
        
        # Obtener datos
        alumnos_asignados = self.model.obtener_alumnos_asignados(self.profesor_actual['ID_profesor'])
        alumnos_disponibles = self.model.obtener_alumnos_disponibles(self.profesor_actual['ID_profesor'])
        solicitudes = self.model.obtener_solicitudes_recibidas(self.profesor_actual['ID_profesor'])
        
        # Crear lista de alumnos asignados
        alumnos_asignados_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        if alumnos_asignados:
            for a in alumnos_asignados:
                alumnos_asignados_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{a['nombre']} {a['apellido']} - {a['no_control']}", expand=True),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, alumno_id=a['ID_alumno']: self.desasignar_alumno(alumno_id),
                                tooltip="Desasignar alumno"
                            ),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=10,
                    )
                )
        else:
            alumnos_asignados_list.controls.append(
                ft.Text("No tienes alumnos asignados", color=ft.Colors.GREY_600)
            )
        
        # Crear lista de alumnos disponibles (para asignar)
        alumnos_disponibles_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        if alumnos_disponibles:
            for a in alumnos_disponibles:
                alumnos_disponibles_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"{a['nombre']} {a['apellido']} - {a['no_control']}", expand=True),
                            ft.IconButton(
                                ft.Icons.ADD,
                                icon_color=ft.Colors.GREEN,
                                on_click=lambda e, alumno_id=a['ID_alumno']: self.asignar_alumno(alumno_id),
                                tooltip="Asignar alumno"
                            ),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10,
                    )
                )
        else:
            alumnos_disponibles_list.controls.append(
                ft.Text("No hay alumnos disponibles para asignar", color=ft.Colors.GREY_600)
            )
        
        # Crear lista de solicitudes
        solicitudes_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        if solicitudes:
            for s in solicitudes:
                solicitudes_list.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"{s['nombre']} {s['apellido']} - {s['no_control']}", weight=ft.FontWeight.BOLD),
                                ft.Text(f"({s['fecha_solicitud']})", size=11, color=ft.Colors.GREY_600),
                            ]),
                            ft.Text(f"Mensaje: {s['mensaje'] if s['mensaje'] else 'Sin mensaje'}", size=12),
                            ft.Row([
                                ft.ElevatedButton(
                                    "✅ Aceptar",
                                    on_click=lambda e, sid=s['ID_solicitud']: self.responder_solicitud(sid, True),
                                    bgcolor=ft.Colors.GREEN_700,
                                    color=ft.Colors.WHITE,
                                    height=30,
                                ),
                                ft.ElevatedButton(
                                    "❌ Rechazar",
                                    on_click=lambda e, sid=s['ID_solicitud']: self.responder_solicitud(sid, False),
                                    bgcolor=ft.Colors.RED_700,
                                    color=ft.Colors.WHITE,
                                    height=30,
                                ),
                            ]),
                        ]),
                        padding=10,
                        bgcolor=ft.Colors.AMBER_50,
                        border_radius=10,
                    )
                )
        else:
            solicitudes_list.controls.append(
                ft.Text("No hay solicitudes pendientes", color=ft.Colors.GREY_600)
            )
        
        def volver_dashboard(e):
            self.page.go("/dashboard")
        
        def refrescar(e):
            self.page.go("/profesores")
        
        return ft.View(
            route="/profesores",
            controls=[
                ft.AppBar(
                    title=ft.Text(f"Gestión de Alumnos - {self.profesor_actual['nombre']}", size=24),
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_dashboard),
                    actions=[
                        ft.IconButton(ft.Icons.REFRESH, on_click=refrescar),
                    ]
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("📋 Mis Alumnos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                                    ft.Divider(),
                                    ft.Container(
                                        content=alumnos_asignados_list,
                                        height=200,
                                    ),
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("➕ Asignar Nuevo Alumno", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                                    ft.Divider(),
                                    ft.Container(
                                        content=alumnos_disponibles_list,
                                        height=200,
                                    ),
                                ]),
                                padding=20,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.Text("📩 Solicitudes Pendientes", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                                    ft.Divider(),
                                    ft.Container(
                                        content=solicitudes_list,
                                        height=200,
                                    ),
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
    
    def mostrar_formulario_creacion(self):
        """Muestra un formulario para crear el perfil de profesor"""
        nombre_field = ft.TextField(label="Nombre", width=400, border_radius=10)
        apellido_field = ft.TextField(label="Apellido", width=400, border_radius=10)
        email_field = ft.TextField(label="Correo electrónico", width=400, border_radius=10)
        especialidad_field = ft.TextField(label="Especialidad", width=400, border_radius=10)
        password_field = ft.TextField(
            label="Contraseña", 
            password=True, 
            can_reveal_password=True, 
            width=400, 
            border_radius=10
        )
        
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
            
            if not email_field.value or not email_field.value.strip():
                mensaje.value = "El email es obligatorio"
                self.page.update()
                return
            
            if not password_field.value:
                mensaje.value = "La contraseña es obligatoria"
                self.page.update()
                return
            
            if len(password_field.value) < 6:
                mensaje.value = "La contraseña debe tener al menos 6 caracteres"
                self.page.update()
                return
            
            # Crear el profesor
            success, msg = self.controller.crear(
                nombre_field.value.strip(),
                apellido_field.value.strip(),
                email_field.value.strip(),
                password_field.value,
                especialidad_field.value.strip() if especialidad_field.value else None,
                self.id_usuario
            )
            
            if success:
                self.dialog.open = False
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Profesor registrado exitosamente"), bgcolor=ft.Colors.GREEN)
                self.page.snack_bar.open = True
                # Recargar la vista
                self.page.go("/profesores")
            else:
                mensaje.value = msg
            self.page.update()
        
        def cancelar(e):
            self.dialog.open = False
            self.page.go("/dashboard")
            self.page.update()
        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Registrar como Profesor"),
            content=ft.Column([
                ft.Text("Completa tus datos para registrarte como profesor", size=14, color=ft.Colors.GREY_600),
                ft.Divider(),
                nombre_field,
                apellido_field,
                email_field,
                especialidad_field,
                password_field,
                mensaje,
            ], width=450, height=450, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Registrar", on_click=guardar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def asignar_alumno(self, id_alumno):
        """Asigna un alumno al profesor actual"""
        success, msg = self.model.asignar_alumno(self.profesor_actual['ID_profesor'], id_alumno)
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=ft.Colors.GREEN if success else ft.Colors.RED
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        if success:
            # Recargar la vista
            self.page.go("/profesores")
    
    def desasignar_alumno(self, id_alumno):
        """Desasigna un alumno del profesor actual"""
        def confirmar(e):
            success, msg = self.model.desasignar_alumno(self.profesor_actual['ID_profesor'], id_alumno)
            
            dialog.open = False
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(msg),
                bgcolor=ft.Colors.GREEN if success else ft.Colors.RED
            )
            self.page.snack_bar.open = True
            self.page.update()
            
            if success:
                self.page.go("/profesores")
        
        def cancelar(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar desasignación"),
            content=ft.Text("¿Estás seguro de que deseas desasignar a este alumno?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Desasignar", on_click=confirmar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def responder_solicitud(self, id_solicitud, aceptar):
        """Acepta o rechaza una solicitud"""
        success, msg = self.model.responder_solicitud(id_solicitud, aceptar)
        
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=ft.Colors.GREEN if success else ft.Colors.RED
        )
        self.page.snack_bar.open = True
        self.page.update()
        
        if success:
            self.page.go("/profesores")