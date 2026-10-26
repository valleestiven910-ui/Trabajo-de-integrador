import flet as ft

from funciones import listar_vacas, buscar_usuario, actualizar_estado_y_foto_catalogo


def cambiar_estado_catalogo(e, vaca, page:ft.Page):
    if e.control.value:
        txt_foto = ft.TextField(
            label="Nombre o ruta de la foto",
            value= vaca.imagen if vaca.imagen else"",
            width=300
        )

        def guardar_foto_y_activar(dialog_event):
            actualizar_estado_y_foto_catalogo(vaca.id_vaca, True, txt_foto.value)
            page.dialog.open = False
            page.update()

            page.snack_bar = ft.SnackBar(ft.Text (f"¡{vaca.nombre_vaca} subida al catalogo!"))
            page.snack_bar.open = True
            page.update()

        def cancelar_cambio(dialog_event):
            e.control.value =False
            page.dialog.open = False
            page.update()

        dlg_foto = ft.AlertDialog(
            title=ft.Text(f"Subir al cátalogo: {vaca.nombre_vaca}"),
            content=ft.Column([
                ft.Text("Ingrese la foto obligatoria para el catalogo:"),
                txt_foto
            ], height=100, tight=True),
            actions=[
                ft.TextButton("Guardar", on_click=guardar_foto_y_activar),
                ft.TextButton("Cancelar", on_click=cancelar_cambio)
            ]
        )

        page.dialog =dlg_foto
        dlg_foto.open = True
        page.update()



    else:
        actualizar_estado_y_foto_catalogo(vaca.id_vaca, False, vaca.imagen)
        page.update()
def mostrar_vacas(page: ft.Page):

    vacas = listar_vacas()

    filas = []

    tabla = ft.DataTable(
        columns =[
            ft.DataColumn(ft.Text("ID de Vaca")),
            ft.DataColumn(ft.Text("ID de Finca")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Raza")),
            ft.DataColumn(ft.Text("Color")),
            ft.DataColumn(ft.Text("Peso")), 
            ft.DataColumn(ft.Text(" Usuario")),
            ft.DataColumn(ft.Text("Catalogo")),
        ],
        rows =[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(vaca.id_vaca)),
                    ft.DataCell(ft.Text(vaca.id_finca)),
                    ft.DataCell(ft.Text(vaca.nombre_vaca)),
                    ft.DataCell(ft.Text(vaca.raza)),
                    ft.DataCell(ft.Text(vaca.color)),
                    ft.DataCell(ft.Text(vaca.peso)),
                    ft.DataCell(ft.Text(buscar_usuario(vaca.id_usuario).nombre
                                        if buscar_usuario(vaca.id_usuario) else "Desconocido")),
                    ft.DataCell(
                        ft.Switch(
                            value=vaca.en_catalogo,
                            on_change=lambda e, v=vaca: cambiar_estado_catalogo(e, v, page)
                        )
                    ),
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