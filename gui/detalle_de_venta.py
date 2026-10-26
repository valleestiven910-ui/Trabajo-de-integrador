import flet as ft

from funciones import listar_vacas


def vista_detalle_de_venta(page: ft. Page):
    
    mis_vacas = listar_vacas()
    if mis_vacas is None:
        mis_vacas=[]

    #Declaración de los campos de textos 
    txt_id_vaca= ft.TextField(label="ID vaca", read_only=True)
    txt_id_usuario=ft.TextField(label="ID Usuario", read_only=True)
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
                txt_nombre_vaca,
                txt_raza,
                txt_color,
                txt_peso,
            ], padding=20, scroll=ft.ScrollMode.AUTO)
        ]
    )