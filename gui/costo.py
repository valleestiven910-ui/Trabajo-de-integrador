import flet as ft

from funciones import listar_costos, registrar_costo_vaca
from gui.detalle_de_venta import mostrar_detalle_vaca


def mostrar_costos_vaca(vaca, page: ft.Page):
    costos = [costo for costo in listar_costos() if costo.id_vaca == vaca.id_vaca]
    filas = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(costo.descripcion)),
                ft.DataCell(ft.Text(costo.fecha)),
                ft.DataCell(ft.Text(f"C$ {costo.precio:.2f}")),
            ]
        )
        for costo in costos
    ]

    if not filas:
        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Sin costos registrados")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("C$ 0.00")),
                ]
            )
        )

    def agregar_costo(e):
        descripcion = ft.TextField(label="Descripción del costo")
        fecha = ft.TextField(label="Fecha (YYYY-MM-DD)")
        precio = ft.TextField(label="Precio (C$)", keyboard_type=ft.KeyboardType.NUMBER)

        def guardar(ev):
            try:
                registrar_costo_vaca(
                    vaca.id_vaca,
                    descripcion.value or "",
                    fecha.value or "",
                    precio.value or "",
                )
            except ValueError as error:
                page.snack_bar = ft.SnackBar(ft.Text(str(error)))
                page.snack_bar.open = True
                page.update()
                return

            formulario.open = False
            page.update()
            mostrar_costos_vaca(vaca, page)

        formulario = ft.AlertDialog(
            title=ft.Text("Agregar costo"),
            content=ft.Column([descripcion, fecha, precio], tight=True),
            actions=[
                ft.ElevatedButton("Guardar", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(formulario, page)),
            ],
        )
        page.dialog = formulario
        formulario.open = True
        page.update()

    def abrir_detalle(e):
        dialogo.open = False
        page.update()
        mostrar_detalle_vaca(vaca, page)

    dialogo = ft.AlertDialog(
        title=ft.Text(f"Costos de {vaca.nombre_vaca}"),
        content=ft.Column(
            [
                ft.Image(src=vaca.imagen, width=180, height=120, fit=ft.ImageFit.COVER),
                ft.Text(f"Raza: {vaca.raza} | Peso: {vaca.peso} kg"),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Concepto")),
                        ft.DataColumn(ft.Text("Fecha")),
                        ft.DataColumn(ft.Text("Precio")),
                    ],
                    rows=filas,
                ),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("Nuevo costo", on_click=agregar_costo),
            ft.ElevatedButton("Detalle de vaca", on_click=abrir_detalle),
            ft.TextButton("Cerrar", on_click=lambda e: cerrar(dialogo, page)),
        ],
    )
    page.dialog = dialogo
    dialogo.open = True
    page.update()


def cerrar(dialogo, page):
    dialogo.open = False
    page.update()
