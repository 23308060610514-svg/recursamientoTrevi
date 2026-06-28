import flet as ft

def DashboardView(page: ft.Page):
    user = getattr(page, "user_data", None)
    
    if not user:
        page.go("/")
        return ft.View(route="/dashboard", controls=[ft.Text("Redirigiendo...")])
    nombre_usuario = user.get('user') or user.get('nombre') or user.get('User') or "Usuario"
    
# En DashboardView.py o donde tengas el botón de cerrar sesión
    def cerrar_sesion(e):
    # Limpiar todos los datos de sesión
        page.user_data = None
        page.clean()  # Limpiar la página
        page.go("/")
        page.update()
    
    def navigation_change(e):
        index = e.control.selected_index
        if index == 0:
            page.go("/alumnos")
        elif index == 1:
            page.go("/profesores")
        elif index == 2:
            page.go("/calificaciones")
        elif index == 3:
            page.go("/tareas")
        elif index == 4:
            page.go("/perfil")
    
    return ft.View(
        route="/dashboard",
        controls=[
            ft.AppBar(
                title=ft.Text(f"Sistema Escolar - {nombre_usuario}"),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.LOGOUT,
                        tooltip="Cerrar Sesión",
                        on_click=cerrar_sesion
                    ),
                ],
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"¡Bienvenido, {nombre_usuario}!", size=24, weight="bold"),
                    ft.Text("Sistema de Gestión Escolar", size=16, color=ft.Colors.BLACK),
                    ft.Container(height=20),
                    ft.Text("Usa esta aplicación para gestionar:", size=14, color=ft.Colors.BLACK),
                    ft.Text("Alumnos y Profesores", size=14, color=ft.Colors.BLACK),
                    ft.Text("Calificaciones y Tareas", size=14, color=ft.Colors.BLACK),
                    ft.Text("Mantén un control académico completo", size=14, color=ft.Colors.BLACK),
                    ft.Container(height=30),
                    ft.Text("Selecciona una opción del menú inferior", size=14, color=ft.Colors.BLACK),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                expand=True,
            ),
            ft.NavigationBar(
                selected_index=0,
                on_change=navigation_change,
                bgcolor=ft.Colors.BLUE_700,
                destinations=[
                    ft.NavigationBarDestination(
                        icon=ft.Icons.GROUP_OUTLINED,
                        selected_icon=ft.Icons.GROUP,
                        label="Alumnos",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.PERSON_OUTLINE,
                        selected_icon=ft.Icons.PERSON,
                        label="Profesores",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.GRADE_OUTLINED,
                        selected_icon=ft.Icons.GRADE,
                        label="Calificaciones",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.ASSIGNMENT_OUTLINED,
                        selected_icon=ft.Icons.ASSIGNMENT,
                        label="Tareas",
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.Icons.PERSON_OUTLINE,
                        selected_icon=ft.Icons.PERSON,
                        label="Perfil",
                    ),
                ],
            ),
        ],
        padding=0,
    )
