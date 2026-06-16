import flet as ft

def UserView(page, auth_controller):
    user = getattr(page, "user_data", None)
    
    def volver_dashboard(e):
        page.go("/dashboard")
    
    if not user:
        return ft.View(
            route="/perfil",
            controls=[
                ft.AppBar(title=ft.Text("Perfil"), leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_dashboard)),
                ft.Container(ft.Text("No hay sesión activa"), alignment=ft.alignment.center, expand=True)
            ]
        )
    
    nombre = user.get("user") or user.get("nombre") or "Usuario"
    email = user.get("Email") or "No disponible"
    id_usuario = user.get("ID_usuario") or "No disponible"
    tipo = user.get("tipo") or "No definido"
    
    # Traducir tipo de usuario al español
    tipo_espanol = {
        "alumno": "Alumno",
        "profesor": "Profesor",
        "admin": "Administrador",
        "usuario": "Usuario"
    }.get(tipo, tipo)
    
    # Icono según tipo de usuario
    icono_tipo = {
        "alumno": ft.Icons.SCHOOL,
        "profesor": ft.Icons.SCHOOL,
        "admin": ft.Icons.ADMIN_PANEL_SETTINGS,
        "usuario": ft.Icons.PERSON
    }.get(tipo, ft.Icons.PERSON)
    
    # Color según tipo de usuario
    color_tipo = {
        "alumno": ft.Colors.BLUE,
        "profesor": ft.Colors.GREEN,
        "admin": ft.Colors.PURPLE,
        "usuario": ft.Colors.GREY
    }.get(tipo, ft.Colors.GREY)
    
    return ft.View(
        route="/perfil",
        controls=[
            ft.AppBar(
                title=ft.Text("Mi Perfil"),
                leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=volver_dashboard),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.BLUE),
                                ft.Text(nombre, size=24, weight="bold"),
                                ft.Container(
                                    content=ft.Text(tipo_espanol, size=14, weight="bold", color=ft.Colors.WHITE),
                                    bgcolor=color_tipo,
                                    border_radius=15,
                                ),
                                ft.Divider(),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.EMAIL),
                                    title=ft.Text("Correo electrónico"),
                                    subtitle=ft.Text(email),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.BADGE),
                                    title=ft.Text("ID de Usuario"),
                                    subtitle=ft.Text(str(id_usuario)),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(icono_tipo, color=color_tipo),
                                    title=ft.Text("Tipo de Usuario"),
                                    subtitle=ft.Text(tipo_espanol, weight=ft.FontWeight.BOLD, color=color_tipo),
                                ),
                            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
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