import flet as ft
from controllers.UsuariosController import AuthController
from controllers.AlumnosController import AlumnosController
from controllers.ProfesoresController import ProfesoresController
from controllers.CalificacionesController import CalificacionesController
from controllers.TareasController import TareasController
from views.LoginView import LoginView
from views.RegisterView import RegisterView
from views.DashboardView import DashboardView
from views.UsuariosView import UserView  
from views.ProfesoresView import ProfesoresView
from views.TareasView import TareasView
from views.CalificacionesView import CalificacionesView
from views.AlumnosView import AlumnosView

def start(page: ft.Page):
    page.title = "Sistema Escolar"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 1024
    page.window_height = 768
    
    auth_controller = AuthController()
    alumnos_controller = AlumnosController()
    profesores_controller = ProfesoresController()
    calificaciones_controller = CalificacionesController()
    tareas_controller = TareasController()
    
    def route_change(e):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(LoginView(page, auth_controller))
        
        elif page.route == "/register":
            page.views.append(RegisterView(page, auth_controller))
        
        elif page.route == "/dashboard":
            if not getattr(page, "user_data", None):
                page.go("/")
                return
            page.views.append(DashboardView(page))
        
        elif page.route == "/perfil":
            if not getattr(page, "user_data", None):
                page.go("/")
                return
            page.views.append(UserView(page, auth_controller))
        
        elif page.route == "/alumnos":
            if not getattr(page, "user_data", None):
                page.go("/")
                return
            alumnos_view = AlumnosView(page, alumnos_controller)
            page.views.append(alumnos_view.build())
        
        elif page.route == "/profesores":
            if not getattr(page, "user_data", None):
                page.go("/")
                return
            profesores_view = ProfesoresView(page, profesores_controller)
            page.views.append(profesores_view.build())
        
        elif page.route == "/calificaciones":
            if not getattr(page, "user_data", None):
                page.go("/")
                return
            calificaciones_view = CalificacionesView(page, calificaciones_controller)
            page.views.append(calificaciones_view.build())
        
        elif page.route == "/tareas":
            if not getattr(page, "user_data", None):
                page.go("/")
                return
            tareas_view = TareasView(page, tareas_controller)
            page.views.append(tareas_view.build())
        
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Enlace inválido"),
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.go("/")
        
        page.update()
    
    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    if page.route == "/":
        route_change(None)
    else:
        page.go("/")

def main():
    ft.app(target=start)

if __name__ == "__main__":
    main()