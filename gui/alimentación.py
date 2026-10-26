import flet as ft
from funciones import listar_alimentación, buscar_vacas


def vista_alimentación(page: ft.Page):
    alimentaciones= listar_alimentación()


    tabla_general= ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID de alinmentación")),
            ft.DataColumn(ft.Text("Tipos de Alimentos")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Cantidad (Libras)")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Costo Del Alimento")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(alimento.id_alimentacion)),
                    ft.DataCell(ft.Text(alimento.tipo_de_alimento)),
                    ft.DataCell(ft.Text(alimento.descripción)),
                    ft.DataCell(ft.Text(alimento.cantidad)),
                    ft.DataCell(ft.Text(alimento.fecha)),
                    ft.DataCell(ft.Text(alimento.costo_alimento))
                ]
            ) for alimento in alimentaciones if alimento.id_vaca is None
        ]
    )
    seccion_general = ft.Column([
            ft.Text ("Alimentación General", 
                    size=18, 
                    weight=ft.FontWeight.BOLD),
                    tabla_general,
        ])

    
    tabla_individual= ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID de alinmentación")),
                        ft.DataColumn(ft.Text("Tipos de Alimentos")),
                        ft.DataColumn(ft.Text("Descripción")),
                        ft.DataColumn(ft.Text("Cantidad (Libras)")),
                        ft.DataColumn(ft.Text("Fecha")),
                        ft.DataColumn(ft.Text("Costo Del Alimento")),
                        ft.DataColumn(ft.Text("Nombre de la vaca"))
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(alimento.id_alimentacion)),
                                ft.DataCell(ft.Text(alimento.tipo_de_alimento)),
                                ft.DataCell(ft.Text(alimento.descripción)),
                                ft.DataCell(ft.Text(alimento.cantidad)),
                                ft.DataCell(ft.Text(alimento.fecha)),
                                ft.DataCell(ft.Text(alimento.costo_alimento)),
                                ft.DataCell(ft.Text(buscar_vacas(alimento.id_vaca).nombre
                                                    if buscar_vacas(alimento.id_vaca)else "Desconocido"))
                            ]
                        ) for alimento in alimentaciones if alimento.id_vaca is not None
                    ]
                )
            
    
    seccion_individual = ft.Column([
        ft.Text("Alimentación Individual", 
                size=18, 
                weight=ft.FontWeight),
                tabla_individual,
    ], visible= False)

    def cambiar_vista(e):
        if selector_tipo.value == "general":
            seccion_general.visible =True
            seccion_individual.visible = False
        else:
            seccion_general.visible = False
            seccion_individual.visible = True
        page.update()


    selector_tipo = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="general",label="General"),
            ft.Radio(value="individual", label="Individual"),
        ]),
        value="general",
        on_change=cambiar_vista
    )

    return ft.view(
        "/alimentación",
        [
            ft.Column(
                [
                    ft.Text("Tipo de Registro", size=16, weight=ft.FontWeight.BOLD),
                    selector_tipo,
                    ft.Divider(height=20),

                    seccion_general,
                    seccion_individual,
                ],
                padding=20,
                scroll=ft.ScrollMode.AUTO
            )
        ]
    )