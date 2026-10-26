import flet as ft

from funciones import listar_producciones, buscar_vaca


def mostrar_producciones(page: ft.Page):

    producciones = listar_producciones()


    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID de la producción")),
            ft.DataColumn(ft.Text("Nombre de la Vaca")),
            ft.DataColumn(ft.Text("Cantidad (Galones)")),
            ft.DataColumn(ft.Text("Cantidad (Litros)")),
            ft.DataColumn(ft.Text("Fecha"))
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(produccion.id_producción)),
                    ft.DataCell(ft.Text(buscar_vaca(produccion.id_vaca).nombre
                                        if buscar_vaca(produccion.id_vaca) else "Desconocido")),
                    ft.DataCell(ft.Text(produccion.cantidad)),
                    ft.DataCell(ft.Text(produccion.Litros)),
                    ft.DataCell(ft.Text(produccion.fecha))
                ]
            ) for produccion in producciones
        ]
    )

    return ft.column(
        controls=[
            ft.Text(
                "Producción",
                size=28,
                weight=ft.FontWeight.BOLD
            ),
            tabla
        ]
    )

