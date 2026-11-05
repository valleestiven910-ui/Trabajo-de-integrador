import flet as ft

from funciones import (
    actualizar_finca,
    buscar_usuario,
    eliminar_finca,
    listar_fincas,
    listar_usuario,
    registrar_finca,
)
from gui.mensajes import mostrar_mensaje


def mostrar_fincas(page: ft.Page):
    tabla_contenedor = ft.Container(expand=True)

    def cargar_tabla():
        filas = []
        for finca in listar_fincas():
            dueño = buscar_usuario(finca.id_usuario)
            nombre_dueño = (
                f"{dueño.nombres} {dueño.apellidos} (ID {dueño.id_usuario})"
                if dueño
                else f"Usuario {finca.id_usuario} no encontrado"
            )
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(finca.id_finca))),
                        ft.DataCell(ft.Text(nombre_dueño)),
                        ft.DataCell(ft.Text(finca.departamento)),
                        ft.DataCell(ft.Text(finca.ubicación)),
                        ft.DataCell(ft.Text(finca.nombre_finca)),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Editar",
                                        on_click=lambda e, f=finca: editar_finca(f),
                                    ),
                                    ft.TextButton(
                                        "Borrar",
                                        on_click=lambda e, f=finca: confirmar_borrado(f),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
            )

        tabla_contenedor.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID finca")),
                ft.DataColumn(ft.Text("Usuario dueño")),
                ft.DataColumn(ft.Text("Departamento")),
                ft.DataColumn(ft.Text("Ubicación")),
                ft.DataColumn(ft.Text("Nombre de finca")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )

    def abrir_formulario(e):
        usuarios = listar_usuario()
        if not usuarios:
            mostrar_mensaje(page, "Registra primero un usuario para asignarle la finca.")
            return

        dueño = ft.Dropdown(
            label="Usuario dueño",
            options=[
                ft.dropdown.Option(
                    key=str(usuario.id_usuario),
                    text=f"{usuario.nombres} {usuario.apellidos} (ID {usuario.id_usuario})",
                )
                for usuario in usuarios
            ],
        )
        departamento = ft.TextField(label="Departamento")
        ubicacion = ft.TextField(label="Ubicación")
        nombre = ft.TextField(label="Nombre de la finca")

        def guardar(ev):
            try:
                nueva_finca = registrar_finca(
                    id_usuario=dueño.value,
                    departamento=departamento.value or "",
                    ubicacion=ubicacion.value or "",
                    nombre_finca=nombre.value or "",
                )
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            usuario_dueño = buscar_usuario(nueva_finca.id_usuario)
            nombre_dueño = f"{usuario_dueño.nombres} {usuario_dueño.apellidos}"
            mostrar_mensaje(page, f"Finca registrada para {nombre_dueño}.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar finca"),
            content=ft.Column(
                [dueño, departamento, ubicacion, nombre],
                tight=True,
                height=300,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    def editar_finca(finca):
        usuarios = listar_usuario()
        dueño = ft.Dropdown(
            label="Usuario dueño",
            value=str(finca.id_usuario),
            options=[
                ft.dropdown.Option(
                    key=str(usuario.id_usuario),
                    text=f"{usuario.nombres} {usuario.apellidos} (ID {usuario.id_usuario})",
                )
                for usuario in usuarios
            ],
        )
        departamento = ft.TextField(label="Departamento", value=finca.departamento)
        ubicacion = ft.TextField(label="Ubicación", value=finca.ubicación)
        nombre = ft.TextField(label="Nombre de la finca", value=finca.nombre_finca)

        def guardar(ev):
            try:
                actualizado = actualizar_finca(
                    finca.id_finca,
                    dueño.value or "",
                    departamento.value or "",
                    ubicacion.value or "",
                    nombre.value or "",
                )
                if not actualizado:
                    raise ValueError("No se encontró la finca para actualizar.")
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(page, "Finca actualizada correctamente.")

        dialogo = ft.AlertDialog(
            title=ft.Text(f"Editar finca {finca.id_finca}"),
            content=ft.Column(
                [dueño, departamento, ubicacion, nombre],
                tight=True,
                height=300,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar cambios", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    def confirmar_borrado(finca):
        def borrar(ev):
            try:
                eliminado = eliminar_finca(finca.id_finca)
            except ValueError as error:
                page.pop_dialog()
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            if eliminado:
                cargar_tabla()
                mostrar_mensaje(page, "Finca eliminada correctamente.")
            else:
                mostrar_mensaje(page, "No se encontró la finca para borrar.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Borrar finca"),
            content=ft.Text(f"¿Borrar la finca {finca.nombre_finca}?"),
            actions=[
                ft.Button("Borrar", on_click=borrar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    cargar_tabla()
    return ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Fincas", size=28, weight=ft.FontWeight.BOLD),
                    ft.Button("Registrar finca", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar(dialogo, page):
    page.pop_dialog()