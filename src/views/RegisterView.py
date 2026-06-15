import flet as ft
from models.schemasModel import UsuarioSchema

def RegisterView(page, auth_controller):
    page.title = "Registro"

    nombre_input = ft.TextField(label="Nombre completo", width=350, prefix_icon=ft.Icons.PERSON)
    email_input = ft.TextField(label="Correo electrónico", width=350, prefix_icon=ft.Icons.EMAIL)
    password_input = ft.TextField(label="Contraseña", width=350, password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
    confirm_input = ft.TextField(label="Confirmar contraseña", width=350, password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
    
    error_text = ft.Text("", color=ft.Colors.RED, visible=False)
    
    def on_register(e):
        nombre = nombre_input.value
        email = email_input.value
        password = password_input.value
        confirm = confirm_input.value
        
        if not all([nombre, email, password, confirm]):
            error_text.value = "Completa todos los campos"
            error_text.visible = True
            page.update()
            return
        
        if password != confirm:
            error_text.value = "Las contraseñas no coinciden"
            error_text.visible = True
            page.update()
            return
        
        if len(password) < 6:
            error_text.value = "La contraseña debe tener al menos 6 caracteres"
            error_text.visible = True
            page.update()
            return
        
        try:
            usuario_data = UsuarioSchema(nombre=nombre, email=email, password=password)
        except Exception as e:
            error_text.value = f"Error en datos: {str(e)}"
            error_text.visible = True
            page.update()
            return
        
        success, message = auth_controller.registrar(usuario_data)
        
        if success:
            page.go("/")
        else:
            error_text.value = message
            error_text.visible = True
            page.update()
    
    def on_back(e):
        page.go("/")
    
    return ft.View(
        route="/register",
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("📝 Crear Cuenta", size=30, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    nombre_input,
                    email_input,
                    password_input,
                    confirm_input,
                    error_text,
                    ft.ElevatedButton("Registrarse", on_click=on_register, width=350, height=45),
                    ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=on_back),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                border_radius=10,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=10)
            )
        ]
    )