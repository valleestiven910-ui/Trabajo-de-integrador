import flet as ft
from funciones import listar_vacas_en_catalogo, listar_costos

def ver_costo_vaca(vaca, page:ft.Page):
    todos_los_costos = listar_costos() if 'listar_costos' in globals() else []
    costos_vaca = [c for c in todos_los_costos if c.id_vaca==vaca.id_vaca]


    detalles_elementos = []

    if not costos_vaca :
        detalles_elementos.append(ft.Text("No hay registros de costos para esta vaca.", italic=True))
    else:
        for c in costos_vaca:
            detalles_elementos.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"ID vaca: {c.id_vaca}",  weight= ft.FontWeight.BOLD),
                        ft.Text(f"Descripción: {c.decripción}"),
                        ft.Tex(f"Fecha:{c.fecha}"),
                        ft.Text(f"Precio: C${c.precio:.2f}", color=ft.colors.GREEN, weight=ft.FontWeight.BOLD),
                    ]),
                    padding=10,
                    border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
                    border_radius= ft.border_radius.all(8),
                    margin=ft.margin.only(bottom=10),
                )
            )
        def realizar_compra(e):
            page.snack_bar = ft.SnackBar(ft.Text(f"¡Iniciando compra para {vaca.nombre_vaca}!"))
            page.snack_bar.open = True
            dlg_costos.open = False
            page.update()

        dlg_costos = ft.AlertDialog(
            title=ft.Text(f"Costo de vaca:{vaca.nombre_vaca}"),
            content=ft.Column([
                ft.Column(detalles_elementos, scroll= ft.ScrollMode.AUTO, height=200)
            ], tight=True, width= 350), 
            actions=[
                 ft.ElevatedButton("Comprar Vaca", icon=ft.icons.SHOPPING_CART, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, on_click=realizar_compra),
                    ft.TextButton("Cerrar", on_click=lambda e: (setattr(dlg_costos, 'open', False), page.update()))
            ]
        )
    page.dialog = dlg_costos
    dlg_costos.open = True
    page.update

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



