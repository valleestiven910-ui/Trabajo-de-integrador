from datetime import date
from html import escape
from pathlib import Path

import flet as ft

from funciones import buscar_finca, buscar_usuario, crear_factura
from gui.mensajes import mostrar_mensaje


def mostrar_comprobante(vaca, costo_vaca, page: ft.Page):
    total_factura = vaca.precio_venta
    vendedor = buscar_usuario(vaca.id_usuario)
    finca = buscar_finca(vaca.id_finca)
    nombre_vendedor = (
        f"{vendedor.nombres} {vendedor.apellidos}" if vendedor else "Dueño no encontrado"
    )
    nombre_finca = finca.nombre_finca if finca else "No especificada"
    nombre_comprador = ft.TextField(label="Nombre del comprador")
    cedula_comprador = ft.TextField(label="Cédula del comprador")

    def descargar_imagen(e):
        try:
            comprador = (nombre_comprador.value or "").strip()
            cedula = (cedula_comprador.value or "").strip()
            if not comprador or not cedula:
                raise ValueError("Completa el nombre y la cédula del comprador.")
            if total_factura <= 0:
                raise ValueError("Registra el precio de venta de la vaca antes de comprar.")
            if vendedor is None:
                raise ValueError("La vaca debe tener un usuario dueño registrado.")

            fecha_factura = date.today().isoformat()
            nueva_factura = crear_factura(
                monto_pagado=total_factura,
                fecha=fecha_factura,
                id_vendedor=vaca.id_usuario,
                id_comprador=0,
                id_vaca=vaca.id_vaca,
                nombre_comprador=comprador,
                cedula_comprador=cedula,
                nombre_vendedor=nombre_vendedor,
                cedula_vendedor=vendedor.cedula,
            )
            if nueva_factura is False:
                raise ValueError("No se pudo crear la factura.")

            descripcion_venta = [
                f"Raza: {vaca.raza}",
                f"Color: {vaca.color}",
                f"Peso: {vaca.peso:g} kg",
                f"Finca: {nombre_finca}",
                f"Salud / condición: {vaca.salud or 'No especificada'}",
                f"Vacunas y tratamientos: {vaca.vacunas or 'No especificados'}",
                f"Motivo de venta: {vaca.motivo_venta or 'No especificado'}",
            ]
            detalle_vaca = "".join(
                f'<text x="40" y="{325 + indice * 28}" font-size="16">'
                f'{escape(detalle)}</text>'
                for indice, detalle in enumerate(descripcion_venta)
            )
            inicio_costos = 325 + len(descripcion_venta) * 28 + 12
            detalle_costos = ""
            if costo_vaca:
                detalle_costos = (
                    f'<text x="40" y="{inicio_costos}" font-size="17" font-weight="bold">'
                    "Costos registrados (informativos)</text>"
                    + "".join(
                        f'<text x="40" y="{inicio_costos + 28 + indice * 28}" font-size="16">'
                        f'{escape(costo.descripcion)}: C$ {costo.precio:,.2f}</text>'
                        for indice, costo in enumerate(costo_vaca)
                    )
                )
            y_total = inicio_costos + (28 + len(costo_vaca) * 28 if costo_vaca else 8) + 32
            altura = max(650, y_total + 70)

            def crear_contenido_svg(tipo_copia):
                return f'''<svg xmlns="http://www.w3.org/2000/svg" width="760" height="{altura}" viewBox="0 0 760 {altura}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="40" y="55" font-family="Arial" font-size="30" font-weight="bold">Factura GAVAD #{nueva_factura.id_factura}</text>
<text x="40" y="88" font-family="Arial" font-size="18" font-weight="bold">{tipo_copia}</text>
<text x="40" y="125" font-family="Arial" font-size="18">Fecha: {fecha_factura}</text>
<text x="40" y="160" font-family="Arial" font-size="18">Vendedor: {escape(nombre_vendedor)}</text>
<text x="40" y="190" font-family="Arial" font-size="18">Cédula vendedor: {escape(vendedor.cedula)}</text>
<text x="40" y="225" font-family="Arial" font-size="18">Comprador: {escape(comprador)}</text>
<text x="40" y="255" font-family="Arial" font-size="18">Cédula comprador: {escape(cedula)}</text>
<text x="40" y="290" font-family="Arial" font-size="18" font-weight="bold">Vaca: {escape(vaca.nombre_vaca)} (ID {vaca.id_vaca})</text>
{detalle_vaca}
{detalle_costos}
<line x1="40" y1="{y_total - 20}" x2="720" y2="{y_total - 20}" stroke="#444"/>
<text x="40" y="{y_total + 20}" font-family="Arial" font-size="24" font-weight="bold">PRECIO DE VENTA: C$ {total_factura:,.2f}</text>
</svg>'''

            carpeta_facturas = Path(__file__).resolve().parents[1] / "facturas"
            carpeta_facturas.mkdir(exist_ok=True)
            ruta_comprador = carpeta_facturas / f"factura-{nueva_factura.id_factura}-comprador.svg"
            ruta_vendedor = carpeta_facturas / f"factura-{nueva_factura.id_factura}-vendedor.svg"
            ruta_comprador.write_text(
                crear_contenido_svg("COPIA PARA EL COMPRADOR"), encoding="utf-8"
            )
            ruta_vendedor.write_text(
                crear_contenido_svg("COPIA PARA EL VENDEDOR"), encoding="utf-8"
            )
        except (OSError, ValueError) as error:
            mostrar_mensaje(page, str(error))
            return

        page.pop_dialog()
        mostrar_mensaje(
            page,
            "Copias guardadas en facturas/: "
            f"{ruta_comprador.name} y {ruta_vendedor.name}",
        )

    dialogo = ft.AlertDialog(
        title=ft.Text(f"Factura de {vaca.nombre_vaca}"),
        content=ft.Column(
            [
                ft.Text(f"Precio de venta: C$ {total_factura:,.2f}", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Vendedor: {nombre_vendedor}"),
                ft.Text(
                    f"{vaca.raza}, {vaca.color}, {vaca.peso:g} kg | Finca: {nombre_finca}"
                ),
                nombre_comprador,
                cedula_comprador,
            ],
            tight=True,
        ),
        actions=[
            ft.Button("Comprar y guardar imagen", on_click=descargar_imagen),
            ft.TextButton("Cancelar", on_click=lambda e: cerrar(dialogo, page)),
        ],
    )
    page.show_dialog(dialogo)


def cerrar(dialogo, page):
    page.pop_dialog()