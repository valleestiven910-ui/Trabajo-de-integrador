from pathlib import Path

import flet as ft
import flet_video as ftv


VIDEO_PATH = (
    Path.home()
    / "Videos"
    / "Grabaciones de pantalla"
    / "Grabación de pantalla 2026-10-31 002908.mp4"
)


def mostrar_splash(page: ft.Page, al_finalizar):
    def abrir_inicio(error=None):
        page.controls.clear()
        al_finalizar()
        if error:
            page.snack_bar = ft.SnackBar(ft.Text(error))
            page.snack_bar.open = True
            page.update()

    if not VIDEO_PATH.is_file():
        abrir_inicio(f"No se encontró el video splash: {VIDEO_PATH}")
        return

    video = ftv.Video(
        playlist=[ftv.VideoMedia(VIDEO_PATH.name)],
        autoplay=True,
        muted=True,
        controls=None,
        fit=ft.BoxFit.CONTAIN,
        fill_color=ft.Colors.BLACK,
        expand=True,
        on_complete=lambda e: abrir_inicio(),
        on_error=lambda e: abrir_inicio("No se pudo reproducir el video splash."),
    )
    page.add(
        ft.Container(
            content=video,
            expand=True,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLACK,
        )
    )
    page.update()