import flet as ft 
from funciones import listar_usuario, listar_finca, listar_vaca, listar_costos, listar_produción, listar_medicamento, listar_alimentación, listar_factura, listar_detalle_de_venta


def mostrar_dashboard(page: ft.page):

    titulo = ft. Text(
        value="Aplicación GAVAD",
        size=30,
        weight=ft.FontWeight.BOLd
    )

    descripcion = ft.Text(
        value="Sistema de gestión de GAVAD",
        size=16
    )

    total_usuarios = len(listar_usuario())
    total_finca = len(listar_finca())
    total_vaca = len(listar_vaca())
    total_factura = len(listar_factura())
    total_costo = len(listar_costos())
    total_detalle_de_venta = len(listar_detalle_de_venta())
    total_producción = len(listar_produción())
    total_medicamento = len(listar_medicamento())
    total_alimentación = len(listar_alimentación())


    estadisticas = ft.Row(
        controls=[
            ft.Text("Usuarios: " + str(total_usuarios)),
            ft.Text("Fincas: " + str(total_finca)),
            ft.Text("vacas: " + str(total_vaca)),
            ft.Text("Facturas: " + str(total_factura)),
            ft.Text("Costos: " + str(total_costo)),
            ft.Text("Detalles de ventas: " + str(total_detalle_de_venta)),
            ft.Text("Producciones: " + str(total_producción)),
            ft.Text("Medicamentos: " + str(total_medicamento)),
            ft.Text("Alimentación: " + str(total_alimentación))],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )
    return ft.Column(
        controls=[
            titulo,
            descripcion,
            estadisticas
        ]
    )