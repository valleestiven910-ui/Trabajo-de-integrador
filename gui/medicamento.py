import flet as ft

from funciones import (
    actualizar_medicamento,
    buscar_vaca,
    eliminar_medicamento,
    listar_medicamento,
    listar_vacas,
    registrar_medicamento,
)
from gui.mensajes import mostrar_mensaje


def mostrar_medicamento(page: ft.Page):
    tabla_contenedor = ft.Container(expand=True)

    def cargar_tabla():
        tabla_contenedor.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Vaca")),
                ft.DataColumn(ft.Text("Remedio")),
                ft.DataColumn(ft.Text("Dosis")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Peso anterior")),
                ft.DataColumn(ft.Text("Peso actual")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(registro.id_medicamento))),
                        ft.DataCell(
                            ft.Text(
                                vaca.nombre_vaca if (vaca := buscar_vaca(registro.id_vaca))
                                else "Desconocida"
                            )
                        ),
                        ft.DataCell(ft.Text(registro.remedio)),
                        ft.DataCell(ft.Text(registro.dosis_por_vacas)),
                        ft.DataCell(ft.Text(registro.fecha)),
                        ft.DataCell(ft.Text(str(registro.peso_anterior_de_la_vaca))),
                        ft.DataCell(ft.Text(str(registro.peso_actual_de_la_vaca))),
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
                for registro in listar_medicamento()
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
        remedio = ft.TextField(label="Remedio")
        dosis = ft.TextField(label="Dosis")
        fecha = ft.TextField(label="Fecha (por ejemplo, 2026-10-31)")
        peso_anterior = ft.TextField(
            label="Peso anterior (kg)", keyboard_type=ft.KeyboardType.NUMBER
        )
        peso_actual = ft.TextField(
            label="Peso actual (kg)", keyboard_type=ft.KeyboardType.NUMBER
        )

        def guardar(ev):
            try:
                registro = registrar_medicamento(
                    id_vaca=vaca_seleccionada.value,
                    remedio=remedio.value,
                    dosis_por_vacas=dosis.value,
                    fecha=fecha.value,
                    peso_anterior_de_la_vaca=peso_anterior.value,
                    peso_actual_de_la_vaca=peso_actual.value,
                )
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(page, f"Medicamento registrado con ID {registro.id_medicamento}.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar medicamento"),
            content=ft.Column(
                [
                    vaca_seleccionada,
                    remedio,
                    dosis,
                    fecha,
                    peso_anterior,
                    peso_actual,
                ],
                tight=True,
                height=420,
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
        remedio = ft.TextField(label="Remedio", value=registro.remedio)
        dosis = ft.TextField(label="Dosis", value=registro.dosis_por_vacas)
        fecha = ft.TextField(label="Fecha", value=registro.fecha)
        peso_anterior = ft.TextField(
            label="Peso anterior (kg)",
            value=str(registro.peso_anterior_de_la_vaca),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        peso_actual = ft.TextField(
            label="Peso actual (kg)",
            value=str(registro.peso_actual_de_la_vaca),
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        def guardar(ev):
            try:
                actualizado = actualizar_medicamento(
                    registro.id_medicamento,
                    vaca_seleccionada.value or "",
                    remedio.value or "",
                    fecha.value or "",
                    peso_anterior.value or "",
                    peso_actual.value or "",
                    dosis.value or "",
                )
                if not actualizado:
                    raise ValueError("No se encontró el medicamento para actualizar.")
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(page, "Registro de medicamento actualizado.")

        dialogo = ft.AlertDialog(
            title=ft.Text(f"Editar medicamento {registro.id_medicamento}"),
            content=ft.Column(
                [vaca_seleccionada, remedio, dosis, fecha, peso_anterior, peso_actual],
                tight=True,
                height=420,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar cambios", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar_dialogo(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    def confirmar_borrado(registro):
        def borrar(ev):
            eliminado = eliminar_medicamento(registro.id_medicamento)
            page.pop_dialog()
            if eliminado:
                cargar_tabla()
                mostrar_mensaje(page, "Registro de medicamento eliminado.")
            else:
                mostrar_mensaje(page, "No se encontró el registro para borrar.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Borrar medicamento"),
            content=ft.Text(f"¿Borrar el registro {registro.id_medicamento}?"),
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
                    ft.Text("Medicamentos", size=28, weight=ft.FontWeight.BOLD),
                    ft.Button("Registrar medicamento", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar_dialogo(dialogo, page):
    page.pop_dialog()
