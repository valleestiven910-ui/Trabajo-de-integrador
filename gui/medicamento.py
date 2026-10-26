import flet as ft

from funciones import listar_medicamento, buscar_vacas, buscar_finca

def mostrar_vacas(page:ft.Page):

    medicamentos = listar_medicamento()

    filas= []

    tabla= ft.DataTable(
        columns =[
            ft.DataColumn(ft.Text("ID de medicamento")),
            ft.DataColumn(ft.Text("ID de vaca")),
            ft.DataColumn(ft.Text("Remedio")),
            ft.DataColumn(ft.Text("Dosis X/VACAS")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Peso_Anterior_Del_Ganado")),
            ft.DataColumn(ft.Text("Peso_Actual_Del_Ganado")),
            ft.DataColumn(ft.Text("finca")),
        ],        
        rows =[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(medicamento.id_medicamento)),
                    ft.DataCell(ft.Text(buscar_vacas(medicamento.id_vaca).nombre
                                        if buscar_vacas(medicamento.id_vaca) else "Desconocido")),
                    ft.DataCell(ft.Text(medicamento.remedio)),
                    ft.DataCell(ft.Text(medicamento.dosis_por_vacas)),
                    ft.DataCell(ft.Text(medicamento.peso_anterior_de_la_vaca)),
                    ft.DataCell(ft.Text(medicamento.peso_actual_de_la_vaca)),
                    ft.DataCell(ft.Text(buscar_finca(medicamento.id_finca).nombre
                                        if buscar_finca(medicamento.id_finca) else "Desconocido"))


                ]
            ) for medicamento in medicamentos
        ]
    )

    return ft.Column(
        controls=[
            ft.Text(
                "Medicamentos",
                size=28,
                weight=ft.FontWeight.BOLD
            ),
            tabla
        ]
    )