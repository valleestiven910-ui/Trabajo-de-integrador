import flet as ft

from funciones import listar_vacas, buscar_usuario



def mostrar_vacas(page: ft.Page):

    vacas = listar_vacas()

    filas = []

    tabla = ft.DataTable(
        columns =[
            ft.DataColumn(ft.Text("ID de Vaca")),
            ft.DataColumn(ft.Text("ID de usuario")),
            ft.DataColumn(ft.Text("ID de Finca")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Raza")),
            ft.DataColumn(ft.Text("Color")),
            ft.DataColumn(ft.Text("Peso"))
        ],
        rows =[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(vaca.id_vaca)),
                    ft.DataCell(ft.Text(vaca.id_usuario)),
                    ft.DataCell(ft.Text(vaca.id_finca)),
                    ft.DataCell(ft.Text(vaca.nombre_vaca)),
                    ft.DataCell(ft.Text(vaca.raza)),
                    ft.DataCell(ft.Text(vaca.color)),
                    ft.DataCell(ft.Text(vaca.peso)),
                    ft.DataCell(ft.Text(buscar_usuario(vaca.usuario_id).nombre
                                        if buscar_usuario(vaca.usuario_id) else "Desconocido"))
                ]
            ) for vaca in vacas
        ]
    )

    return ft.Column(
        controls=[
            ft.Text(
                "Vacas",
                size=28,
                weight=ft.FontWeight.BOLD
            ),
            tabla
        ]
    )