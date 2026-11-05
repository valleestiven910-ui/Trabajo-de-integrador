from secrets import randbelow

from entidades import vaca, usuario, finca, medicamento, costo, producción, factura, alimentación
from Datos import lista_vacas, lista_finca, lista_usuario, lista_medicamento, lista_costo, lista_producción, lista_factura, lista_detalle_de_venta, lista_alimentación


def _generar_id_unico(registros, atributo_id):
    ids_existentes = {getattr(registro, atributo_id) for registro in registros}
    while True:
        id_generado = randbelow(90_000_000) + 10_000_000
        if id_generado not in ids_existentes:
            return id_generado


#===========
#Registrar un usuario
#===========
def registrar_usuario(id_usuario=None, nombre="", correo="", contraseña="", cedula="", celular="", apellidos=""):
    try:
        id_usuario = (
            _generar_id_unico(lista_usuario, "id_usuario")
            if id_usuario is None
            else int(id_usuario)
        )
    except (TypeError, ValueError) as error:
        raise ValueError("El ID de usuario debe ser un número entero.") from error

    nombre = str(nombre or "").strip()
    apellidos = str(apellidos or "").strip()
    cedula = str(cedula or "").strip()
    celular = str(celular or "").strip()
    contraseña = str(contraseña or "")
    if id_usuario <= 0 or not nombre or not apellidos or not cedula or not celular or not contraseña:
        raise ValueError("Completa nombre, apellidos, cédula, celular y contraseña.")
    if any(registrado.id_usuario == id_usuario or registrado.cedula == cedula for registrado in lista_usuario):
        raise ValueError("Ya existe un usuario con ese ID o cédula.")

    usuario_nuevo = usuario(
        id_usuario=id_usuario,
        nombres=nombre,
        apellidos=apellidos,
        cedula=cedula,
        celular=celular,
        contraseña=contraseña,
    )
    lista_usuario.append(usuario_nuevo)
    return usuario_nuevo


def listar_usuario():
    return lista_usuario

def buscar_usuario(id_usuario):
    try:
        id_usuario = int(id_usuario)
    except (TypeError, ValueError):
        return None
    for usuario_nuevo in lista_usuario:
        if usuario_nuevo.id_usuario == id_usuario:
            return usuario_nuevo
    return None

def eliminar_usuario(id_usuario):
    usuario_encontrado = buscar_usuario(id_usuario)
    if usuario_encontrado is None:
        return False
    if any(finca_actual.id_usuario == usuario_encontrado.id_usuario for finca_actual in lista_finca):
        raise ValueError("No se puede borrar un usuario que todavía tiene fincas registradas.")
    if any(vaca_actual.id_usuario == usuario_encontrado.id_usuario for vaca_actual in lista_vacas):
        raise ValueError("No se puede borrar un usuario que todavía tiene vacas registradas.")
    if any(
        usuario_encontrado.id_usuario
        in (factura_actual.ID_vendedor, factura_actual.ID_comprador)
        for factura_actual in lista_factura
    ):
        raise ValueError("No se puede borrar un usuario asociado a facturas registradas.")
    lista_usuario.remove(usuario_encontrado)
    return True


def actualizar_usuario(id_usuario, nombre, apellidos, cedula, celular, contraseña=None):
    usuario_existente = buscar_usuario(id_usuario)
    if usuario_existente is None:
        return False

    nombre = str(nombre or "").strip()
    apellidos = str(apellidos or "").strip()
    cedula = str(cedula or "").strip()
    celular = str(celular or "").strip()
    if not nombre or not apellidos or not cedula or not celular:
        raise ValueError("Nombre, apellidos, cédula y celular son obligatorios.")
    if any(
        otro.id_usuario != usuario_existente.id_usuario and otro.cedula == cedula
        for otro in lista_usuario
    ):
        raise ValueError("Ya existe otro usuario con esa cédula.")
    if contraseña is not None and str(contraseña):
        usuario_existente.contraseña = str(contraseña)

    usuario_existente.nombres = nombre
    usuario_existente.apellidos = apellidos
    usuario_existente.cedula = cedula
    usuario_existente.celular = celular
    return True

