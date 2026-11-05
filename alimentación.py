import flet as ft

from funciones import (
    buscar_vaca,
    actualizar_alimentación,
    eliminar_alimentación,
    listar_alimentación,
    listar_vacas,
    registrar_alimentación,
)
from gui.mensajes import mostrar_mensaje


def vista_alimentación(page: ft.Page):
    tabla_general = ft.Container()
    tabla_individual = ft.Container()
    seccion_general = ft.Column(
        [
            ft.Text("Alimentación general", size=18, weight=ft.FontWeight.BOLD),
            tabla_general,
        ]
    )
    seccion_individual = ft.Column(
        [
            ft.Text("Alimentación individual", size=18, weight=ft.FontWeight.BOLD),
            tabla_individual,
        ],
        visible=False,
    )

    def cargar_tablas():
        alimentos = listar_alimentación()
        tabla_general.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Cantidad (libras)")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Costo")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(alimento.id_alimentacion))),
                        ft.DataCell(ft.Text(alimento.tipo_de_alimento)),
                        ft.DataCell(ft.Text(alimento.descripción)),
                        ft.DataCell(ft.Text(str(alimento.cantidad))),
                        ft.DataCell(ft.Text(alimento.fecha)),
                        ft.DataCell(ft.Text(f"C$ {alimento.costo_alimento:.2f}")),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Editar",
                                        on_click=lambda e, a=alimento: editar_registro(a),
                                    ),
                                    ft.TextButton(
                                        "Borrar",
                                        on_click=lambda e, a=alimento: confirmar_borrado(a),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
                for alimento in alimentos
                if alimento.id_vaca is None
            ],
        )
        tabla_individual.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Cantidad (libras)")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Costo")),
                ft.DataColumn(ft.Text("Vaca")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(alimento.id_alimentacion))),
                        ft.DataCell(ft.Text(alimento.tipo_de_alimento)),
                        ft.DataCell(ft.Text(alimento.descripción)),
                        ft.DataCell(ft.Text(str(alimento.cantidad))),
                        ft.DataCell(ft.Text(alimento.fecha)),
                        ft.DataCell(ft.Text(f"C$ {alimento.costo_alimento:.2f}")),
                        ft.DataCell(
                            ft.Text(
                                vaca.nombre_vaca
                                if (vaca := buscar_vaca(alimento.id_vaca))
                                else "Desconocida"
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Editar",
                                        on_click=lambda e, a=alimento: editar_registro(a),
                                    ),
                                    ft.TextButton(
                                        "Borrar",
                                        on_click=lambda e, a=alimento: confirmar_borrado(a),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
                for alimento in alimentos
                if alimento.id_vaca is not None
            ],
        )

    def abrir_formulario(e):
        tipo = ft.TextField(label="Tipo de alimento")
        descripcion = ft.TextField(label="Descripción", multiline=True, min_lines=1, max_lines=3)
        cantidad = ft.TextField(
            label="Cantidad (libras)", keyboard_type=ft.KeyboardType.NUMBER
        )
        fecha = ft.TextField(label="Fecha (por ejemplo, 2026-10-31)")
        costo = ft.TextField(
            label="Costo (C$)", keyboard_type=ft.KeyboardType.NUMBER, value="0"
        )
        asignacion = ft.Dropdown(
            label="Aplicar a",
            value="general",
            options=[
                ft.dropdown.Option(key="general", text="Alimentación general"),
                *[
                    ft.dropdown.Option(
                        key=str(vaca.id_vaca),
                        text=f"{vaca.nombre_vaca} (ID {vaca.id_vaca})",
                    )
                    for vaca in listar_vacas()
                ],
            ],
        )

        def guardar(ev):
            try:
                registro = registrar_alimentación(
                    tipo_de_alimento=tipo.value,
                    descripción=descripcion.value,
                    cantidad=cantidad.value,
                    fecha=fecha.value,
                    costo_alimento=costo.value,
                    id_vaca=(
                        None
                        if asignacion.value == "general"
                        else asignacion.value
                    ),
                )
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tablas()
            mostrar_mensaje(
                page, f"Alimentación registrada con ID {registro.id_alimentacion}."
            )

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar alimentación"),
            content=ft.Column(
                [tipo, descripcion, cantidad, fecha, costo, asignacion],
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

    def editar_registro(alimento):
        tipo = ft.TextField(label="Tipo de alimento", value=alimento.tipo_de_alimento)
        descripcion = ft.TextField(
            label="Descripción",
            value=alimento.descripción,
            multiline=True,
            min_lines=1,
            max_lines=3,
        )
        cantidad = ft.TextField(
            label="Cantidad (libras)",
            value=str(alimento.cantidad),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        fecha = ft.TextField(label="Fecha", value=alimento.fecha)
        costo = ft.TextField(
            label="Costo (C$)",
            value=str(alimento.costo_alimento),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        asignacion = ft.Dropdown(
            label="Aplicar a",
            value=(
                "general"
                if alimento.id_vaca is None
                else str(alimento.id_vaca)
            ),
            options=[
                ft.dropdown.Option(key="general", text="Alimentación general"),
                *[
                    ft.dropdown.Option(
                        key=str(vaca.id_vaca),
                        text=f"{vaca.nombre_vaca} (arete {vaca.id_vaca})",
                    )
                    for vaca in listar_vacas()
                ],
            ],
        )

        def guardar(ev):
            try:
                actualizado = actualizar_alimentación(
                    alimento.id_alimentacion,
                    tipo.value or "",
                    descripcion.value or "",
                    cantidad.value or "",
                    fecha.value or "",
                    costo.value or "",
                    None if asignacion.value == "general" else asignacion.value,
                )
                if not actualizado:
                    raise ValueError("No se encontró el registro para actualizar.")
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tablas()
            mostrar_mensaje(page, "Registro de alimentación actualizado.")

        dialogo = ft.AlertDialog(
            title=ft.Text(f"Editar alimentación {alimento.id_alimentacion}"),
            content=ft.Column(
                [tipo, descripcion, cantidad, fecha, costo, asignacion],
                tight=True,
                height=420,
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

    def confirmar_borrado(alimento):
        def borrar(ev):
            eliminado = eliminar_alimentación(alimento.id_alimentacion)
            page.pop_dialog()
            if eliminado:
                cargar_tablas()
                mostrar_mensaje(page, "Registro de alimentación eliminado.")
            else:
                mostrar_mensaje(page, "No se encontró el registro para borrar.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Borrar alimentación"),
            content=ft.Text(f"¿Borrar el registro {alimento.id_alimentacion}?"),
            actions=[
                ft.Button("Borrar", on_click=borrar),
                ft.TextButton(
                    "Cancelar", on_click=lambda ev: cerrar_dialogo(dialogo, page)
                ),
            ],
        )
        page.show_dialog(dialogo)

    def cambiar_vista(e):
        es_general = selector_tipo.value == "general"
        seccion_general.visible = es_general
        seccion_individual.visible = not es_general
        page.update()

    selector_tipo = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(value="general", label="General"),
                ft.Radio(value="individual", label="Individual"),
            ]
        ),
        value="general",
        on_change=cambiar_vista,
    )
    cargar_tablas()

    return ft.View(
        route="/alimentación",
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Alimentación", size=28, weight=ft.FontWeight.BOLD
                                ),
                                ft.Button(
                                    "Registrar alimentación",
                                    on_click=abrir_formulario,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text("Tipo de registro", size=16, weight=ft.FontWeight.BOLD),
                        selector_tipo,
                        ft.Divider(height=20),
                        seccion_general,
                        seccion_individual,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=20,
                expand=True,
            )
        ],
    )


def cerrar_dialogo(dialogo, page):
    page.pop_dialog()
