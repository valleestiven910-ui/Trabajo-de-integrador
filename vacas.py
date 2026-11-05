from pathlib import Path
import shutil
from uuid import uuid4

import flet as ft

from funciones import (
    actualizar_vaca,
    actualizar_estado_y_foto_catalogo,
    buscar_finca,
    buscar_usuario,
    eliminar_vaca,
    listar_fincas,
    listar_usuario,
    listar_vacas,
    registrar_vaca,
)
from gui.mensajes import mostrar_mensaje

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"


def cambiar_estado_catalogo(e, vaca, page:ft.Page):
    activar = bool(e.control.value)
    if activar and not vaca.imagen:
        e.control.value = False
        mostrar_mensaje(page, "Agrega una imagen antes de publicar la vaca.")
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
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Editar",
                                        on_click=lambda e, v=vaca: abrir_formulario(e, v),
                                    ),
                                    ft.TextButton(
                                        "Borrar",
                                        on_click=lambda e, v=vaca: confirmar_borrado(v),
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                    ]
                )
            )

        tabla_contenedor.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Arete / ID")),
                ft.DataColumn(ft.Text("Finca")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Raza")),
                ft.DataColumn(ft.Text("Color")),
                ft.DataColumn(ft.Text("Peso (kg)")),
                ft.DataColumn(ft.Text("Dueño")),
                ft.DataColumn(ft.Text("Catálogo")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=filas,
        )

    def abrir_formulario(e, vaca_editar=None):
        usuarios = listar_usuario()
        if not usuarios:
            mostrar_mensaje(page, "Registra primero un usuario y su finca para agregar vacas.")
            return

        dueño = ft.Dropdown(
            label="Usuario dueño",
            value=str(vaca_editar.id_usuario) if vaca_editar else None,
            options=[
                ft.dropdown.Option(
                    key=str(usuario.id_usuario),
                    text=f"{usuario.nombres} {usuario.apellidos} (ID {usuario.id_usuario})",
                )
                for usuario in usuarios
            ],
        )
        fincas = listar_fincas()
        fincas_dueño = (
            [finca for finca in fincas if finca.id_usuario == vaca_editar.id_usuario]
            if vaca_editar
            else fincas
        )
        finca_seleccionada = ft.Dropdown(
            label="Finca",
            helper_text="Al elegir un dueño, se muestran solo sus fincas.",
            options=[
                ft.dropdown.Option(
                    key=str(finca.id_finca),
                    text=f"{finca.nombre_finca} (ID {finca.id_finca})",
                )
                for finca in fincas_dueño
            ],
            value=str(vaca_editar.id_finca) if vaca_editar else None,
        )

        def cargar_fincas(e=None):
            fincas_dueño = fincas
            if dueño.value:
                fincas_dueño = [
                    finca
                    for finca in fincas
                    if str(finca.id_usuario) == str(dueño.value)
                ]
            ids_fincas_dueño = {str(finca.id_finca) for finca in fincas_dueño}
            finca_seleccionada.options = [
                ft.dropdown.Option(
                    key=str(finca.id_finca),
                    text=f"{finca.nombre_finca} (ID {finca.id_finca})",
                )
                for finca in fincas_dueño
            ]
            if finca_seleccionada.value not in ids_fincas_dueño:
                finca_seleccionada.value = None
            page.update()

        dueño.on_change = cargar_fincas
        nombre = ft.TextField(
            label="Nombre",
            value=vaca_editar.nombre_vaca if vaca_editar else "",
        )
        raza = ft.TextField(label="Raza", value=vaca_editar.raza if vaca_editar else "")
        color = ft.TextField(label="Color", value=vaca_editar.color if vaca_editar else "")
        peso = ft.TextField(
            label="Peso (kg)",
            value=str(vaca_editar.peso) if vaca_editar else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        id_arete = ft.TextField(
            label="Número de arete (ID de vaca)",
            value=str(vaca_editar.id_vaca) if vaca_editar else "",
            read_only=bool(vaca_editar),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        precio_venta = ft.TextField(
            label="Precio de venta (opcional)",
            hint_text="Ej.: 40,000 o 1250,50",
            value=str(vaca_editar.precio_venta) if vaca_editar and vaca_editar.precio_venta else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        salud = ft.TextField(
            label="Salud / condición",
            value=vaca_editar.salud if vaca_editar else "",
        )
        vacunas = ft.TextField(
            label="Vacunas y tratamientos",
            value=vaca_editar.vacunas if vaca_editar else "",
        )
        motivo_venta = ft.TextField(
            label="Motivo de venta",
            value=vaca_editar.motivo_venta if vaca_editar else "",
        )
        ruta_imagen = vaca_editar.imagen if vaca_editar else ""
        if ruta_imagen:
            ruta_imagen = ruta_imagen.replace("\\", "/")
            if ruta_imagen.startswith("catalogo/"):
                ruta_imagen = f"assets/{ruta_imagen}"
        imagen = ft.TextField(
            label="Foto seleccionada",
            value=ruta_imagen,
            read_only=True,
            expand=True,
        )
        vista_previa = ft.Image(
            src=ruta_imagen,
            width=180,
            height=140,
            fit=ft.BoxFit.CONTAIN,
        )
        publicar = ft.Checkbox(
            label="Publicar en catálogo",
            value=vaca_editar.en_catalogo if vaca_editar else False,
        )

        def seleccionar_imagen(e):
            if not e.files:
                return

            archivo = e.files[0]
            extension = Path(archivo.name).suffix.lower()
            if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
                mostrar_mensaje(page, "Selecciona una imagen JPG, PNG o WebP.")
                return

            carpeta_imagenes = ASSETS_DIR / "catalogo"
            destino = carpeta_imagenes / f"{uuid4().hex}{extension}"
            try:
                carpeta_imagenes.mkdir(parents=True, exist_ok=True)
                if archivo.bytes is not None:
                    destino.write_bytes(archivo.bytes)
                elif archivo.path:
                    shutil.copy2(archivo.path, destino)
                else:
                    raise OSError("El selector no devolvió acceso al archivo.")
            except OSError as error:
                mostrar_mensaje(page, f"No se pudo guardar la foto: {error}")
                return

            imagen.value = destino.relative_to(ASSETS_DIR.parent).as_posix()
            vista_previa.src = imagen.value
            page.update()

        selector_imagen = next(
            (
                servicio
                for servicio in page.services
                if isinstance(servicio, ft.FilePicker)
                and servicio.data == "selector-foto-vaca"
            ),
            None,
        )
        if selector_imagen is None:
            selector_imagen = ft.FilePicker()
            selector_imagen.data = "selector-foto-vaca"
            page.services.append(selector_imagen)
        selector_imagen.on_result = seleccionar_imagen

        def guardar(ev):
            try:
                if publicar.value and not (imagen.value or "").strip():
                    raise ValueError("Agrega una imagen para publicar la vaca.")
                if vaca_editar:
                    actualizado = actualizar_vaca(
                        id_vaca=vaca_editar.id_vaca,
                        id_usuario=dueño.value or "",
                        id_finca=finca_seleccionada.value or "",
                        nombre_vaca=nombre.value or "",
                        raza=raza.value or "",
                        peso=peso.value or "",
                        color=color.value or "",
                        imagen=imagen.value or "",
                        en_catalogo=publicar.value,
                        precio_venta=precio_venta.value or "",
                        salud=salud.value or "",
                        vacunas=vacunas.value or "",
                        motivo_venta=motivo_venta.value or "",
                    )
                    if not actualizado:
                        raise ValueError("No se encontró la vaca para actualizar.")
                else:
                    registrar_vaca(
                        id_usuario=dueño.value or "",
                        id_finca=finca_seleccionada.value or "",
                        nombre_vaca=nombre.value or "",
                        raza=raza.value or "",
                        color=color.value or "",
                        peso=peso.value or "",
                        imagen=imagen.value or "",
                        en_catalogo=publicar.value,
                        id_arete=id_arete.value or "",
                    )
            except (OSError, ValueError) as error:
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            cargar_tabla()
            mostrar_mensaje(
                page,
                "Vaca actualizada correctamente."
                if vaca_editar
                else "Vaca registrada correctamente.",
            )

        dialogo = ft.AlertDialog(
            title=ft.Text("Editar vaca" if vaca_editar else "Registrar vaca"),
            content=ft.Column(
                [
                    dueño,
                    finca_seleccionada,
                    nombre,
                    raza,
                    color,
                    peso,
                    *([id_arete] if not vaca_editar else []),
                    *(
                        [precio_venta, salud, vacunas, motivo_venta]
                        if vaca_editar
                        else []
                    ),
                    ft.Row(
                        [
                            imagen,
                            ft.Button(
                                "Subir foto",
                                icon=ft.Icons.UPLOAD_FILE,
                                action=ft.PickFiles(
                                    selector_imagen,
                                    dialog_title="Selecciona la foto de la vaca",
                                    file_type=ft.FilePickerFileType.IMAGE,
                                    allowed_extensions=["jpg", "jpeg", "png", "webp"],
                                    allow_multiple=False,
                                    with_data=True,
                                ),
                            ),
                        ]
                    ),
                    vista_previa,
                    publicar,
                ],
                tight=True,
                height=560,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.Button("Guardar", on_click=guardar),
                ft.TextButton(
                    "Cancelar",
                    on_click=lambda ev: cerrar_dialogo(dialogo, page),
                ),
            ],
        )
        page.show_dialog(dialogo)

    def confirmar_borrado(vaca):
        def borrar(ev):
            try:
                eliminado = eliminar_vaca(vaca.id_vaca)
            except ValueError as error:
                page.pop_dialog()
                mostrar_mensaje(page, str(error))
                return

            page.pop_dialog()
            if eliminado:
                cargar_tabla()
                mostrar_mensaje(
                    page,
                    "Vaca y sus registros relacionados eliminados correctamente.",
                )
            else:
                mostrar_mensaje(page, "No se encontró la vaca para borrar.")

        dialogo = ft.AlertDialog(
            title=ft.Text("Borrar vaca"),
            content=ft.Text(
                f"¿Borrar a {vaca.nombre_vaca} (arete {vaca.id_vaca}) y sus costos, "
                "medicamentos, producción y alimentación asociados? Esta acción no se puede deshacer."
            ),
            actions=[
                ft.Button("Borrar", on_click=borrar),
                ft.TextButton("Cancelar", on_click=lambda ev: cerrar_dialogo(dialogo, page)),
            ],
        )
        page.show_dialog(dialogo)

    cargar_tabla()
    return ft.Column(
        controls=[
            ft.Row(
                [
                    ft.Text("Vacas", size=28, weight=ft.FontWeight.BOLD),
                    ft.Button("Registrar vaca", on_click=abrir_formulario),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            tabla_contenedor,
        ],
        expand=True,
    )


def cerrar_dialogo(dialogo, page):
    page.pop_dialog()