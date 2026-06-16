import flet as ft

def LoginView(page, auth_controller):
    page.title = "Iniciar Sesión"
    
    email_input = ft.TextField(
        label="Correo electrónico",
        hint_text="ejemplo@correo.com",
        width=350,
        prefix_icon=ft.Icons.EMAIL
    )
    
    password_input = ft.TextField(
        label="Contraseña",
        hint_text="••••••••",
        width=350,
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK
    )
    
    error_text = ft.Text("", color=ft.Colors.RED, visible=False)
    
    def on_login(e):
        email = email_input.value
        password = password_input.value
        
        if not email or not password:
            error_text.value = "Completa todos los campos"
            error_text.visible = True
            page.update()
            return
        
        user, message = auth_controller.login(email, password)
        
        if user:
            page.user_data = user
            # Mostrar mensaje de bienvenida con el rol
            rol_espanol = {
                "alumno": "Alumno",
                "profesor": "Profesor",
                "admin": "Administrador"
            }.get(user.get("tipo"), "Usuario")
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"¡Bienvenido {rol_espanol} {user.get('user', '')}!"),
                bgcolor=ft.Colors.GREEN
            )
            page.snack_bar.open = True
            page.go("/dashboard")
        else:
            error_text.value = message
            error_text.visible = True
            page.update()
    
    def on_register(e):
        page.go("/register")
    
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("📚 Sistema Escolar", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text("Iniciar Sesión", size=24, weight=ft.FontWeight.W_500),
                    ft.Text("Acceso para alumnos y profesores", size=14, color=ft.Colors.GREY_600),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    email_input,
                    password_input,
                    error_text,
                    ft.ElevatedButton("Ingresar", on_click=on_login, width=350, height=45),
                    ft.TextButton("¿No tienes cuenta? Regístrate", on_click=on_register),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10)
            )
        ]
    )