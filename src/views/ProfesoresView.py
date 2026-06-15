import flet as ft
from models.ProfesoresModel import ProfesoresModel

class ProfesoresView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.model = ProfesoresModel()
        self.data_table = None
        self.dialog = None

    def build(self):
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight="bold")),
                ft.DataColumn(ft.Text("Nombre", weight="bold")),
                ft.DataColumn(ft.Text("Apellido", weight="bold")),
                ft.DataColumn(ft.Text("Email", weight="bold")),
                ft.DataColumn(ft.Text("Especialidad", weight="bold")),
                ft.DataColumn(ft.Text("Acciones", weight="bold")),
            ],
            rows=[]
        )
        
        self.cargar_datos()
        
        def agregar_profesor(e):
            self.mostrar_formulario()
        
        def volver_dashboard(e):
            self.page.go("/dashboard")
        
        return ft.View(
            route="/profesores",
            controls=[
                ft.AppBar(
                    title=ft.Text("Gestión de Profesores", size=24),
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
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "➕ Agregar Profesor", 
                                            on_click=agregar_profesor, 
                                            icon=ft.Icons.PERSON_ADD,
                                            bgcolor=ft.Colors.GREEN_700,
                                            color=ft.Colors.WHITE,
                                        ),
                                    ], alignment=ft.MainAxisAlignment.END),
                                ]),
                                padding=15,
                            ),
                            elevation=3,
                        ),
                        ft.Container(height=20),
                        ft.Text("📋 Lista de Profesores", size=18, weight=ft.FontWeight.BOLD),
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
    
    def cargar_datos(self):
        profesores = self.controller.listar()
        self.data_table.rows = []
        
        for profesor in profesores:
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(profesor.get('ID_profesor', '')))),
                    ft.DataCell(ft.Text(profesor.get('nombre', ''))),
                    ft.DataCell(ft.Text(profesor.get('apellido', ''))),
                    ft.DataCell(ft.Text(profesor.get('Email', ''))),
                    ft.DataCell(ft.Text(profesor.get('especialidad', 'Sin especificar'))),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, 
                                    on_click=lambda e, p=profesor: self.editar_profesor(p)),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                    on_click=lambda e, p=profesor: self.eliminar_profesor(p)),
                    ])),
                ])
            )
        self.page.update()
    
    def mostrar_formulario(self, profesor=None):
        nombre_field = ft.TextField(label="Nombre", value=profesor.get('nombre') if profesor else "", width=400, border_radius=10)
        apellido_field = ft.TextField(label="Apellido", value=profesor.get('apellido') if profesor else "", width=400, border_radius=10)
        email_field = ft.TextField(label="Correo electrónico", value=profesor.get('Email') if profesor else "", width=400, border_radius=10)
        especialidad_field = ft.TextField(label="Especialidad", value=profesor.get('especialidad') if profesor else "", width=400, border_radius=10)
        password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=400, border_radius=10, visible=not profesor)
        confirm_field = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=400, border_radius=10, visible=not profesor)
        
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
            
            if profesor:
                success, msg = self.controller.actualizar(
                    profesor['ID_profesor'],
                    nombre_field.value.strip(),
                    apellido_field.value.strip(),
                    email_field.value.strip(),
                    especialidad_field.value.strip() if especialidad_field.value else None
                )
            else:
                if not password_field.value:
                    mensaje.value = "La contraseña es obligatoria"
                    self.page.update()
                    return
                
                if not confirm_field.value:
                    mensaje.value = "Confirma la contraseña"
                    self.page.update()
                    return
                
                if password_field.value != confirm_field.value:
                    mensaje.value = "Las contraseñas no coinciden"
                    self.page.update()
                    return
                
                if len(password_field.value) < 6:
                    mensaje.value = "La contraseña debe tener al menos 6 caracteres"
                    self.page.update()
                    return
                
                user = getattr(self.page, "user_data", None)
                id_usuario = user.get('ID_usuario') if user else None
                
                if not id_usuario:
                    mensaje.value = "Error: No se encontró el usuario logueado"
                    self.page.update()
                    return
                
                success, msg = self.controller.crear(
                    nombre_field.value.strip(),
                    apellido_field.value.strip(),
                    email_field.value.strip(),
                    password_field.value,
                    especialidad_field.value.strip() if especialidad_field.value else None,
                    id_usuario
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
        
        altura = 400 if not profesor else 300
        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Agregar Profesor" if not profesor else "Editar Profesor"),
            content=ft.Column([
                nombre_field, 
                apellido_field, 
                email_field, 
                especialidad_field,
                password_field, 
                confirm_field, 
                mensaje
            ], width=450, height=altura, spacing=10, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Guardar", on_click=guardar, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def editar_profesor(self, profesor):
        self.mostrar_formulario(profesor)
    
    def eliminar_profesor(self, profesor):
        def confirmar(e):
            success, msg = self.controller.eliminar(profesor['ID_profesor'])
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
            content=ft.Text(f"¿Eliminar al profesor {profesor['nombre']} {profesor['apellido']}?\n\n⚠️ Esta acción también eliminará su cuenta de usuario asociada."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton("Eliminar", on_click=confirmar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
            ],
        )
        self.page.overlay.append(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()