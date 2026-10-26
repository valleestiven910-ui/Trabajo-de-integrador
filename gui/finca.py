import flet as ft

from funciones import listar_fincas


def mostrar_fincas(page: ft.Page):

    fincas = listar_fincas()

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID Finca")),
            ft.DataColumn(ft.Text("ID Usuario")),
            ft.DataColumn(ft.Text("Departamento")),
            ft.DataColumn(ft.Text("Ubicación")),
            ft.DataColumn(ft.Text("Nombre de la finca"))
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(finca.id_finca)),
                    ft.DataCell(ft.Text(finca.id_usuario)),
                    ft.DataCell(ft.Text(finca.departamento)),
                    ft.DataCell(ft.Text(finca.ubicación)),
                    ft.DataCell(ft.Text(finca.nombre_finca))
                ]
            ) for finca in fincas
        ]
    )


    return ft.Column(
        controls=[
            ft.Text(
                "Fincas",
                size=28,
                weight=ft.FontWeight.REGULAR
            ),
            tabla
        ]
    )