def iniciar_sesion(cédula, contraseña):
    cedula_ingresada = str(cédula or "").strip()
    contraseña_ingresada = str(contraseña or "")
    for u in lista_usuario:
        if u.cedula == cedula_ingresada and u.contraseña == contraseña_ingresada:
            return u
    return None 


#================
#Registrar la finca
# ============ 
def registrar_finca(id_finca=None, id_usuario=None, departamento="", ubicacion="", nombre_finca=""):
    try:
        id_usuario = int(id_usuario)
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona un usuario dueño válido.") from error

    if buscar_usuario(id_usuario) is None:
        raise ValueError("Registra primero al usuario que será dueño de la finca.")
    departamento = str(departamento or "").strip()
    ubicacion = str(ubicacion or "").strip()
    nombre_finca = str(nombre_finca or "").strip()
    if not departamento or not ubicacion or not nombre_finca:
        raise ValueError("Departamento, ubicación y nombre de finca son obligatorios.")

    try:
        id_finca = (
            _generar_id_unico(lista_finca, "id_finca")
            if id_finca is None
            else int(id_finca)
        )
    except (TypeError, ValueError) as error:
        raise ValueError("El ID de finca debe ser un número entero.") from error
    if id_finca <= 0 or any(registrada.id_finca == id_finca for registrada in lista_finca):
        raise ValueError("El ID de finca debe ser positivo y único.")

    nueva_finca = finca(
        id_finca=id_finca,
        id_usuario=id_usuario,
        departamento=departamento,
        ubicación=ubicacion,
        nombre_finca=nombre_finca,
    )
    lista_finca.append(nueva_finca)
    return nueva_finca

def listar_fincas():
    return lista_finca

def buscar_finca(id_finca):
    try:
        id_finca = int(id_finca)
    except (TypeError, ValueError):
        return None
    for finca_a_registrar in lista_finca:
        if finca_a_registrar.id_finca == id_finca:
            return finca_a_registrar
    return None

def actualizar_finca(id_finca, id_usuario, departamento, ubicacion, nombre_finca):
    finca_existente = buscar_finca(id_finca)
    if finca_existente is None:
        return False

    try:
        id_usuario = int(id_usuario)
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona un usuario dueño válido.") from error
    if buscar_usuario(id_usuario) is None:
        raise ValueError("Selecciona un usuario registrado.")
    if id_usuario != finca_existente.id_usuario and any(
        vaca_actual.id_finca == finca_existente.id_finca
        for vaca_actual in lista_vacas
    ):
        raise ValueError(
            "Primero cambia las vacas de finca antes de cambiar el dueño de esta finca."
        )
    departamento = str(departamento or "").strip()
    ubicacion = str(ubicacion or "").strip()
    nombre_finca = str(nombre_finca or "").strip()
    if not departamento or not ubicacion or not nombre_finca:
        raise ValueError("Departamento, ubicación y nombre de finca son obligatorios.")

    finca_existente.id_usuario = id_usuario
    finca_existente.departamento = departamento
    finca_existente.ubicación = ubicacion
    finca_existente.nombre_finca = nombre_finca
    return True

def eliminar_finca(id_finca):
    finca_encontrada = buscar_finca(id_finca)
    if finca_encontrada is None:
        return False
    if any(vaca_actual.id_finca == finca_encontrada.id_finca for vaca_actual in lista_vacas):
        raise ValueError("No se puede borrar una finca que todavía tiene vacas registradas.")
    lista_finca.remove(finca_encontrada)
    return True

