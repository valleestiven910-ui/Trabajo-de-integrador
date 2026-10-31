import flet as ft

from gui.Login import mostrar_login
from gui.usuario import mostrar_usuarios
from gui.finca import mostrar_fincas
from gui.vacas import mostrar_vacas
from gui.medicamento import mostrar_medicamento
from gui.producción import mostrar_producciones
from gui.alimentación import vista_alimentación
from gui.catalogo import mostrar_catalogo
from gui.splash_screen import VIDEO_PATH, mostrar_splash

def main(page: ft.Page):
    page.title = "Sistema de Gestión Ganadera"
    page.window_width = 1100
    page.window_height = 700
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT

    def mostrar_sistema(usuario_actual):
        page.controls.clear()
        contenido = ft.Container(expand=True, padding=20)
        vistas = [
            ("Usuarios", mostrar_usuarios),
            ("Fincas", mostrar_fincas),
            ("Vacas", mostrar_vacas),
            ("Medicamentos", mostrar_medicamento),
            ("Producción", mostrar_producciones),
            ("Alimentación", vista_alimentación),
            ("Catálogo", mostrar_catalogo),
        ]

        def cargar_vista(vista):
            control = vista(page)
            if isinstance(control, ft.View):
                control = ft.Column(controls=control.controls, expand=True)
            contenido.content = control
            page.update()

        menu = ft.Column(
            controls=[
                ft.Text("GAVAD", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Hola, {usuario_actual.nombres}"),
                *[
                    ft.ElevatedButton(
                        nombre,
                        width=170,
                        on_click=lambda e, vista=vista: cargar_vista(vista),
                    )
                    for nombre, vista in vistas
                ],
                ft.TextButton(
                    "Cerrar sesión",
                    on_click=lambda e: mostrar_login(page, mostrar_sistema),
                ),
            ],
            width=190,
            spacing=10,
        )

        page.add(
            ft.Row(
                controls=[menu, ft.VerticalDivider(width=1), contenido],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            )
        )
        cargar_vista(mostrar_usuarios)

    mostrar_splash(page, lambda: mostrar_login(page, mostrar_sistema))


if __name__ == "__main__":
    ft.run(main, assets_dir=str(VIDEO_PATH.parent))