import flet as ft

from funciones import buscar_usuario, listar_fincas, listar_usuario, registrar_finca


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
            ],
            rows=filas,
        )

    def abrir_formulario(e):
        usuarios = listar_usuario()
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
                page.snack_bar = ft.SnackBar(ft.Text(str(error)))
                page.snack_bar.open = True
                page.update()
                return

            dialogo.open = False
            cargar_tabla()
            usuario_dueño = buscar_usuario(nueva_finca.id_usuario)
            nombre_dueño = f"{usuario_dueño.nombres} {usuario_dueño.apellidos}"
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Finca registrada para {nombre_dueño}.")
            )
            page.snack_bar.open = True
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar finca"),
            content=ft.Column(
                [dueño, departamento, ubicacion, nombre],
                tight=True,
                height=300,
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
                    ft.Text("Fincas", size=28, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Registrar finca", on_click=abrir_formulario),
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