#==========
#Registrar una vaca 
#===========
def registrar_vaca(
    id_usuario,
    id_finca,
    nombre_vaca,
    raza,
    color,
    peso,
    imagen="",
    en_catalogo=False,
    precio_venta="",
    salud="",
    vacunas="",
    motivo_venta="",
    id_arete=None,
):
    try:
        id_usuario = int(id_usuario)
        id_finca = int(id_finca)
        peso = float(peso)
        id_arete = int(id_arete)
    except (TypeError, ValueError) as error:
        raise ValueError("El ID de arete y los IDs relacionados deben ser enteros; el peso debe ser numérico.") from error
    try:
        precio_venta = (
            _parsear_precio(precio_venta)
            if str(precio_venta or "").strip()
            else 0.0
        )
    except ValueError as error:
        raise ValueError(f"El precio de venta no es válido: {error}") from error

    if id_usuario <= 0 or id_finca <= 0:
        raise ValueError("Los IDs de usuario y finca deben ser mayores que cero.")
    if buscar_usuario(id_usuario) is None:
        raise ValueError("Registra primero al usuario dueño de la vaca.")
    finca_vaca = buscar_finca(id_finca)
    if finca_vaca is None:
        raise ValueError("Selecciona una finca registrada.")
    if finca_vaca.id_usuario != id_usuario:
        raise ValueError("La finca seleccionada pertenece a otro usuario.")
    if id_arete <= 0:
        raise ValueError("Ingresa un número de arete válido.")
    if any(registrada.id_vaca == id_arete for registrada in lista_vacas):
        raise ValueError("Ya existe una vaca registrada con ese número de arete.")
    nombre_vaca = str(nombre_vaca or "").strip()
    raza = str(raza or "").strip()
    color = str(color or "").strip()
    imagen = str(imagen or "").strip()
    if not nombre_vaca or not raza or not color:
        raise ValueError("Nombre, raza y color son obligatorios.")
    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")
    if precio_venta < 0:
        raise ValueError("El precio de venta no puede ser negativo.")
    if en_catalogo and not imagen:
        raise ValueError("Agrega una foto antes de publicar la vaca en el catálogo.")

    nueva_vaca = vaca(
        id_vaca=id_arete,
        id_usuario=id_usuario,
        id_finca=id_finca,
        nombre_vaca=nombre_vaca,
        raza=raza,
        color=color,
        peso=peso,
        imagen=imagen,
        en_catalogo=bool(en_catalogo),
        precio_venta=precio_venta,
        salud=str(salud or "").strip(),
        vacunas=str(vacunas or "").strip(),
        motivo_venta=str(motivo_venta or "").strip(),
    )
    lista_vacas.append(nueva_vaca)
    return nueva_vaca

def listar_vacas():
    return lista_vacas

def buscar_vaca(id_vaca):
    try:
        id_vaca = int(id_vaca)
    except (TypeError, ValueError):
        return None
    for vaca in lista_vacas:
        if vaca.id_vaca == id_vaca:
            return vaca
    return None

def actualizar_vaca(
    id_vaca,
    id_usuario,
    id_finca,
    nombre_vaca,
    raza,
    peso,
    color,
    imagen=None,
    en_catalogo=None,
    precio_venta=None,
    salud=None,
    vacunas=None,
    motivo_venta=None,
):
    vaca_existente = buscar_vaca(id_vaca)
    if vaca_existente is None:
        return False

    try:
        id_usuario = int(id_usuario)
        id_finca = int(id_finca)
        peso = float(peso)
        precio_venta = (
            vaca_existente.precio_venta
            if precio_venta is None
            else (
                _parsear_precio(precio_venta)
                if str(precio_venta or "").strip()
                else 0.0
            )
        )
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona usuario y finca válidos, e ingresa valores numéricos.") from error

    finca_vaca = buscar_finca(id_finca)
    if buscar_usuario(id_usuario) is None:
        raise ValueError("Selecciona un usuario dueño registrado.")
    if finca_vaca is None or finca_vaca.id_usuario != id_usuario:
        raise ValueError("Selecciona una finca registrada que pertenezca al dueño.")

    nombre_vaca = str(nombre_vaca or "").strip()
    raza = str(raza or "").strip()
    color = str(color or "").strip()
    imagen = vaca_existente.imagen if imagen is None else str(imagen or "").strip()
    en_catalogo = vaca_existente.en_catalogo if en_catalogo is None else bool(en_catalogo)
    if not nombre_vaca or not raza or not color:
        raise ValueError("Nombre, raza y color son obligatorios.")
    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")
    if precio_venta < 0:
        raise ValueError("El precio de venta no puede ser negativo.")
    if en_catalogo and not imagen:
        raise ValueError("Agrega una imagen antes de publicar la vaca en el catálogo.")

    vaca_existente.id_usuario = id_usuario
    vaca_existente.id_finca = id_finca
    vaca_existente.nombre_vaca = nombre_vaca
    vaca_existente.raza = raza
    vaca_existente.color = color
    vaca_existente.peso = peso
    vaca_existente.imagen = imagen
    vaca_existente.en_catalogo = en_catalogo
    vaca_existente.precio_venta = precio_venta
    if salud is not None:
        vaca_existente.salud = str(salud or "").strip()
    if vacunas is not None:
        vaca_existente.vacunas = str(vacunas or "").strip()
    if motivo_venta is not None:
        vaca_existente.motivo_venta = str(motivo_venta or "").strip()
    return True

