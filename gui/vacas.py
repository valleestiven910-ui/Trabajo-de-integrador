import flet as ft

from funciones import (
    actualizar_estado_y_foto_catalogo,
    buscar_finca,
    buscar_usuario,
    listar_fincas,
    listar_usuario,
    listar_vacas,
    registrar_vaca,
)


def cambiar_estado_catalogo(e, vaca, page:ft.Page):
    activar = bool(e.control.value)
    if activar and not vaca.imagen:
        e.control.value = False
        page.snack_bar = ft.SnackBar(ft.Text("Agrega una imagen antes de publicar la vaca."))
        page.snack_bar.open = True
        page.update()
        return

    actualizar_estado_y_foto_catalogo(vaca.id_vaca, activar, vaca.imagen)
    page.update()
def mostrar_vacas(page: ft.Page):
    tabla_contenedor = ft.Container(expand=True)

    def cargar_tabla():
        filas = []
        for vaca in listar_vacas():
            finca = buscar_finca(vaca.id_finca)
            usuario = buscar_usuario(vaca.id_usuario)
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(vaca.id_vaca))),
                        ft.DataCell(ft.Text(finca.nombre_finca if finca else "Desconocida")),
                        ft.DataCell(ft.Text(vaca.nombre_vaca)),
                        ft.DataCell(ft.Text(vaca.raza)),
                        ft.DataCell(ft.Text(vaca.color)),
                        ft.DataCell(ft.Text(str(vaca.peso))),
                        ft.DataCell(ft.Text(usuario.nombres if usuario else "Desconocido")),
                        ft.DataCell(
                            ft.Switch(
                                value=vaca.en_catalogo,
                                on_change=lambda e, v=vaca: cambiar_estado_catalogo(e, v, page),
                            )
                        ),
                    ]
                )
            )

        tabla_contenedor.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID de vaca")),
                ft.DataColumn(ft.Text("Finca")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Raza")),
                ft.DataColumn(ft.Text("Color")),
                ft.DataColumn(ft.Text("Peso")),
                ft.DataColumn(ft.Text("Dueño")),
                ft.DataColumn(ft.Text("Catálogo")),
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
        finca_seleccionada = ft.Dropdown(label="Finca")

        def cargar_fincas(e=None):
            fincas_dueño = [
                finca
                for finca in listar_fincas()
                if str(finca.id_usuario) == str(dueño.value)
            ]
            finca_seleccionada.options = [
                ft.dropdown.Option(
                    key=str(finca.id_finca),
                    text=f"{finca.nombre_finca} (ID {finca.id_finca})",
                )
                for finca in fincas_dueño
            ]
            finca_seleccionada.value = None
            page.update()

        dueño.on_change = cargar_fincas
        nombre = ft.TextField(label="Nombre")
        raza = ft.TextField(label="Raza")
        color = ft.TextField(label="Color")
        peso = ft.TextField(label="Peso en kg", keyboard_type=ft.KeyboardType.NUMBER)
        imagen = ft.TextField(label="URL o ruta de imagen")
        publicar = ft.Checkbox(label="Publicar en catálogo", value=False)

        def guardar(ev):
            try:
                if publicar.value and not (imagen.value or "").strip():
                    raise ValueError("Agrega una imagen para publicar la vaca.")
                registrar_vaca(
                    dueño.value or "",
                    finca_seleccionada.value or "",
                    nombre.value or "",
                    raza.value or "",
                    color.value or "",
                    peso.value or "",
                    imagen.value or "",
                    publicar.value,
                )
            except ValueError as error:
                page.snack_bar = ft.SnackBar(ft.Text(str(error)))
                page.snack_bar.open = True
                page.update()
                return

            dialogo.open = False
            cargar_tabla()
            page.snack_bar = ft.SnackBar(ft.Text("Vaca registrada correctamente."))
            page.snack_bar.open = True
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Registrar vaca"),
            content=ft.Column(
                [dueño, finca_seleccionada, nombre, raza, color, peso, imagen, publicar],
                tight=True,
                height=400,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.ElevatedButton("Guardar", on_click=guardar),
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda ev: cerrar_dialogo(dialogo, page),
                ),
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
                    ft.Text("Vacas", size=28, weight=ft.FontWeight.BOLD),
                    ft.ElevatedButton("Registrar vaca", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar_dialogo(dialogo, page):
    dialogo.open = False
    page.update()