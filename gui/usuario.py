import flet as ft


from fuunciones import listar_usuarios


def mostrar_usuarios(page: ft.page):

    usuarios = listar_usuarios()

    tabla = ft.DataTa