def eliminar_vaca(id_vaca):
    vaca_encontrada= buscar_vaca(id_vaca)

    if vaca_encontrada is None:
        return False
    if any(factura_actual.id_vaca == vaca_encontrada.id_vaca for factura_actual in lista_factura):
        raise ValueError("No se puede borrar una vaca que ya tiene una factura registrada.")

    id_registro = vaca_encontrada.id_vaca
    lista_vacas.remove(vaca_encontrada)
    lista_costo[:] = [registro for registro in lista_costo if registro.id_vaca != id_registro]
    lista_medicamento[:] = [registro for registro in lista_medicamento if registro.id_vaca != id_registro]
    lista_producción[:] = [registro for registro in lista_producción if registro.id_vaca != id_registro]
    lista_alimentación[:] = [
        registro for registro in lista_alimentación if registro.id_vaca != id_registro
    ]
    lista_detalle_de_venta[:] = [
        registro for registro in lista_detalle_de_venta if registro.id_vaca != id_registro
    ]
    return True

#============
#Costo
#===========
def regitrar_costo(id_costo, id_finca, nombre_costo, valor):


    id_costo = _generar_id_unico(lista_costo, "id_costos")

    costo_nuevo = costo(
        id= int(id_costo),
        id_finca=(id_finca),
        nombre=nombre_costo,
        valor=float(valor)
    )
    lista_costo.append(costo_nuevo)


def listar_costos():
    return lista_costo


def _parsear_precio(precio):
    texto = str(precio or "").strip().replace(" ", "")
    if not texto:
        raise ValueError("El precio debe ser numérico.")

    if "," in texto and "." in texto:
        separador_decimal = "," if texto.rfind(",") > texto.rfind(".") else "."
        separador_miles = "." if separador_decimal == "," else ","
        entero, decimales = texto.rsplit(separador_decimal, 1)
        entero = entero.replace(separador_miles, "")
        if not entero.isdigit() or not decimales.isdigit():
            raise ValueError("El formato del precio no es válido.")
        texto_normalizado = f"{entero}.{decimales}"
    elif "," in texto:
        grupos = texto.split(",")
        if grupos[0].isdigit() and all(
            grupo.isdigit() and len(grupo) == 3 for grupo in grupos[1:]
        ):
            texto_normalizado = "".join(grupos)
        elif len(grupos) == 2 and all(grupo.isdigit() for grupo in grupos):
            texto_normalizado = f"{grupos[0]}.{grupos[1]}"
        else:
            raise ValueError("El formato del precio no es válido.")
    else:
        texto_normalizado = texto

    try:
        return float(texto_normalizado)
    except ValueError as error:
        raise ValueError("El precio debe ser numérico.") from error


