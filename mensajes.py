import flet as ft


def mostrar_mensaje(page: ft.Page, mensaje: str):
    page.show_dialog(ft.SnackBar(ft.Text(mensaje)))
