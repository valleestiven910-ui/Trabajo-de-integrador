import flet as ft
from funciones import (
    buscar_finca,
    eliminar_costo,
    listar_vacas_en_catalogo,
    listar_costos,
)
from gui.costo import mostrar_formulario_costo
from gui.factura import mostrar_comprobante
from gui.mensajes import mostrar_mensaje


VERDE = "#034d2c"
CREMA = "#faf7ca"


def _dato_catalogo(icono, texto):
    return ft.Row(
        [
            ft.Icon(icono, size=16, color=VERDE),
            ft.Text(texto, size=12, color=VERDE),
        ],
        spacing=6,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


def ver_costo_vaca(vaca, page: ft.Page):
    costos_vaca = [c for c in listar_costos() if c.id_vaca == vaca.id_vaca]

    detalles_elementos = []

    if vaca.imagen:
        detalles_elementos.append(
            ft.Image(
                src=vaca.imagen,
                width=560,
                height=220,
                fit=ft.BoxFit.CONTAIN,
            )
        )
    finca = buscar_finca(vaca.id_finca)
    detalles_elementos.extend(
        [
            ft.Text(f"Raza: {vaca.raza}"),
            ft.Text(f"Color: {vaca.color}"),
            ft.Text(f"Peso: {vaca.peso:g} kg"),
            ft.Text(f"Finca: {finca.nombre_finca if finca else 'No especificada'}"),
            ft.Text(f"Salud / condición: {vaca.salud or 'No especificada'}"),
            ft.Text(f"Vacunas y tratamientos: {vaca.vacunas or 'No especificados'}"),
            ft.Text(f"Motivo de venta: {vaca.motivo_venta or 'No especificado'}"),
            ft.Text("Precio de venta", weight=ft.FontWeight.BOLD),
            ft.Text(
                f"C$ {vaca.precio_venta:,.2f}" if vaca.precio_venta > 0
                else "Precio de venta no registrado"
            ),
            ft.Text("Costos registrados", weight=ft.FontWeight.BOLD),
        ]
    )

    if not costos_vaca:
        detalles_elementos.append(ft.Text("No hay registros de costos para esta vaca.", italic=True))
    else:
        for c in costos_vaca:
            detalles_elementos.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Descripción: {c.descripcion}"),
                        ft.Text(f"Fecha: {c.fecha}"),
                        ft.Text(
                            f"Precio: C${c.precio:.2f}",
                            color=VERDE,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Editar",
                                    on_click=lambda e, costo=c: editar_costo(costo),
                                ),
                                ft.TextButton(
                                    "Borrar",
                                    on_click=lambda e, costo=c: confirmar_borrado_costo(costo),
                                ),
                            ],
                            spacing=0,
                        ),
                    ]),
                    padding=10,
                    border=ft.Border.all(1, VERDE),
                    border_radius=ft.BorderRadius.all(8),
                    margin=ft.Margin.only(bottom=10),
                )
            )

    def agregar_costo(e):
        def actualizar_costos():
            page.pop_dialog()
            ver_costo_vaca(vaca, page)

        mostrar_formulario_costo(vaca, page, actualizar_costos)

    def editar_costo(costo):
        def actualizar_costos():
            page.pop_dialog()
            ver_costo_vaca(vaca, page)

        mostrar_formulario_costo(
            vaca,
            page,
            actualizar_costos,
            costo_editar=costo,
        )

    def confirmar_borrado_costo(costo):
        def borrar(ev):
            eliminado = eliminar_costo(costo.id_costos)
            page.pop_dialog()
            if eliminado:
                page.pop_dialog()
                ver_costo_vaca(vaca, page)
            else:
                mostrar_mensaje(page, "No se encontró el costo para borrar.")

        dialogo_confirmacion = ft.AlertDialog(
            title=ft.Text("Borrar costo"),
            content=ft.Text(f"¿Borrar el costo “{costo.descripcion}”?"),
            actions=[
                ft.Button("Borrar", on_click=borrar),
                ft.TextButton("Cancelar", on_click=lambda e: page.pop_dialog()),
            ],
        )
        page.show_dialog(dialogo_confirmacion)

    def realizar_compra(e):
        page.pop_dialog()
        mostrar_comprobante(vaca, costos_vaca, page)

    dlg_costos = ft.AlertDialog(
        title=ft.Text(f"Información de {vaca.nombre_vaca}"),
        content=ft.Container(
            width=600,
            height=440,
            content=ft.Column(
                detalles_elementos,
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        actions=[
            ft.Button(
                "Registrar costo",
                icon=ft.Icons.ADD,
                on_click=agregar_costo,
            ),
            *(
                [
                    ft.Button(
                        "Comprar Vaca",
                        icon=ft.Icons.SHOPPING_CART,
                        bgcolor=VERDE,
                        color=CREMA,
                        on_click=realizar_compra,
                    )
                ]
                if vaca.precio_venta > 0
                else []
            ),
            ft.TextButton(
                "Cerrar",
                on_click=lambda e: page.pop_dialog(),
            ),
        ],
    )
    page.show_dialog(dlg_costos)

def mostrar_catalogo(page: ft.Page):
    vacas_catalogo = listar_vacas_en_catalogo()

    tarjetas = []
    tarjetas_por_vaca = []

    if not vacas_catalogo:
        tarjetas.append(ft.Text("No hay vacas publicadas en el catálogo todavía.", size=16, italic=True))

    else:
        for vaca in vacas_catalogo:
            finca = buscar_finca(vaca.id_finca)
            ruta_imagen = (vaca.imagen or "").replace("\\", "/")
            if ruta_imagen.startswith("catalogo/"):
                ruta_imagen = f"assets/{ruta_imagen}"
            tarjeta= ft.Container(
                content=ft.Column([

                    ft.Image(
                        src=ruta_imagen
                        if ruta_imagen
                        else "https://via.placeholder.com/150",
                        width=150,
                        height=150,
                        fit=ft.BoxFit.COVER,
                        border_radius=ft.BorderRadius.all(10),
                    ),
                    ft.Text(
                        vaca.nombre_vaca,
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=VERDE,
                    ),
                    _dato_catalogo(ft.Icons.PETS, f"Raza: {vaca.raza}"),
                    _dato_catalogo(ft.Icons.SCALE, f"Peso: {vaca.peso:g} kg"),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SELL, size=16, color=VERDE),
                            ft.Text(
                                f"C$ {vaca.precio_venta:,.2f}"
                                if vaca.precio_venta > 0
                                else "Precio pendiente",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=VERDE,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10,
                border=ft.Border.all(1, VERDE),
                border_radius=ft.BorderRadius.all(10),
                bgcolor=CREMA,
                on_click=lambda e, v=vaca: ver_costo_vaca(v, page)
            )
            tarjetas_por_vaca.append((vaca, finca, tarjeta))

    if tarjetas_por_vaca:
        tarjetas = [tarjeta for _, _, tarjeta in tarjetas_por_vaca]

    grid_vacas = ft.GridView(
        expand=True,
        runs_count=4,
        max_extent=200,
        child_aspect_ratio=0.8,
        spacing=10,
        run_spacing=10,
        controls=tarjetas,
    )

    def buscar_vacas(e=None):
        consulta = (busqueda.value or "").strip().casefold()
        coincidencias = []
        for vaca, finca, tarjeta in tarjetas_por_vaca:
            valores = (
                vaca.id_vaca,
                vaca.nombre_vaca,
                vaca.raza,
                vaca.color,
                finca.nombre_finca if finca else "",
                vaca.salud,
                vaca.vacunas,
                vaca.motivo_venta,
            )
            if not consulta or any(consulta in str(valor).casefold() for valor in valores):
                coincidencias.append(tarjeta)

        grid_vacas.controls = coincidencias or [
            ft.Text("No se encontraron vacas con esa búsqueda.", italic=True)
        ]
        page.update()

    busqueda = ft.TextField(
        label="Buscar vaca",
        hint_text="Nombre, arete, raza, color o finca",
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=VERDE,
        color=CREMA,
        label_style=ft.TextStyle(color=CREMA),
        hint_style=ft.TextStyle(color=CREMA),
        border_color=CREMA,
        focused_border_color=CREMA,
        cursor_color=CREMA,
        on_change=buscar_vacas,
    )

    return ft.View(
        route="/catalogo",
        bgcolor=CREMA,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Vacas en ventas",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=VERDE,
                        ),
                        ft.Divider(color=VERDE),
                        busqueda,
                        ft.Container(content=grid_vacas, expand=True, padding=10),
                    ],
                    expand=True,
                ),
                padding=20,
                expand=True,
            )
        ]
    )