def registrar_costo_vaca(id_vaca, descripcion, fecha, precio):
    try:
        id_vaca = int(id_vaca)
        precio = _parsear_precio(precio)
    except (TypeError, ValueError) as error:
        raise ValueError("El ID de vaca debe ser entero y el precio debe ser numérico.") from error

    if buscar_vaca(id_vaca) is None:
        raise ValueError("No se encontró la vaca seleccionada.")
    descripcion = str(descripcion or "").strip()
    fecha = str(fecha or "").strip()
    if not descripcion or not fecha:
        raise ValueError("La descripción y la fecha son obligatorias.")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    nuevo_costo = costo(
        id_costos=_generar_id_unico(lista_costo, "id_costos"),
        id_vaca=id_vaca,
        fecha=fecha,
        precio=precio,
        descripcion=descripcion,
    )
    lista_costo.append(nuevo_costo)
    return nuevo_costo

def buscar_costo(id_costo):
    try:
        id_costo = int(id_costo)
    except (TypeError, ValueError):
        return None
    for costo_nuevo in lista_costo:
        if costo_nuevo.id_costos == id_costo:
            return costo_nuevo
    return None

def actualizar_costo(id_costo, descripcion, fecha, precio):
    costo_existente = buscar_costo(id_costo)
    if costo_existente is None:
        return False

    descripcion = str(descripcion or "").strip()
    fecha = str(fecha or "").strip()
    if not descripcion or not fecha:
        raise ValueError("La descripción y la fecha son obligatorias.")
    try:
        precio = _parsear_precio(precio)
    except ValueError as error:
        raise ValueError(f"El precio no es válido: {error}") from error
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    costo_existente.descripcion = descripcion
    costo_existente.fecha = fecha
    costo_existente.precio = precio
    return True

def eliminar_costo(id_costo):
    costo_encontrado= buscar_costo(id_costo)

    if costo_encontrado:
        lista_costo.remove(costo_encontrado)
        return True
    return False

def comparar_costos_por_vaca(id_finca):
    costos_encontrados = []
    for costo_nuevo in lista_costo:
        if costo_nuevo.id_finca == id_finca:
            costos_encontrados.append(costo)
    return costos_encontrados


#====================
#factura
#================

def crear_factura(
    id_factura=None,
    monto_pagado=0.0,
    fecha="",
    id_vendedor=0,
    id_comprador=0,
    id_vaca=None,
    nombre_comprador="",
    cedula_comprador="",
    nombre_vendedor="",
    cedula_vendedor="",
):
    if id_factura is None:
        id_factura = _generar_id_unico(lista_factura, "id_factura")

    if any(factura_actual.id_factura == int(id_factura) for factura_actual in lista_factura):
        return False  # La factura ya existe, no se puede crear una nueva con el mismo ID

    factura_nueva = factura(
        id_factura=int(id_factura),
        monto_pagado=float(monto_pagado),
        fecha=fecha,
        ID_vendedor=int(id_vendedor),
        ID_comprador=int(id_comprador),
        id_vaca=int(id_vaca) if id_vaca is not None else None,
        nombre_comprador=nombre_comprador,
        cedula_comprador=cedula_comprador,
        nombre_vendedor=nombre_vendedor,
        cedula_vendedor=cedula_vendedor,
    )

    lista_factura.append(factura_nueva)
    return factura_nueva

def listar_factura():
    return lista_factura

def buscar_factura(id_factura):
    for factura_nueva in lista_factura:
        if factura_nueva.id_factura==id_factura:
            return factura_nueva
        return None

def actualizar_factura(id_factura, monto_pagado, fecha, id_vendedor, id_comprador):
     factura_nueva= buscar_factura (id_factura)



     if factura_nueva:
         factura_nueva.id_factura=id_factura,
         factura_nueva.monto_pagado= monto_pagado,
         factura_nueva.fecha= fecha,
         factura_nueva.id_vendedor=id_vendedor,
         factura_nueva.id_comprador= id_comprador
         return True
     return False

    
