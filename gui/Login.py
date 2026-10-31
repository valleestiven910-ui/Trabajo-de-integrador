import flet as ft

from funciones import iniciar_sesion, registrar_usuario


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

		def iniciar(e):
			usuario = iniciar_sesion(cedula.value or "", contraseña.value or "")
			if usuario is None:
				page.snack_bar = ft.SnackBar(ft.Text("Cédula o contraseña incorrecta."))
				page.snack_bar.open = True
				page.update()
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
			ft.Text("GAVAD", size=30, weight=ft.FontWeight.BOLD),
			ft.Text("Inicia sesión con tu cédula", size=16),
		]
		if mensaje:
			controles.append(ft.Text(mensaje, color=ft.colors.GREEN))
		controles.extend(
			[
				cedula,
				contraseña,
				ft.ElevatedButton("Ingresar", on_click=iniciar, width=320),
				ft.Text("¿No tienes cuenta?"),
				ft.TextButton("Registrarme", on_click=abrir_registro),
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
					border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
					border_radius=8,
				),
				alignment=ft.alignment.center,
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
			page.snack_bar = ft.SnackBar(ft.Text(str(error)))
			page.snack_bar.open = True
			page.update()
			return
		al_registrar(usuario.cedula)

	page.add(
		ft.Container(
			content=ft.Container(
				content=ft.Column(
					[
						ft.Text("Crear cuenta", size=28, weight=ft.FontWeight.BOLD),
						nombres,
						apellidos,
						cedula,
						celular,
						contraseña,
						ft.ElevatedButton("Registrarme", on_click=registrar, width=320),
						ft.TextButton("Volver al inicio", on_click=lambda e: al_registrar("")),
					],
					tight=True,
					spacing=12,
					horizontal_alignment=ft.CrossAxisAlignment.CENTER,
				),
				width=400,
				padding=28,
				border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
				border_radius=8,
			),
			alignment=ft.alignment.center,
			expand=True,
		)
	)
	page.update()
