import flet as ft


from funciones import actualizar_usuario, eliminar_usuario, listar_usuario, registrar_usuario
from gui.mensajes import mostrar_mensaje


def mostrar_usuarios(page: ft.Page):
    tabla_contenedor = ft.Container(expand=True)

    def cargar_tabla():
        filas = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(usuario.id_usuario))),
                    ft.DataCell(ft.Text(usuario.nombres)),
                    ft.DataCell(ft.Text(usuario.apellidos)),
                    ft.DataCell(ft.Text(usuario.cedula)),
                    ft.DataCell(ft.Text(usuario.celular)),
                    ft.DataCell(
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Editar",
                                    on_click=lambda e, u=usuario: editar_usuario(u),
                                ),
                                ft.TextButton(
                                    "Borrar",
                                    on_click=lambda e, u=usuario: confirmar_borrado(u),
                                ),
                            ],
                            spacing=0,
                        )
                    ),
                ]
            )
            for usuario in listar_usuario()
        ]
        tabla_contenedor.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID usuario")),
                ft.DataColumn(ft.Text("Nombres")),
                ft.DataColumn(ft.Text("Apellidos")),
                ft.DataColumn(ft.Text("Cédula")),
                ft.DataColumn(ft.Text("Celular")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )

    def abrir_formulario(e):
        nombres = ft.TextField(label="Nombres")
        apellidos = ft.TextField(label="Apellidos")
        cedula = ft.TextField(label="Cédula")
        celular = ft.TextField(label="Celular")
        contraseña = ft.TextField(label="Contraseña", password=True, can_reveal_password=True)

        def guardar(ev):
            try:
                nuevo_usuario = registrar_usuario(
                    nombre=nombres.value or "",
                    apellidos=apellidos.value or "",
                    cedula=cedula.value or "",
                    celular=celular.value or "",
                    contraseña=contraseña.value or "",
                )
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(
                page, f"Usuario registrado con ID {nuevo_usuario.id_usuario}."
            )

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar usuario"),
            content=ft.Column(
                [nombres, apellidos, cedula, celular, contraseña],
                tight=True,
                height=350,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    def editar_usuario(usuario):
        nombres = ft.TextField(label="Nombres", value=usuario.nombres)
        apellidos = ft.TextField(label="Apellidos", value=usuario.apellidos)
        cedula = ft.TextField(label="Cédula", value=usuario.cedula)
        celular = ft.TextField(label="Celular", value=usuario.celular)
        contraseña = ft.TextField(
            label="Nueva contraseña (opcional)",
            password=True,
            can_reveal_password=True,
        )

        def guardar(ev):
            try:
                actualizado = actualizar_usuario(
                    usuario.id_usuario,
                    nombres.value or "",
                    apellidos.value or "",
                    cedula.value or "",
                    celular.value or "",
                    contraseña.value,
                )
                if not actualizado:
                    raise ValueError("No se encontró el usuario para actualizar.")
            except ValueError as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(page, "Usuario actualizado correctamente.")

        dialogo = ft.AlertDialog(
            title=ft.Text(f"Editar usuario {usuario.id_usuario}"),
            content=ft.Column(
                [nombres, apellidos, cedula, celular, contraseña],
                tight=True,
                height=350,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar cambios", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    def confirmar_borrado(usuario):
        def borrar(ev):
            try:
                eliminado = eliminar_usuario(usuario.id_usuario)
            except ValueError as error:
                page.pop_dialog()
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            if eliminado:
                cargar_tabla()
                mostrar_mensaje(page, "Usuario eliminado correctamente.")
            else:
                mostrar_mensaje(page, "No se encontró el usuario para borrar.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Borrar usuario"),
            content=ft.Text(f"¿Borrar a {usuario.nombres} {usuario.apellidos}?"),
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
                    ft.Text("Usuarios", size=28, weight=ft.FontWeight.BOLD),
                    ft.Button("Registrar usuario", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar(dialogo, page):
    page.pop_dialog()