def eliminar_factura(id_factura):
    factura_encontrada=buscar_factura(id_factura)

    if factura_encontrada:
        lista_factura.remove(factura_encontrada)
        return True
    return False




#========================
#detalle de la venta
#========================

def crear_descripción_de_la_venta(id_detalle, id_vaca, cantidad, precio):
    id_detalle = _generar_id_unico(lista_detalle_de_venta, "id_detalle")

    detalle = lista_detalle_de_venta(
        id_detalle=int(id_detalle),
        id_vaca= int(id_vaca),
        cantidad= int(cantidad),
        precio= float(precio)
    )


    lista_detalle_de_venta.append(detalle)
    return detalle

def historial_detalle():
    return lista_detalle_de_venta



def buscar_detalle_de_venta(id_detalle):
    for detalle_nuevo in lista_detalle_de_venta:

        if detalle_nuevo.id_detalle==id_detalle:
            return detalle_nuevo
        return None

def actualiza_detalle(id_detalle, id_vaca, cantidad, precio):
    detalle_nuevo= buscar_detalle_de_venta(id_detalle)


    if detalle_nuevo:
        detalle_nuevo.id_detalle=id_detalle,
        detalle_nuevo.id_vaca=id_vaca,
        detalle_nuevo.cantidad=cantidad,
        detalle_nuevo.precio=precio

        return True
    return False
def listar_detalle_de_venta():
    return lista_detalle_de_venta


def eliminar_detalle(id_detalle):
    detalle_encontrado=buscar_detalle_de_venta(id_detalle)

    if detalle_encontrado:
        lista_detalle_de_venta.remove(detalle_encontrado)
        return True
    return False






#===========
#registro de medicamento
#==============
def registrar_medicamento(
    id_medicamento=None,
    id_vaca=None,
    remedio="",
    fecha="",
    peso_anterior_de_la_vaca="",
    peso_actual_de_la_vaca="",
    dosis_por_vacas="",
):
    try:
        id_vaca = int(id_vaca)
        peso_anterior = float(peso_anterior_de_la_vaca)
        peso_actual = float(peso_actual_de_la_vaca)
        dosis = float(dosis_por_vacas)
        id_medicamento = (
            _generar_id_unico(lista_medicamento, "id_medicamento")
            if id_medicamento is None
            else int(id_medicamento)
        )
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona una vaca e ingresa pesos y dosis numéricos.") from error

    if buscar_vaca(id_vaca) is None:
        raise ValueError("Registra primero una vaca.")
    remedio = str(remedio or "").strip()
    fecha = str(fecha or "").strip()
    if id_medicamento <= 0 or not remedio or not fecha:
        raise ValueError("Remedio y fecha son obligatorios.")
    if peso_anterior <= 0 or peso_actual <= 0 or dosis <= 0:
        raise ValueError("Los pesos y la dosis deben ser mayores que cero.")

    nuevo_medicamento = medicamento(
        id_medicamento=id_medicamento,
        id_vaca=id_vaca,
        remedio=remedio,
        fecha=fecha,
        peso_anterior_de_la_vaca=peso_anterior,
        peso_actual_de_la_vaca=peso_actual,
        dosis_por_vacas=str(dosis),
    )

    lista_medicamento.append(nuevo_medicamento)
    return nuevo_medicamento

def listar_medicamento():
    return lista_medicamento

def buscar_medicamento(id_medicamento):
    try:
        id_medicamento = int(id_medicamento)
    except (TypeError, ValueError):
        return None
    for nuevo_medicamento in lista_medicamento:
        if nuevo_medicamento.id_medicamento == id_medicamento:
            return nuevo_medicamento
    return None

    
