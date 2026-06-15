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
                                    leading=ft.Icon(ft.Icons.CATEGORY),
                                    title=ft.Text("Tipo de Usuario"),
                                    subtitle=ft.Text(tipo),
                                ),
                            ], spacing=10),
                            padding=20,
                        ),
                        elevation=3,
                    ),
                ]),
                padding=20,
                expand=True,
            )
        ]
    )