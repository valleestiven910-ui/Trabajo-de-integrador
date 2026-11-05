from pathlib import Path

import flet as ft
import flet_video as ftv

from gui.mensajes import mostrar_mensaje


ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
VIDEO_PATH = Path(__file__).resolve().parents[1] / "Grabación de pantalla 2026-11-02 185800.mp4"
def mostrar_splash(page: ft.Page, al_finalizar):
    def abrir_inicio(error=None):
        page.controls.clear()
        al_finalizar()
        if error:
            mostrar_mensaje(page, error)

    def mostrar_error_video(e):
        detalle = getattr(e, "data", None) or "El reproductor no proporcionó detalles."
        abrir_inicio(f"No se pudo reproducir el video splash: {detalle}")

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
        on_error=mostrar_error_video,
    )
    page.add(
        ft.Container(
            content=video,
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor=ft.Colors.BLACK,
        )
    )
    page.update()