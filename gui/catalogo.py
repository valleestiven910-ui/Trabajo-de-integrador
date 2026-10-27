import flet as ft
from funciones import listar_vacas_en_catalogo



def mostrar_catalogo(page: ft.Page):
    vacas_catalogo = listar_vacas_en_catalogo()


    tarjetas= []

    if not vacas_catalogo:
        tarjetas.append(ft.Text("No hay vacas publicadas en el catálogo todavía.", size=16, italic=True))

    else:
        for vaca in vacas_catalogo:
            tarjeta= ft.Container(
                content=ft.Column([

                    ft.Image(
                        src=vaca.imagen if vaca.imagen else "https://via.placeholder.com/150",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.COVER,
                        border_radius=ft.border_radius.all(10),
                    ),
                    ft.Text(vaca.nombre_vaca, weight=ft.FontWeight.BOLD, size=16),
                    ft.Text(f"Raza: {vaca.raza}", size=12),
                    ft.Text(f"Peso:{vaca.peso} Kg", size=12),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius=ft.border_radius.all(10),
                bgcolor=ft.colors.SURFACE_VARIAT,
                on_click= lambda e, v=vaca: ver_costo_vaca(v,page)
            )
            tarjetas.append(tarjeta)


    grid_vacas = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=200,
        child_aspect_ratio=0.8,
        spacing=10,
        run_spacing=10,
        controls=tarjetas
    )

    return ft.View(
        "/catalogo",
        [
            ft.Column([
                ft.Text("Vacas en ventas", size=30, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Container(content=grid_vacas, expand=True, padding=10)
            ], padding=20, expand=True)
        ]
    )



