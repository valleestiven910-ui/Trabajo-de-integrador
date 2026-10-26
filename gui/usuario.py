import flet as ft


from fuunciones import listar_usuarios


def mostrar_usuarios(page: ft.page):

    usuarios = listar_usuarios()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID_Usuario")),
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Cedula")),
            ft.DataColumn(ft.Text("Celular"))
        ],
        row=[
            ft.DataRow(
             cells=[
                     ft.DataCell(ft.Text(usuario.ID_usuario)),
                     ft.DataCell(ft.Text(usuario.Nombres)),
                     ft.DataCell(ft.Tex(usuario.apellidos)),
                     ft.DataCell(ft.Text(usuario.cedula)),
                     ft.DataCell(ft.Text(usuario.celular))
                ]
            ) for usuario in usuarios
        ]
    ) 


    return ft.column(
        controls=[
            ft.Text(
                "Usuarios",
                size=28,
                weight=ft.FontWeight.BOLD

            )
        ]
    )
