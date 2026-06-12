import flet as ft

def UserView(page, auth_controller):
    page.title = "Perfil"
    user = getattr(page, "user_data", None)
    
    def formatear_fecha(fecha):
        if not fecha:
            return "No disponible"
        if hasattr(fecha, 'strftime'):
            return fecha.strftime("%d/%m/%Y")
        if isinstance(fecha, str):
            if ' ' in fecha:
                fecha_parte = fecha.split(' ')[0]
                partes = fecha_parte.split('-')
                if len(partes) == 3:
                    return f"{partes[2]}/{partes[1]}/{partes[0]}"
            else:
                partes = fecha.split('-')
                if len(partes) == 3:
                    return f"{partes[2]}/{partes[1]}/{partes[0]}"
        return str(fecha)
    
    
    if not user:
        return ft.View(
            route="/perfil",
            controls=[
                ft.AppBar(title=ft.Text("Perfil de Usuario", size=30)),
                ft.Container(
                    ft.Column([
                        ft.Text("No hay datos de usuario disponibles", size=20, color=ft.Colors.RED),
                        ft.ElevatedButton("Volver al inicio", on_click=lambda _: page.go("/"))
                    ]),
                    padding=20, expand=True,
                    alignment=ft.alignment.center
                ),
            ]
        )
    

    if isinstance(user, dict):
        nombre_usuario = user.get('User') or user.get('username') or user.get('nombre') or "No disponible"
        email = user.get('Email') or user.get('email') or "No disponible"
        id_usuario = user.get('ID_usuario') or user.get('id') or "No disponible"
        fecha_registro = user.get('Fecha_Registro') or user.get('fecha_registro') or "No disponible"
    

    elif isinstance(user, (tuple, list)):
    
        if len(user) >= 5:
            id_usuario = user[0] if user[0] else "No disponible"
            nombre_usuario = user[1] if user[1] else "No disponible"
            email = user[2] if user[2] else "No disponible"
            fecha_registro = user[4] if user[4] else "No disponible"
        else:
            nombre_usuario = "Datos incompletos"
            email = "Datos incompletos"
            id_usuario = "Datos incompletos"
            fecha_registro = "Datos incompletos"
    
    
    else:
        nombre_usuario = getattr(user, 'User', None) or getattr(user, 'username', None) or "No disponible"
        email = getattr(user, 'Email', None) or getattr(user, 'email', None) or "No disponible"
        id_usuario = getattr(user, 'ID_usuario', None) or getattr(user, 'id', None) or "No disponible"
        fecha_registro = getattr(user, 'Fecha_Registro', None) or getattr(user, 'fecha_registro', None) or "No disponible"
    
    
    return ft.View(
        route="/perfil",
        controls=[
            ft.AppBar(
                title=ft.Text("Perfil de Usuario", size=30),
                actions=[
                    ft.IconButton(ft.Icons.BOOK, on_click=lambda _: page.go("/dashboard")),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, on_click=lambda _: page.go("/"))
                ],
            ),
            ft.Container(
                ft.Column([
                    ft.Divider(thickness=8, color=ft.Colors.BLUE),
                    ft.Row([ft.Text(f"Usuario: {nombre_usuario}", size=20)]),
                    ft.Divider(thickness=6, color=ft.Colors.BLUE),
                    ft.Row([ft.Text(f"Email: {email}", size=20)]),
                    ft.Divider(thickness=6, color=ft.Colors.BLUE),
                    ft.Row([ft.Text(f"ID de Usuario: {id_usuario}", size=20)]),
                    ft.Divider(thickness=6, color=ft.Colors.BLUE),
                    ft.Row([ft.Text(f"Fecha de registro: {formatear_fecha(fecha_registro)}", size=20)]),
                    ft.Divider(thickness=8, color=ft.Colors.BLUE),
                ], expand=True),
                padding=20, expand=True,
            ),
        ]
    )