def actualizar_medicamento(id_medicamento, id_vaca, remedio, fecha, peso_anterior_de_la_vaca, peso_actual_de_la_vaca, dosis_por_vacas):
    registro = buscar_medicamento(id_medicamento)
    if registro is None:
        return False
    try:
        id_vaca = int(id_vaca)
        peso_anterior = float(peso_anterior_de_la_vaca)
        peso_actual = float(peso_actual_de_la_vaca)
        dosis = float(dosis_por_vacas)
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona una vaca e ingresa pesos y dosis numéricos.") from error
    if buscar_vaca(id_vaca) is None:
        raise ValueError("Selecciona una vaca registrada.")
    remedio = str(remedio or "").strip()
    fecha = str(fecha or "").strip()
    if not remedio or not fecha:
        raise ValueError("Remedio y fecha son obligatorios.")
    if peso_anterior <= 0 or peso_actual <= 0 or dosis <= 0:
        raise ValueError("Los pesos y la dosis deben ser mayores que cero.")

    registro.id_vaca = id_vaca
    registro.remedio = remedio
    registro.fecha = fecha
    registro.peso_anterior_de_la_vaca = peso_anterior
    registro.peso_actual_de_la_vaca = peso_actual
    registro.dosis_por_vacas = str(dosis)
    return True

def eliminar_medicamento(id_medicamento):
    medicamento_encontrado= buscar_medicamento(id_medicamento)


    if medicamento_encontrado:
        lista_medicamento.remove(medicamento_encontrado)
        return True
    return False




#=========
#producción
#=========
def registrar_producción(id_producción=None, id_vaca=None, cantidad="", Litros="", fecha=""):
    try:
        id_vaca = int(id_vaca)
        cantidad = float(cantidad)
        litros = float(Litros)
        id_producción = (
            _generar_id_unico(lista_producción, "id_producción")
            if id_producción is None
            else int(id_producción)
        )
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona una vaca e ingresa cantidades numéricas.") from error

    if buscar_vaca(id_vaca) is None:
        raise ValueError("Registra primero una vaca.")
    fecha = str(fecha or "").strip()
    if id_producción <= 0 or not fecha:
        raise ValueError("La fecha es obligatoria.")
    if cantidad <= 0 or litros <= 0:
        raise ValueError("Las cantidades deben ser mayores que cero.")

    nueva_producción = producción(
        id_producción=id_producción,
        id_vaca=id_vaca,
        cantidad=cantidad,
        Litros=litros,
        fecha=fecha,
    )


    lista_producción.append (nueva_producción)
    return nueva_producción

def listar_producciones():
    return lista_producción

def buscar_producción(id_producción):
    try:
        id_producción = int(id_producción)
    except (TypeError, ValueError):
        return None
    for nueva_producción in lista_producción:
        if nueva_producción.id_producción == id_producción:
            return nueva_producción
    return None

def actualizar_producción(id_producción, id_vaca, cantidad, Litros, fecha):
    nueva_producción = buscar_producción(id_producción)
    if nueva_producción is None:
        return False
    try:
        id_vaca = int(id_vaca)
        cantidad = float(cantidad)
        Litros = float(Litros)
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona una vaca e ingresa cantidades numéricas.") from error
    if buscar_vaca(id_vaca) is None:
        raise ValueError("Selecciona una vaca registrada.")
    fecha = str(fecha or "").strip()
    if not fecha:
        raise ValueError("La fecha es obligatoria.")
    if cantidad <= 0 or Litros <= 0:
        raise ValueError("Las cantidades deben ser mayores que cero.")

    nueva_producción.id_vaca = id_vaca
    nueva_producción.cantidad = cantidad
    nueva_producción.Litros = Litros
    nueva_producción.fecha = fecha
    return True





def eliminar_producción(id_producción):
    producción_encontrada= buscar_producción(id_producción)
    if producción_encontrada:
        lista_producción.remove(producción_encontrada)
        return True
    return False



