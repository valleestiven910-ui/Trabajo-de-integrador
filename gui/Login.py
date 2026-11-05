import flet as ft

from funciones import iniciar_sesion, registrar_usuario
from gui.mensajes import mostrar_mensaje


VERDE = "#034d2c"
CREMA = "#faf7ca"


def _aplicar_colores(campo):
	campo.bgcolor = VERDE
	campo.color = CREMA
	campo.cursor_color = CREMA
	campo.border_color = CREMA
	campo.focused_border_color = CREMA
	campo.label_style = ft.TextStyle(color=CREMA)
	campo.hint_style = ft.TextStyle(color=CREMA)


def mostrar_login(page: ft.Page, al_iniciar_sesion):
	def mostrar_formulario(cedula_inicial="", mensaje=""):
		page.controls.clear()

		cedula = ft.TextField(
			label="Cédula",
			value=cedula_inicial,
			autofocus=True,
			on_submit=lambda e: iniciar(e),
		)
		contraseña = ft.TextField(
			label="Contraseña",
			password=True,
			can_reveal_password=True,
			on_submit=lambda e: iniciar(e),
		)

		_aplicar_colores(cedula)
		_aplicar_colores(contraseña)

		def iniciar(e):
			usuario = iniciar_sesion(cedula.value or "", contraseña.value or "")
			if usuario is None:
				mostrar_mensaje(page, "Cédula o contraseña incorrecta.")
				return
			al_iniciar_sesion(usuario)

		def abrir_registro(e):
			mostrar_registro(
				page,
				lambda cedula_registrada: mostrar_formulario(
					cedula_registrada,
					"Cuenta creada. Ingresa tu contraseña para continuar.",
				),
			)

		controles = [
			ft.Text("GAVAD", size=30, weight=ft.FontWeight.BOLD, color=VERDE),
			ft.Text("Inicia sesión con tu cédula", size=16, color=VERDE),
		]
		if mensaje:
			controles.append(ft.Text(mensaje, color=VERDE))
		controles.extend(
			[
				cedula,
				contraseña,
				ft.Button(
					"Ingresar",
					on_click=iniciar,
					width=320,
					bgcolor=VERDE,
					color=CREMA,
				),
				ft.Text("¿No tienes cuenta?", color=VERDE),
				ft.TextButton(
					"Registrarme",
					on_click=abrir_registro,
					style=ft.ButtonStyle(color=VERDE),
				),
			]
		)
		page.add(
			ft.Container(
				content=ft.Container(
					content=ft.Column(
						controles,
						tight=True,
						spacing=14,
						horizontal_alignment=ft.CrossAxisAlignment.CENTER,
					),
					width=400,
					padding=28,
					bgcolor=CREMA,
					border=ft.Border.all(1, VERDE),
					border_radius=8,
				),
				alignment=ft.Alignment.CENTER,
				expand=True,
			)
		)
		page.update()

	mostrar_formulario()


def mostrar_registro(page: ft.Page, al_registrar):
	page.controls.clear()
	nombres = ft.TextField(label="Nombres")
	apellidos = ft.TextField(label="Apellidos")
	cedula = ft.TextField(label="Cédula")
	celular = ft.TextField(label="Celular")
	contraseña = ft.TextField(
		label="Contraseña",
		password=True,
		can_reveal_password=True,
	)

	for campo in (nombres, apellidos, cedula, celular, contraseña):
		_aplicar_colores(campo)

	def registrar(e):
		try:
			usuario = registrar_usuario(
				nombre=nombres.value or "",
				apellidos=apellidos.value or "",
				cedula=cedula.value or "",
				celular=celular.value or "",
				contraseña=contraseña.value or "",
			)
		except ValueError as error:
			mostrar_mensaje(page, str(error))
			return
		al_registrar(usuario.cedula)

	page.add(
		ft.Container(
			content=ft.Container(
				content=ft.Column(
					[
						ft.Text("Crear cuenta", size=28, weight=ft.FontWeight.BOLD, color=VERDE),
						nombres,
						apellidos,
						cedula,
						celular,
						contraseña,
						ft.Button(
							"Registrarme",
							on_click=registrar,
							width=320,
							bgcolor=VERDE,
							color=CREMA,
						),
						ft.TextButton(
							"Volver al inicio",
							on_click=lambda e: al_registrar(""),
							style=ft.ButtonStyle(color=VERDE),
						),
					],
					tight=True,
					spacing=12,
					horizontal_alignment=ft.CrossAxisAlignment.CENTER,
				),
				width=400,
				padding=28,
				bgcolor=CREMA,
				border=ft.Border.all(1, VERDE),
				border_radius=8,
			),
			alignment=ft.Alignment.CENTER,
			expand=True,
		)
	)
	page.update()
