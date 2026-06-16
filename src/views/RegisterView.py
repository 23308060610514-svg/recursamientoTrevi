import flet as ft
from models.schemasModel import UsuarioSchema

def RegisterView(page, auth_controller):
    page.title = "Registro"

    nombre_input = ft.TextField(label="Nombre completo", width=350, prefix_icon=ft.Icons.PERSON)
    apellido_input = ft.TextField(label="Apellido", width=350, prefix_icon=ft.Icons.PERSON_OUTLINE)
    email_input = ft.TextField(label="Correo electrónico", width=350, prefix_icon=ft.Icons.EMAIL)
    password_input = ft.TextField(label="Contraseña", width=350, password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
    confirm_input = ft.TextField(label="Confirmar contraseña", width=350, password=True, can_reveal_password=True, prefix_icon=ft.Icons.LOCK)
    
    # Selector de rol
    rol_dropdown = ft.Dropdown(
        width=350,
        label="Tipo de usuario",
        value="alumno",
        options=[
            ft.dropdown.Option("alumno", "Alumno"),
            ft.dropdown.Option("profesor", "Profesor"),
        ],
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
    )
    
    # Campo para número de control (visible solo para alumnos)
    no_control_field = ft.TextField(
        label="Número de Control",
        width=350,
        prefix_icon=ft.Icons.BADGE,
        border_radius=10,
        visible=True,
    )
    
    error_text = ft.Text("", color=ft.Colors.RED, visible=False)
    
    def on_rol_change(e):
        if rol_dropdown.value == "alumno":
            no_control_field.visible = True
        else:
            no_control_field.visible = False
        page.update()
    
    rol_dropdown.on_change = on_rol_change
    
    def on_register(e):
        nombre = nombre_input.value
        apellido = apellido_input.value
        email = email_input.value
        password = password_input.value
        confirm = confirm_input.value
        rol = rol_dropdown.value
        no_control = no_control_field.value if rol == "alumno" else None
        
        # Validaciones
        if not all([nombre, apellido, email, password, confirm]):
            error_text.value = "Completa todos los campos obligatorios"
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
        
        if rol == "alumno" and not no_control:
            error_text.value = "El número de control es obligatorio para alumnos"
            error_text.visible = True
            page.update()
            return
        
        try:
            usuario_data = UsuarioSchema(nombre=nombre, apellido=apellido, email=email, password=password)
        except Exception as e:
            error_text.value = f"Error en datos: {str(e)}"
            error_text.visible = True
            page.update()
            return
        
        # Registrar según el rol
        if rol == "alumno":
            success, message = auth_controller.registrar_alumno_completo(
                nombre, apellido, no_control, email, password
            )
        else:  # profesor
            success, message = auth_controller.registrar_profesor_completo(
                nombre, apellido, email, password
            )
        
        if success:
            # Mostrar mensaje de éxito y redirigir al login
            page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=ft.Colors.GREEN)
            page.snack_bar.open = True
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
                    ft.Text("Regístrate como alumno o profesor", size=14, color=ft.Colors.GREY_600),
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    nombre_input,
                    apellido_input,
                    email_input,
                    password_input,
                    confirm_input,
                    rol_dropdown,
                    no_control_field,
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