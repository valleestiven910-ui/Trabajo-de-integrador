from datetime import date
from html import escape
from pathlib import Path

import flet as ft

from funciones import buscar_usuario, crear_factura


def mostrar_comprobante(vaca, costo_vaca, page: ft.Page):
    total_factura = sum(costo.precio for costo in costo_vaca)
    vendedor = buscar_usuario(vaca.id_usuario)
    nombre_vendedor = (
        f"{vendedor.nombres} {vendedor.apellidos}" if vendedor else "Dueño no encontrado"
    )
    nombre_comprador = ft.TextField(label="Nombre del comprador")
    cedula_comprador = ft.TextField(label="Cédula del comprador")

    def descargar_imagen(e):
        try:
            comprador = (nombre_comprador.value or "").strip()
            cedula = (cedula_comprador.value or "").strip()
            if not comprador or not cedula:
                raise ValueError("Completa el nombre y la cédula del comprador.")
            if total_factura <= 0:
                raise ValueError("Agrega al menos un costo con precio antes de comprar.")
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

            detalle_costos = "".join(
                f'<text x="40" y="{310 + indice * 32}" font-size="16">'
                f'{escape(costo.descripcion)}: C$ {costo.precio:.2f}</text>'
                for indice, costo in enumerate(costo_vaca)
            )
            altura = max(500, 430 + len(costo_vaca) * 32)

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
{detalle_costos}
<line x1="40" y1="{330 + len(costo_vaca) * 32}" x2="720" y2="{330 + len(costo_vaca) * 32}" stroke="#444"/>
<text x="40" y="{370 + len(costo_vaca) * 32}" font-family="Arial" font-size="24" font-weight="bold">TOTAL: C$ {total_factura:.2f}</text>
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
            page.snack_bar = ft.SnackBar(ft.Text(str(error)))
            page.snack_bar.open = True
            page.update()
            return

        dialogo.open = False
        page.snack_bar = ft.SnackBar(
            ft.Text(
                "Copias guardadas en facturas/: "
                f"{ruta_comprador.name} y {ruta_vendedor.name}"
            )
        )
        page.snack_bar.open = True
        page.update()

    dialogo = ft.AlertDialog(
        title=ft.Text(f"Factura de {vaca.nombre_vaca}"),
        content=ft.Column(
            [
                ft.Text(f"Total: C$ {total_factura:.2f}", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Vendedor: {nombre_vendedor}"),
                nombre_comprador,
                cedula_comprador,
            ],
            tight=True,
        ),
        actions=[
            ft.ElevatedButton("Comprar y guardar imagen", on_click=descargar_imagen),
            ft.TextButton("Cancelar", on_click=lambda e: cerrar(dialogo, page)),
        ],
    )
    page.dialog = dialogo
    dialogo.open = True
    page.update()


def cerrar(dialogo, page):
    dialogo.open = False
    page.update()