import flet as ft

from funciones import listar_costos, listar_vacas
from gui.factura import mostrar_comprobante


def mostrar_detalle_vaca(vaca, page: ft.Page):
    def comprar(e):
        dialogo.open = False
        page.update()
        costos = [costo for costo in listar_costos() if costo.id_vaca == vaca.id_vaca]
        mostrar_comprobante(vaca, costos, page)

    dialogo = ft.AlertDialog(
        title=ft.Text(f"Detalle de vaca: {vaca.nombre_vaca}"),
        content=ft.Column(
            [
                ft.Image(src=vaca.imagen, width=220, height=150, fit=ft.ImageFit.COVER),
                ft.Text(f"ID: {vaca.id_vaca}"),
                ft.Text(f"Dueño (ID): {vaca.id_usuario}"),
                ft.Text(f"Finca (ID): {vaca.id_finca}"),
                ft.Text(f"Nombre: {vaca.nombre_vaca}"),
                ft.Text(f"Raza: {vaca.raza}"),
                ft.Text(f"Color: {vaca.color}"),
                ft.Text(f"Peso: {vaca.peso} kg"),
            ],
            tight=True,
        ),
        actions=[
            ft.ElevatedButton("Comprar", on_click=comprar),
            ft.TextButton("Cerrar", on_click=lambda e: cerrar(dialogo, page)),
        ],
    )
    page.dialog = dialogo
    dialogo.open = True
    page.update()


def cerrar(dialogo, page):
    dialogo.open = False
    page.update()


def vista_detalle_de_venta(page: ft. Page):
    
    mis_vacas = listar_vacas()
    if mis_vacas is None:
        mis_vacas=[]

    #Declaración de los campos de textos 
    txt_id_vaca= ft.TextField(label="ID vaca", read_only=True)
    txt_id_usuario=ft.TextField(label="ID Usuario", read_only=True)
    txt_id_finca= ft.TextField(label= "ID Vaca", read_only=True)
    txt_nombre_vaca= ft.TextField(label="Nombre Vaca", read_only=True)
    txt_raza = ft.TextField(label="Raza", read_only=True)
    txt_color = ft.TextField(label="Color", read_only=True)
    txt_peso = ft.TextField(label="Peso", read_only=True)
    dropdown_vacas = ft.Dropdown(
        label="Seleccionar Vaca Registrada",
        options=[
            ft.dropdown.Option(
            key=str(v.id_vaca), 
            text=f"{v.id_vaca}-{v.nombre_vaca}"
            ) for v in mis_vacas
        ],
    
)
    def seleccionar_vacas(e):
        id_sel = dropdown_vacas.value
        vaca = next((v for v in mis_vacas if str(v.id_vaca) ==str( id_sel)), None)

        if vaca:
            txt_id_vaca.value = str(vaca.id_vaca)
            txt_id_usuario.value = str(vaca.id_usuario) 
            txt_id_finca.value = str(vaca.id_finca)
            txt_nombre_vaca.value = str(vaca.nombre_vaca)
            txt_raza.value = str(vaca.raza)
            txt_color.value = str(vaca.color)
            txt_peso.value = str(vaca.peso)
            page.update()

    dropdown_vacas.on_change =seleccionar_vacas

    return ft.View(
        "/detalle_de_venta",
        [
            ft.AppBar(title=ft.Text("Detalle de Venta"), bgcolor=ft.colors.BLUE_GREY_900),
            ft.Column([
                dropdown_vacas,
                txt_id_vaca,
                txt_id_usuario,
                txt_id_finca,
                txt_nombre_vaca,
                txt_raza,
                txt_color,
                txt_peso,
            ], padding=20, scroll=ft.ScrollMode.AUTO)
        ]
    )