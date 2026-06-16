import flet as ft

class AlumnosView:
    def __init__(self, page, controller):
        self.page = page
        self.controller = controller
        self.data_table = None
        self.dialog = None

    def build(self):
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
        
        def agregar_alumno(e):
            self.mostrar_formulario()
        
        def volver_dashboard(e):
            self.page.go("/dashboard")
        
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
                                    ft.Row([
                                        ft.ElevatedButton(
                                            "➕ Agregar Alumno", 
                                            on_click=agregar_alumno, 
                                            icon=ft.Icons.ADD,
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
                        ft.Text("📋 Lista de Alumnos", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Container(
                            content=ft.Row([self.data_table], alignment=ft.MainAxisAlignment.CENTER),
                        ),
                    ]),
                    padding=20,
                    expand=True,
                )
            ]
        )
    
    def cargar_datos(self):
        alumnos = self.controller.listar()
        self.data_table.rows = []
        
        for alumno in alumnos:
            self.data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(alumno.get('ID_alumno', '')))),
                    ft.DataCell(ft.Text(alumno.get('nombre', ''))),
                    ft.DataCell(ft.Text(alumno.get('apellido', ''))),
                    ft.DataCell(ft.Text(alumno.get('no_control', ''))),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.BLUE, 
                                    on_click=lambda e, a=alumno: self.editar_alumno(a)),
                        ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED,
                                    on_click=lambda e, a=alumno: self.eliminar_alumno(a)),
                    ])),
                ])
            )
        self.page.update()
    
    def mostrar_formulario(self, alumno=None):
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
            
            user = getattr(self.page, "user_data", None)
            id_usuario = user.get('ID_usuario') if user else None
            
            if not id_usuario:
                mensaje.value = "Error: No se encontró el usuario logueado"
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
        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Agregar Alumno" if not alumno else "Editar Alumno"),
            content=ft.Column([
                nombre_field, 
                apellido_field, 
                control_field, 
                mensaje
            ], width=450, height=280, spacing=10),
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