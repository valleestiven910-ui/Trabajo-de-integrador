import flet as ft


from funciones import listar_usuario, registrar_usuario


def mostrar_usuarios(page: ft.page):
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
                page.snack_bar = ft.SnackBar(ft.Text(str(error)))
                page.snack_bar.open = True
                page.update()
                return

            dialogo.open = False
            cargar_tabla()
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Usuario registrado con ID {nuevo_usuario.id_usuario}.")
            )
            page.snack_bar.open = True
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar usuario"),
            content=ft.Column(
                [nombres, apellidos, cedula, celular, contraseña],
                tight=True,
                height=350,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.ElevatedButton("Guardar", on_click=guardar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar(dialogo, page)),
            ],
        )
        page.dialog = dialogo
        dialogo.open = True
        page.update()

    cargar_tabla()
    return ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Usuarios", size=28, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Registrar usuario", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar(dialogo, page):
    dialogo.open = False
    page.update()
