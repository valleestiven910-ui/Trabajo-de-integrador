import flet as ft

from funciones import (
    actualizar_producción,
    buscar_vaca,
    eliminar_producción,
    listar_producciones,
    listar_vacas,
    registrar_producción,
)
from gui.mensajes import mostrar_mensaje


def mostrar_producciones(page: ft.Page):
    tabla_contenedor = ft.Container(expand=True)

    def cargar_tabla():
        tabla_contenedor.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Vaca")),
                ft.DataColumn(ft.Text("Cantidad (galones)")),
                ft.DataColumn(ft.Text("Cantidad (litros)")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(registro.id_producción))),
                        ft.DataCell(
                            ft.Text(
                                vaca.nombre_vaca if (vaca := buscar_vaca(registro.id_vaca))
                                else "Desconocida"
                            )
                        ),
                        ft.DataCell(ft.Text(str(registro.cantidad))),
                        ft.DataCell(ft.Text(str(registro.Litros))),
                        ft.DataCell(ft.Text(registro.fecha)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Editar",
                                        on_click=lambda e, r=registro: editar_registro(r),
                                    ),
                                    ft.TextButton(
                                        "Borrar",
                                        on_click=lambda e, r=registro: confirmar_borrado(r),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
                for registro in listar_producciones()
            ],
        )

    def abrir_formulario(e):
        vaca_seleccionada = ft.Dropdown(
            label="Vaca",
            options=[
                ft.dropdown.Option(
                    key=str(vaca.id_vaca),
                    text=f"{vaca.nombre_vaca} (ID {vaca.id_vaca})",
                )
                for vaca in listar_vacas()
            ],
        )
        cantidad = ft.TextField(
            label="Cantidad (galones)", keyboard_type=ft.KeyboardType.NUMBER
        )
        litros = ft.TextField(
            label="Cantidad (litros)", keyboard_type=ft.KeyboardType.NUMBER
        )
        fecha = ft.TextField(label="Fecha (por ejemplo, 2026-10-31)")

        def guardar(ev):
            try:
                registro = registrar_producción(
                    id_vaca=vaca_seleccionada.value,
                    cantidad=cantidad.value,
                    Litros=litros.value,
                    fecha=fecha.value,
                )
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(page, f"Producción registrada con ID {registro.id_producción}.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar producción"),
            content=ft.Column(
                [vaca_seleccionada, cantidad, litros, fecha],
                tight=True,
                height=300,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar", on_click=guardar),
                ft.TextButton(
                    "Cancelar", on_click=lambda ev: cerrar_dialogo(dialogo, page)
                ),
            ],
        )
        page.show_dialog(dialogo)

    def editar_registro(registro):
        vaca_seleccionada = ft.Dropdown(
            label="Vaca",
            value=str(registro.id_vaca),
            options=[
                ft.dropdown.Option(
                    key=str(vaca.id_vaca),
                    text=f"{vaca.nombre_vaca} (arete {vaca.id_vaca})",
                )
                for vaca in listar_vacas()
            ],
        )
        cantidad = ft.TextField(
            label="Cantidad (galones)",
            value=str(registro.cantidad),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        litros = ft.TextField(
            label="Cantidad (litros)",
            value=str(registro.Litros),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        fecha = ft.TextField(label="Fecha", value=registro.fecha)

        def guardar(ev):
            try:
                actualizado = actualizar_producción(
                    registro.id_producción,
                    vaca_seleccionada.value or "",
                    cantidad.value or "",
                    litros.value or "",
                    fecha.value or "",
                )
                if not actualizado:
                    raise ValueError("No se encontró la producción para actualizar.")
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(page, "Registro de producción actualizado.")

        dialogo = ft.AlertDialog(
            title=ft.Text(f"Editar producción {registro.id_producción}"),
            content=ft.Column(
                [vaca_seleccionada, cantidad, litros, fecha],
                tight=True,
                height=300,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar cambios", on_click=guardar),
                ft.TextButton(
                    "Cancelar", on_click=lambda ev: cerrar_dialogo(dialogo, page)
                ),
            ],
        )
        page.show_dialog(dialogo)

    def confirmar_borrado(registro):
        def borrar(ev):
            eliminado = eliminar_producción(registro.id_producción)
            page.pop_dialog()
            if eliminado:
                cargar_tabla()
                mostrar_mensaje(page, "Registro de producción eliminado.")
            else:
                mostrar_mensaje(page, "No se encontró el registro para borrar.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Borrar producción"),
            content=ft.Text(f"¿Borrar el registro {registro.id_producción}?"),
            actions=[
                ft.Button("Borrar", on_click=borrar),
                ft.TextButton(
                    "Cancelar", on_click=lambda ev: cerrar_dialogo(dialogo, page)
                ),
            ],
        )
        page.show_dialog(dialogo)

    cargar_tabla()
    return ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Producción", size=28, weight=ft.FontWeight.BOLD),
                    ft.Button("Registrar producción", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar_dialogo(dialogo, page):
    page.pop_dialog()
