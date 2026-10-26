import flet as ft
from funciones import listar_alimentación, buscar_usuario


def vista_alimentación(page: ft.Page):
    alimentaciones= listar_alimentación()


    seccion_general = ft.Column([
        ft.Text ("Alimentación General", 
                 size=18, 
                 weight=ft.FontWeight.BOLD),
                 
    ])
    tabla_general= ft.DataTable(ft.Text(""))


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