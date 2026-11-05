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


VERDE = "#034d2c"
CREMA = "#faf7ca"


def main(page: ft.Page):
    page.title = "Sistema de Gestión Ganadera"
    page.window_width = 1100
    page.window_height = 700
    page.window_resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = CREMA
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=VERDE,
            on_primary=CREMA,
            secondary=VERDE,
            on_secondary=CREMA,
            surface=CREMA,
            on_surface=VERDE,
            on_surface_variant=VERDE,
            outline=VERDE,
            outline_variant=VERDE,
            surface_container_low=CREMA,
        ),
        text_theme=ft.TextTheme(
            body_small=ft.TextStyle(color=VERDE),
            body_medium=ft.TextStyle(color=VERDE),
            body_large=ft.TextStyle(color=VERDE),
            title_small=ft.TextStyle(color=VERDE),
            title_medium=ft.TextStyle(color=VERDE),
            title_large=ft.TextStyle(color=VERDE),
            headline_small=ft.TextStyle(color=VERDE),
            headline_medium=ft.TextStyle(color=VERDE),
            headline_large=ft.TextStyle(color=VERDE),
        ),
        data_table_theme=ft.DataTableTheme(
            heading_row_color=VERDE,
            heading_text_style=ft.TextStyle(
                color=CREMA,
                weight=ft.FontWeight.BOLD,
            ),
            data_row_color=CREMA,
            data_text_style=ft.TextStyle(color=VERDE),
            divider_thickness=1,
            decoration=ft.BoxDecoration(
                bgcolor=CREMA,
                border=ft.Border.all(1, VERDE),
                border_radius=8,
            ),
        ),
        dialog_theme=ft.DialogTheme(
            bgcolor=CREMA,
            title_text_style=ft.TextStyle(
                color=VERDE,
                weight=ft.FontWeight.BOLD,
            ),
            content_text_style=ft.TextStyle(color=VERDE),
        ),
        scaffold_bgcolor=CREMA,
        card_bgcolor=CREMA,
        use_material3=True,
    )

    def mostrar_sistema(usuario_actual):
        page.controls.clear()
        contenido = ft.Container(expand=True, padding=20, bgcolor=CREMA)
        vistas = [
            ("Usuarios", ft.Icons.PEOPLE_ALT, mostrar_usuarios),
            ("Fincas", ft.Icons.LANDSCAPE, mostrar_fincas),
            ("Vacas", ft.Icons.ASSESSMENT, mostrar_vacas),
            ("Medicamentos", ft.Icons.MEDICATION, mostrar_medicamento),
            ("Producción", ft.Icons.WATER_DROP, mostrar_producciones),
            ("Alimentación", ft.Icons.GRASS, vista_alimentación),
            ("Catálogo", ft.Icons.STORE, mostrar_catalogo),
        ]

        def cargar_vista(vista):
            control = vista(page)
            if isinstance(control, ft.View):
                controles_vista = list(control.controls)
                if control.appbar is not None:
                    controles_vista.insert(0, control.appbar)
                control = ft.Column(controls=controles_vista, expand=True)
            contenido.content = control
            page.update()

        menu = ft.Column(
            controls=[
                ft.Text(
                    "GAVAD",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=CREMA,
                ),
                ft.Text(
                    f"Bienvenido, {usuario_actual.nombres}",
                    color=CREMA,
                ),
                *[
                    ft.Button(
                        nombre,
                        icon=icono,
                        icon_color=VERDE,
                        color=VERDE,
                        bgcolor=CREMA,
                        width=170,
                        on_click=lambda e, vista=vista: cargar_vista(vista),
                    )
                    for nombre, icono, vista in vistas
                ],
                ft.TextButton(
                    "Cerrar sesión",
                    on_click=lambda e: mostrar_login(page, mostrar_sistema),
                    style=ft.ButtonStyle(color=CREMA),
                ),
            ],
            width=190,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

        page.add(
            ft.Row(
                controls=[
                    ft.Container(content=menu, bgcolor=VERDE, padding=16),
                    ft.VerticalDivider(width=1, color=VERDE),
                    contenido,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            )
        )
        cargar_vista(mostrar_usuarios)

    mostrar_splash(page, lambda: mostrar_login(page, mostrar_sistema))


if __name__ == "__main__":
    ft.run(main, assets_dir=str(VIDEO_PATH.parent))