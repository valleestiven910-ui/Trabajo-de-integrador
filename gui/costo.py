import flet as ft
from funciones import listar_vacas_en_catalogo, listar_vaca, listar_costo



def ver_costo_vaca(vaca, page: ft.Page):

    todos_los_costos = listar_costo() if 'listar_costos' in globals() else []
    costo_vaca= [c for c in todos_los_costos if c.id_vaca ==vaca.id_vaca]


    detalles_elementos = []
    total_precio = 0

    if not costo_vaca:
        detalles_elementos.append(ft.Text("No hay registros de costos para esta vaca.", italic=True))
    else:
        for c in costo_vaca:
            total_precio += c.precio
            detalles_elementos.append(
                ft.Container(
                    content= ft.Column([
                        ft.Text(f"ID Vaca: {c.id_vaca}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"Descripcióm: {c.descripción}"),
                        ft.Text(f"Fecha:{c.fecha}"),
                        ft.Text(f"Precio: ${c.precio:.2f}", color=ft.colors.GREEN, weight=ft.FontWeight.BOLD),


                    ]),
                    padding=10,
                    border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
                    border_radius=ft.border_radius.all(8),
                    margin= ft.margin.only(bottom=10)
                )
            )
    def realizar_compra(e):
        page.sanck_bar = ft.SnackBar(ft.Text(f"¡Has iniciado el proceso de compra para {vaca.nombre_vaca}!"))
        page.snack_bar.open=True
        dlg_costo.open=False
        page.update()


    dlg_costos =ft.AlertDialog(
        title=ft.Text(f"Detalles de Costos: {vaca.nombre_vaca}"),
        content=ft.Column([
            ft.Image(src=vaca.imagen, width=100, height=100, fit=ft.ImageFit.COVER),
            ft.Divider(),
            ft.Text("Historial de Inversión y Precios:", weight=ft.FontWeight.BOLD)
            ft.Column(detalles_elementos, scroll=ft.ScrollMode.AUTO, height=180)
        ], tight=True, width=350),
        actions=[
            ft.ElevatedButton("Comprar Vaca", icon=ft.icons.SHOPPING_CART, bgcolor = ft.color.GREEN, color=ft.colors.WHITE, 
                              on_click=realizar_compra),
            ft.TextButton("Cerrar", on_click=lambda e: (setattr(dlg_costos, 'open', False), page.update()))                  
        ]
    )
    page.dialog = dlg_costos
    dlg_costos.open = True
    page.update()