def registrar_alimentación(
    id_alimentación=None,
    tipo_de_alimento="",
    descripción="",
    cantidad="",
    fecha="",
    costo_alimento="",
    id_vaca=None,
):
    try:
        cantidad = float(cantidad)
        costo_alimento = float(costo_alimento)
        id_alimentación = (
            _generar_id_unico(lista_alimentación, "id_alimentacion")
            if id_alimentación is None
            else int(id_alimentación)
        )
        id_vaca = int(id_vaca) if id_vaca not in (None, "") else None
    except (TypeError, ValueError) as error:
        raise ValueError("La cantidad y el costo deben ser numéricos; selecciona una vaca válida.") from error

    if id_vaca is not None and buscar_vaca(id_vaca) is None:
        raise ValueError("Selecciona una vaca registrada o deja el registro como alimentación general.")
    tipo_de_alimento = str(tipo_de_alimento or "").strip()
    descripción = str(descripción or "").strip()
    fecha = str(fecha or "").strip()
    if id_alimentación <= 0 or not tipo_de_alimento or not descripción or not fecha:
        raise ValueError("Tipo, descripción y fecha son obligatorios.")
    if cantidad <= 0 or costo_alimento < 0:
        raise ValueError("La cantidad debe ser mayor que cero y el costo no puede ser negativo.")

    nueva_alimentación = alimentación(
        id_alimentacion=id_alimentación,
        tipo_de_alimento=tipo_de_alimento,
        descripción=descripción,
        cantidad=cantidad,
        fecha=fecha,
        costo_alimento=costo_alimento,
        id_vaca=id_vaca,
    )

    lista_alimentación.append(nueva_alimentación)
    return nueva_alimentación


def listar_alimentación():
    return lista_alimentación


def buscar_alimentación(id_alimentación):
    try:
        id_alimentación = int(id_alimentación)
    except (TypeError, ValueError):
        return None
    for nueva_alimentación in lista_alimentación:
        if nueva_alimentación.id_alimentacion == id_alimentación:
            return nueva_alimentación
    return None

def actualizar_alimentación(
    id_alimentación,
    tipo_de_alimento,
    descripción,
    cantidad,
    fecha,
    costo_alimento,
    id_vaca=None,
):
    nueva_alimentación = buscar_alimentación(id_alimentación)
    if nueva_alimentación is None:
        return False
    try:
        cantidad = float(cantidad)
        costo_alimento = float(costo_alimento)
        id_vaca = int(id_vaca) if id_vaca not in (None, "") else None
    except (TypeError, ValueError) as error:
        raise ValueError("Cantidad y costo deben ser numéricos; selecciona una vaca válida.") from error
    if id_vaca is not None and buscar_vaca(id_vaca) is None:
        raise ValueError("Selecciona una vaca registrada o alimentación general.")
    if cantidad <= 0 or costo_alimento < 0:
        raise ValueError("La cantidad debe ser mayor que cero y el costo no puede ser negativo.")

    tipo_de_alimento = str(tipo_de_alimento or "").strip()
    descripción = str(descripción or "").strip()
    fecha = str(fecha or "").strip()
    if not tipo_de_alimento or not descripción or not fecha:
        raise ValueError("Tipo, descripción y fecha son obligatorios.")

    nueva_alimentación.tipo_de_alimento = tipo_de_alimento
    nueva_alimentación.descripción = descripción
    nueva_alimentación.cantidad = cantidad
    nueva_alimentación.fecha = fecha
    nueva_alimentación.costo_alimento = costo_alimento
    nueva_alimentación.id_vaca = id_vaca
    return True


def eliminar_alimentación(id_alimentación):
    alimentación_encontrada= buscar_alimentación(id_alimentación)

    if alimentación_encontrada:
        lista_alimentación.remove(alimentación_encontrada)
        return True
    return False

def listar_vacas_en_catalogo():
    todas_las_vacas = lista_vacas

    vacas_seleccionadas = [v for v in todas_las_vacas if v.en_catalogo==True]

    return vacas_seleccionadas

def actualizar_estado_y_foto_catalogo(id_vaca, en_catalogo, imagen):
    vaca_encontrada = buscar_vaca(id_vaca)
    if vaca_encontrada: 
        vaca_encontrada.en_catalogo = en_catalogo
        vaca_encontrada.imagen =imagen
        return True
    return False
    