import flet as ft

from funciones import (
    actualizar_costo,
    eliminar_costo,
    listar_costos,
    registrar_costo_vaca,
)
from gui.detalle_de_venta import mostrar_detalle_vaca
from gui.mensajes import mostrar_mensaje


def mostrar_formulario_costo(vaca, page: ft.Page, al_guardar=None, costo_editar=None):
    descripcion = ft.TextField(
        label="Descripción del costo",
        value=costo_editar.descripcion if costo_editar else "",
    )
    fecha = ft.TextField(
        label="Fecha (YYYY-MM-DD)",
        value=costo_editar.fecha if costo_editar else "",
    )
    precio = ft.TextField(
        label="Precio (C$)",
        hint_text="Ej.: 40,000 o 1250,50",
        value=str(costo_editar.precio) if costo_editar else "",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    def guardar(ev):
        try:
            if costo_editar:
                actualizado = actualizar_costo(
                    costo_editar.id_costos,
                    descripcion.value or "",
                    fecha.value or "",
                    precio.value or "",
                )
                if not actualizado:
                    raise ValueError("No se encontró el costo para actualizar.")
            else:
                registrar_costo_vaca(
                    vaca.id_vaca,
                    descripcion.value or "",
                    fecha.value or "",
                    precio.value or "",
                )
        except ValueError as error:
            mostrar_mensaje(page, str(error))
            return

        page.pop_dialog()
        if al_guardar:
            al_guardar()

    formulario = ft.AlertDialog(
        title=ft.Text("Editar costo" if costo_editar else "Agregar costo"),
        content=ft.Column([descripcion, fecha, precio], tight=True),
        actions=[
            ft.Button("Guardar cambios" if costo_editar else "Guardar", on_click=guardar),
            ft.TextButton("Cancelar", on_click=lambda ev: page.pop_dialog()),
        ],
    )
    page.show_dialog(formulario)


def mostrar_costos_vaca(vaca, page: ft.Page):
    costos = [costo for costo in listar_costos() if costo.id_vaca == vaca.id_vaca]
    filas = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(costo.id_costos))),
                ft.DataCell(ft.Text(costo.descripcion)),
                ft.DataCell(ft.Text(costo.fecha)),
                ft.DataCell(ft.Text(f"C$ {costo.precio:.2f}")),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.TextButton(
                                "Editar",
                                on_click=lambda e, c=costo: editar_costo(c),
                            ),
                            ft.TextButton(
                                "Borrar",
                                on_click=lambda e, c=costo: confirmar_borrado(c),
                            ),
                        ],
                        spacing=0,
                    )
                ),
            ]
        )
        for costo in costos
    ]

    if not filas:
        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("Sin costos registrados")),
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(ft.Text("C$ 0.00")),
                    ft.DataCell(ft.Text("-")),
                ]
            )
        )

    def agregar_costo(e):
        def actualizar_costos():
            page.pop_dialog()
            mostrar_costos_vaca(vaca, page)

        mostrar_formulario_costo(vaca, page, actualizar_costos)

    def editar_costo(costo):
        def actualizar_costos():
            page.pop_dialog()
            mostrar_costos_vaca(vaca, page)

        mostrar_formulario_costo(
            vaca,
            page,
            actualizar_costos,
            costo_editar=costo,
        )

    def confirmar_borrado(costo):
        def borrar(ev):
            eliminado = eliminar_costo(costo.id_costos)
            page.pop_dialog()
            if eliminado:
                page.pop_dialog()
                mostrar_costos_vaca(vaca, page)
            else:
                mostrar_mensaje(page, "No se encontró el costo para borrar.")

        confirmacion = ft.AlertDialog(
            title=ft.Text("Borrar costo"),
            content=ft.Text(f"¿Borrar el costo “{costo.descripcion}”?"),
            actions=[
                ft.Button("Borrar", on_click=borrar),
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            ],
        )
        page.show_dialog(confirmacion)

    def abrir_detalle(e):
        page.pop_dialog()
        mostrar_detalle_vaca(vaca, page)

    dialogo = ft.AlertDialog(
        title=ft.Text(f"Costos de {vaca.nombre_vaca}"),
        content=ft.Column(
            [
                ft.Image(src=vaca.imagen, width=180, height=120, fit=ft.BoxFit.COVER),
                ft.Text(f"Raza: {vaca.raza} | Peso: {vaca.peso:g} kg"),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("Concepto")),
                        ft.DataColumn(ft.Text("Fecha")),
                        ft.DataColumn(ft.Text("Precio")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=filas,
                ),
            ],
            tight=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        actions=[
            ft.TextButton("Nuevo costo", on_click=agregar_costo),
            ft.Button("Detalle de vaca", on_click=abrir_detalle),
            ft.TextButton("Cerrar", on_click=lambda e: cerrar(dialogo, page)),
        ],
    )
    page.show_dialog(dialogo)


def cerrar(dialogo, page):
    page.pop_dialog()
